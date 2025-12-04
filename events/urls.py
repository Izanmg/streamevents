from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list_view, name='list'),
    path('my-events/', views.my_events_view, name='my_events'),
    path('create/', views.event_create_view, name='create'),
    path('<int:pk>/', views.event_detail_view, name='detail'),
    path('<int:pk>/edit/', views.event_update_view, name='edit'),
]
