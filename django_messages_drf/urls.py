from django.urls import path

from . import views

app_name = "django_messages_drf"

urlpatterns = [
    path('inbox/', views.InboxListApiView.as_view(), name='inbox'),
    path('message/thread/<uuid>/', views.ThreadListApiView.as_view(), name='thread'),
    path('message/thread/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-create'),
    path('message/thread/<uuid>/<user_id>/send/', views.ThreadCRUDApiView.as_view(), name='thread-send'),
    path('message/thread/<user_id>/<thread_id>/edit/', views.EditMessageApiView.as_view(), name='message-edit'),
    path('thread/<uuid>/delete', views.ThreadCRUDApiView.as_view(), name='thread-delete'),
]
