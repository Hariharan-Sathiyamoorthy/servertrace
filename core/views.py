from django.shortcuts import redirect,render
from .models import Server,Technician,Log
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from .forms import CreateServerForm,CreateLogForm,CreateTechnicianForm
from users.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages




# Create your views here.
# from django.http import HttpResponse

def getDashBoard(request):

    if not request.user.is_authenticated:
        return redirect('/users/login')
    servers = Server.objects.all().order_by('-created_at')[:5]
    total_servers = Server.objects.all().count()
    # get total number of technicians
    technicians = Technician.objects.all()
    total_technicians = technicians.count()
    # get total number of logs
    logs = Log.objects.filter(priority="High")
    total_logs = logs.count()
    # send data to the template
    logs_per_month = Log.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
    # create a two list  one with the month and the other with the count
    labels = ["January","February"]+[log['month'].strftime('%B') for log in logs_per_month]
    data = ["4","1"]+[log['count'] for log in logs_per_month]

    # convert the arrays to JSON
    labels_json = json.dumps(labels, cls=DjangoJSONEncoder)
    data_json = json.dumps(data, cls=DjangoJSONEncoder)
    # print(months,counts)
    context = {
        'servers': servers,
        'technicians': technicians,
        'logs': logs,
        'labels_json': labels_json,
        'data_json': data_json,
        'total_servers': total_servers,
        'total_technicians': total_technicians,
        'total_logs': total_logs
    }
    # print(context)
    return render(request,'Dashboard/Dashboard.html',context)

def createServer(request):
    form = CreateServerForm()
    if request.method == 'POST':
        form = CreateServerForm(request.POST)
        user = UserProfile.objects.get(user=request.user)
        if form.is_valid():
            server = form.save(commit=False)
            server.save()
            server.users.set([user.id])
            return redirect('/server/get_servers')
        else:  
            print("d",form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {"form":form,'title': 'Create Instances', 'button': 'Launch Instance'}
    return render(request,'Servers/CreateServer.html',context)

def viewServer(request,id):
    server = get_object_or_404(Server, id=id)
    logstoServer = Log.objects.filter(server=server.id).count()
    context = {
        'server': server,
        'logstoServer': logstoServer
        
    }
    return render(request,'Servers/ViewServer.html',context)

def deleteServer(request,id):
    server = get_object_or_404(Server, id=id)
    server.delete()
    return redirect('/server/get_servers')

def getServers(request):
    servers = Server.objects.all()
    context = {
        'servers': servers
    }
    return render(request,'Servers/GetServers.html',context)

def updateServer(request,id):
    server = get_object_or_404(Server, id=id)
    if request.method == 'POST':
        form = CreateServerForm(request.POST, instance=server)
        user = UserProfile.objects.get(user=request.user)
        if form.is_valid():
            server = form.save(commit=False)
            server.save()
            server.users.set([user.id])
            return redirect('/server/get_servers')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = CreateServerForm(instance=server)
    context = { 'form': form,'title': 'Update Instance', 'button': 'Update Instance'}
    return render(request,'Servers/CreateServer.html',context)  

def getLogs(request):
    logs = Log.objects.all()
    context = {
        'logs': logs
    }
    return render(request,'Logs/GetLogs.html',context)

def createLog(request):
    user = UserProfile.objects.get(user=request.user)
    form = CreateLogForm(isTech=user.is_techie,logStatus="Open")
    if request.method == 'POST':
        form = CreateLogForm(request.POST,isTech=user.is_techie,logStatus="Open")
        if form.is_valid():
            log = form.save(commit=False)
            log.created_by = user
            log.save()
            return redirect('/server/get_logs')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    context = {"form":form,'title': 'Create Log', 'button': 'Create Log'}  
    return render(request,'Logs/CreateLog.html',context)

def editLog(request,id):
    user = UserProfile.objects.get(user=request.user)

    form = CreateLogForm()
    log = get_object_or_404(Log, id=id)
    if request.method == 'POST':
        form = CreateLogForm(request.POST, instance=log,isTech=user.is_techie,logStatus=log.status)
        if form.is_valid():
            log = form.save(commit=False)
            log.modified_by = user
            log.save()
            return redirect('/server/get_logs')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = CreateLogForm(instance=log,isTech=user.is_techie,logStatus=log.status)
    context = { 'form': form,'title': 'Update Log', 'button': 'Update Log'}
    return render(request,'Logs/CreateLog.html',context)


def deleteLog(request,id):
    log = get_object_or_404(Log, id=id)
    if request.user != log.created_by.user:
        messages.error(request, "You are not allowed to delete this log")
    else:
        log.delete()
    return redirect('/server/get_logs')

def getTechnicians(request):
    techs = Technician.objects.all()
    context = {
        'techs': techs
    }
    return render(request,'Technicians/GetTechnicians.html',context)



def editTechnician(request,id):
    tech = get_object_or_404(Technician, id=id)
    if request.method == 'POST':
        form = CreateTechnicianForm(request.POST, instance=tech)
        if form.is_valid():
            tech = form.save(commit=False)
            tech.save()
            return redirect('/server/get_technicians')
        else:
            print(form.errors)
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
    else:
        form = CreateTechnicianForm(instance=tech)
    context = { 'form': form}
    return render(request,'Technicians/EditTechnician.html',context)

def deleteTechnician(request,id):
    tech = get_object_or_404(Technician, id=id)
    tech.delete()
    return redirect('/server/get_technicians')



