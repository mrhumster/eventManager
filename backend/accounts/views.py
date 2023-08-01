from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from accounts import logger
from accounts.forms import LoginForm, SigninForm, UpdateForm, SettingsForm, ForgotPasswordForm, ChangePasswordForm
from accounts.models import Token, Settings
from eventManager.settings import LOGIN_REDIRECT_URL, SITE_SCHEMA, MODERATOR_MAIL
from accounts.tasks import send_email

FORM_ERROR_TEXT = 'Форма заполнена с ошибками!'


def index(request):
    match request.method:
        case 'GET':
            cache.set('next', request.GET.get('next', None))
            form = LoginForm()

        case 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username=username, password=password)
                if user is not None and user.is_active:
                    login(request, user)
                    if not request.user.is_anonymous:
                        messages.add_message(
                            request,
                            messages.SUCCESS,
                            f'Привет, {request.user.first_name} {request.user.last_name}!'
                        )
                        token, create = Token.objects.get_or_create(owner=user)
                        if not token.email_verified:
                            messages.warning(
                                request, 'Ваш адрес электронной почты не подтверждён. Функционал может быть ограничен. '
                                         'Если вы не получили письмо с подтверждением, можете запросить его повторно в '
                                         'представлении "Профиль" пользователя.')
                    if cache.get("next"):
                        return redirect(cache.get("next"))
                    else:
                        return redirect(LOGIN_REDIRECT_URL)
                elif user is not None and not user.is_active:
                    if user.is_staff:
                        messages.add_message(
                            request, messages.INFO,
                            f'Пользователь отключен. Вы запросили роль "Специалист", поэтому письмо для подтверждения учетной записи было отправлено администратору. Если возникли вопросы, напишите письмо на адрес: {MODERATOR_MAIL}')
                    else:
                        messages.add_message(
                            request, messages.INFO,
                            'Пользователь отключен. Для завершения регистрации, перейдите по ссылке из письма.')
                else:
                    form.add_error('password', 'Проверьте правильность ввода пароля')
                    messages.add_message(request, messages.ERROR, FORM_ERROR_TEXT)
            else:
                messages.add_message(request, messages.ERROR, FORM_ERROR_TEXT)

    return render(request, 'accounts/index.html', {'form': form})


@login_required()
def change_password_view(request):
    match request.method:
        case 'GET':
            form = ChangePasswordForm()
            return render(request, 'accounts/change_password.html', {'form': form})

        case 'POST':
            form = ChangePasswordForm(request.POST, request=request)
            user = request.user
            if form.is_valid():
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.info(request, 'Пароль изменён')
                return render(request, 'accounts/profile.html')
            else:
                messages.error(request, 'Форма не прошла проверку')
                return render(request, 'accounts/change_password.html', {'form': form})


def forgot_password_view(request):
    match request.method:
        case 'GET':
            form = ForgotPasswordForm()
            return render(request, 'accounts/forgot_password.html', {'form': form})
        case 'POST':
            form = ForgotPasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(username__iexact=form.cleaned_data['username'])
                password = User.objects.make_random_password()
                user.set_password(password)
                user.save()
                if user.token.first().email_verified:
                    msg = {
                        'subject': f'🔒 Ваш пароль для входа',
                        'body': f'{user.username} {password}',
                        'recipients': [user.email],
                        'template': 'messages/forgot_password.html',
                        'url': f"{SITE_SCHEMA}://{Site.objects.get_current().domain}"
                    }
                    send_email.delay(**msg)
                    messages.info(request, 'Письмо с паролем отправлено')
                    return redirect('accounts:index')
                else:
                    messages.warning(request, f'Ваш адрес электронной почты не был подтвержден!<br><hr>'
                                              f'Обратитесь к администратору: <a href="mailto:{MODERATOR_MAIL}">{MODERATOR_MAIL}</a>', extra_tags='safe')
                    return redirect('accounts:index')
            else:
                return render(request, 'accounts/forgot_password.html', {'form': form})


@login_required
def settings_view(request):
    match request.method:
        case 'GET':
            user_settings, created = Settings.objects.get_or_create(user=request.user)
            form = SettingsForm(instance=user_settings)
            return render(request, 'accounts/settings.html', {'form': form})
        case 'POST':
            form = SettingsForm(data=request.POST)
            if form.is_valid():
                user_settings = Settings.objects.get(user=request.user)
                [setattr(user_settings, field, form.cleaned_data[field]) for field in SettingsForm._meta.fields]
                user_settings.save()
                messages.success(request, 'Настройки сохранены')
                return redirect('accounts:settings')
            else:
                return render(request, 'accounts/settings.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('accounts:index')


def signin_view(request):
    match request.method:
        case 'POST':
            form = SigninForm(request.POST)
            if form.is_valid():
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    email=form.cleaned_data.get('email'),
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    password=form.cleaned_data.get('password'),
                )

                if form.cleaned_data.get('group') == 'staff':
                    user.is_staff = True

                token = Token.objects.create(owner=user)
                settings, _ = Settings.objects.get_or_create(user=user)
                group, _ = Group.objects.get_or_create(name=form.cleaned_data.get('group'))
                if _:
                    logger.debug(f'Создана новая группа пользователей: {group}')
                user.groups.add(group)
                user.is_active = False
                user.save()

                if group.name == 'user':
                    messages.success(request, f'Пользователь сохранен. Проверьте почту.')
                    send_email.delay(
                        subject=f'Пользователь зарегистрирован',
                        body=f'Пользователь {user.email} зарегистрирован. Для завершения регистрации, необходимо нажать перейти [по ссылке](url).',
                        recipients=[user.email],
                        from_email='ru89050995432@yandex.ru',
                        template='messages/email_confirm.html',
                        check_email_verified=False,
                        confirm_url=token.get_absolute_url()
                    )
                    token.sendmail_date = timezone.now()
                    token.save()
                elif group.name == 'staff':
                    messages.success(
                        request,
                        f'Пользователь сохранен. Письмо с подтверждением, будет выслано после модерации администратором.'
                    )
                    send_email.delay(
                        subject=f'🫂 Пользователь зарегистрирован',
                        body=f'Пользователь {user.email} зарегистрирован. Для завершения регистрации, необходимо нажать перейти [по ссылке](url).',
                        recipients=[MODERATOR_MAIL],
                        template='messages/email_confirm_service.html',
                        check_email_verified=False,
                        confirm_url=token.get_absolute_url()
                    )
                    token.sendmail_date = timezone.now()
                    user.save()
                return redirect('accounts:index')

            else:
                messages.add_message(request, messages.ERROR, FORM_ERROR_TEXT)
        case 'GET':
            form = SigninForm()
    return render(request, 'accounts/signin.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def delete_view(request):
    user = request.user
    logout(request)
    user.delete()
    messages.add_message(request, messages.WARNING, f'Пользователь {request.user.username} удалён.')
    return redirect('accounts:index')


@login_required
def update_view(request):
    match request.method:
        case 'POST':
            form = UpdateForm(data=request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль пользователя обновлен')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Что-то пошло не так')
                return render(request, 'accounts/update.html', {'form': form})
        case 'GET':
            form = UpdateForm(instance=request.user)
            return render(request, 'accounts/update.html', {'form': form})


def confirm_view(request, token):
    match request.method:
        case 'GET':
            try:
                token = Token.objects.get(uid=token)
                token.email_verified = True
                token.verified_date = timezone.now()
                token.save()
                user = token.owner
                user.is_active = True
                user.save()
                messages.success(request, 'Почта подтверждена')
                send_email.delay(
                    subject=f'Адрес электронной почти подтвержден',
                    body=f'Пользователь {user.username} зарегистрирован.',
                    recipients=[user.email],
                    from_email='ru89050995432@yandex.ru',
                    template='messages/email_verified.html',
                    check_email_verified=True,
                )
            except ObjectDoesNotExist:
                messages.error(request, 'Токен не существует')
            finally:
                return redirect(LOGIN_REDIRECT_URL)


@login_required
@permission_required("accounts.view_settings", raise_exception=True)
def userprofile_view(request, username):
    match request.method:
        case 'GET':
            user = get_object_or_404(User, username=username)
            return render(request, 'accounts/user_profile.html', {'user':  user})


@login_required
def email_verified_view(request):
    match request.method:
        case 'GET':
            user = request.user
            token = user.token.first()
            send_email.delay(
                subject=f'🫂 Пользователь зарегистрирован',
                body=f'Пользователь {user} зарегистрирован. Для завершения регистрации, необходимо нажать перейти [по ссылке](url).',
                recipients=[user.email],
                template='messages/email_confirm.html',
                check_email_verified=False,
                confirm_url=token.get_absolute_url()
            )
            token.sendmail_date = timezone.now()
            token.save()
            messages.info(request, 'Письмо отправлено')
            return redirect('accounts:profile')
