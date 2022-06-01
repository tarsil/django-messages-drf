from django.urls import include, path

urlpatterns = [
    path("", include("django_messages_drf.urls", namespace="django_messages_drf")),
]
