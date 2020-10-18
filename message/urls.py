from django.conf.urls import url
from . import views

app_name = "message"

urlpatterns = [
    url(
        r"file/upload/$",
        views.file_upload,
        name="file_upload",
    ),
]
