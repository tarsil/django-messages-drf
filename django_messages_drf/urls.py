from django.urls import path

from . import views

app_name = "django_messages_drf"

urlpatterns = [
    path('inbox/', views.InboxListApiView.as_view(), name='inbox'),
    path('threads/', views.SentboxListApiView.as_view(), name='sentbox'),
    path('threads/<uuid>/messages/', views.ThreadListApiView.as_view(), name='thread'),
    path('threads/<user_id>', views.ThreadCRUDApiView.as_view(), name='thread-create'),
    path('threads/<user_id>/<uuid>', views.ThreadCRUDApiView.as_view(), name='thread-send'),
    path('threads/<user_id>/<thread_uuid>', views.EditMessageApiView.as_view(), name='message-edit'),
    path('threads/<uuid>', views.ThreadCRUDApiView.as_view(), name='thread-delete'),
]
