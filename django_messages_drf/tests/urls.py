from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("django_messages_drf.urls", namespace="django_messages_drf")),
]
