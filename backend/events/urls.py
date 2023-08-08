from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewEventView, ListEventView, DetailEventView, DeleteEventView, RegisterView, CancelView, \
    UpdateEventView, AddGuestView, DetailGuestListView, RegisterRefusedGuestView, CancelRegisteredGuestView, \
    SetVisitedGuestView, TasksList, TaskViewSet, EventViewSet, GuestViewSet

app_name = 'events'

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
router.register(r'events', EventViewSet)
router.register(r'guests', GuestViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path('', ListEventView.as_view(), name='events'),
    path('new/', NewEventView.as_view(), name='new-event'),
    path('<int:pk>/', DetailEventView.as_view(), name='event'),
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

]