from django.shortcuts import render
from .forms import FileUploadForm
from message.file_parser import BulkAirtimeUpload

# Create your views here.


def file_upload(request):
    if request.method == "GET":
        form = FileUploadForm()
        return render(request, "message/file_upload.html", {"form": form})
    if request.method == "POST":
        error_list = None
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            bulk_sms = BulkAirtimeUpload(instance.id)
            bulk_sms.trigger_sms()
            if bulk_sms.errors():
                error_list = bulk_sms.error
        return render(
            request,
            "message/file_upload.html",
            {"form": form, "error_list": error_list},
        )
