from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

def home(request):
    context_ = {
        "title": "Home",
        "Home": "active",
    }
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)
    # return render(request, "cuboidapp/Home.html", context_)

def about(request):
    context_ = {
        "title": "About",
        "About": "active",
    }
    return HttpResponse(status=201)