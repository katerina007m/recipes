from importlib.resources import contents

from django.core.files.storage import FileSystemStorage
from django.db.models.expressions import result
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from .forms import UserBioForm

# Create your views here.

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm(),
    }
    return render(request, "requestdataapp/user-bio-form.html", context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()        #Новый экземпляр
        filename = fs.save(myfile.name, myfile)
        print("saved file", filename)

    return render(request, "requestdataapp/file-upload.html")