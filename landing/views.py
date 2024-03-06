from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.shortcuts import render




# landing page
def laodLandingPage(request):
    return render(request, "index.html")
