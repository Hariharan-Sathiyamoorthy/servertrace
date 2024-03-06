from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse

def getDashBoard(request):

    return render(request,'Dashboard/Dashboard.html')
