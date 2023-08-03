from django.urls import path
from .views import NewEventView, ListEventView, DetailEventView, DeleteEventView, RegisterView, CancelView, \
    UpdateEventView, AddGuestView, DetailGuestListView

app_name = 'events'
urlpatterns = [
    path('', ListEventView.as_view(), name='event-list'),
    path('new/', NewEventView.as_view(), name='new-event'),
    path('<int:pk>/', DetailEventView.as_view(), name='event-detail'),
    path('<int:pk>/delete/', DeleteEventView.as_view(), name='event-delete'),
    path('<int:pk>/update/', UpdateEventView.as_view(), name='event-update'),
    path('<int:pk>/register/', RegisterView.as_view(), name='register-for-the-event'),
    path('<int:pk>/cancel/', CancelView.as_view(), name='cancel-registration'),
    path('<int:pk>/add-guest/', AddGuestView.as_view(), name='add-an-event-guest'),
    path('<int:pk>/guest-list/', DetailGuestListView.as_view(), name='guest-list')
]