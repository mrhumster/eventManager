from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewEventView, ListEventView, DetailEventView, DeleteEventView, RegisterView, CancelView, \
    UpdateEventView, AddGuestView, DetailGuestListView, RegisterRefusedGuestView, CancelRegisteredGuestView, \
    SetVisitedGuestView, task_list, TasksList, event_detail, guest_detail, task_detail

app_name = 'events'

urlpatterns = [
    path('', ListEventView.as_view(), name='event-list'),
    path('new/', NewEventView.as_view(), name='new-event'),
    path('<int:pk>/', DetailEventView.as_view(), name='event-detail'),
    path('<int:pk>/delete/', DeleteEventView.as_view(), name='event-delete'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='event-update'),
    path('<int:pk>/register/', RegisterView.as_view(), name='register-for-the-event'),
    path('<int:pk>/register/<int:person_id>/', RegisterRefusedGuestView.as_view(), name='register-refused-guest'),
    path('<int:pk>/cancel/', CancelView.as_view(), name='cancel-registration'),
    path('<int:pk>/cancel/<int:person_id>/', CancelRegisteredGuestView.as_view(), name='cancel-registered-guest'),
    path('<int:pk>/visited/<int:person_id>/', SetVisitedGuestView.as_view(), name='set-visited-guest'),
    path('<int:pk>/add-guest/', AddGuestView.as_view(), name='add-an-event-guest'),
    path('<int:pk>/guest-list/', DetailGuestListView.as_view(), name='guest-list'),
    path('<int:pk>/tasks/', TasksList.as_view(), name='event-tasks'),
    path('<int:pk>/api/tasks/', task_list),
    path('<int:pk>/api/event/', event_detail),
    path('<int:pk>/api/guest/', guest_detail),
    path('<int:pk>/api/task/', task_detail)
]