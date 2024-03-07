from django.shortcuts import redirect,render
from .models import Server,Technician,Log
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json
from .forms import CreateServerForm,CreateLogForm
from users.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.models import User



# Create your views here.
# from django.http import HttpResponse

def getDashBoard(request):

    # get total number of servers
    servers = Server.objects.all()
    total_servers = servers.count()
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
    context = {"form":form}
    return render(request,'Servers/CreateServer.html',context)

def viewServer(request):
    return render(request,'Servers/ViewServer.html')

def deleteServer(request):
    return render(request,'Servers/DeleteServer.html')

def getServers(request):
    servers = Server.objects.all()
    context = {
        'servers': servers
    }
    return render(request,'Servers/GetServers.html',context)

def getAServer(request):
    return render(request,'Servers/GetAServer.html')

def getLogs(request):
    logs = Log.objects.all()
    context = {
        'logs': logs
    }
    return render(request,'Logs/GetLogs.html',context)

def createLog(request):
    return render(request,'Logs/CreateLog.html')

def editLog(request):
    return render(request,'Logs/EditLog.html')

def deleteLog(request):
    return render(request,'Logs/DeleteLog.html')

def getTechnicians(request):
    techs = Technician.objects.all()
    context = {
        'techs': techs
    }
    return render(request,'Technicians/GetTechnicians.html',context)

def createTechnician(request):
    return render(request,'Technicians/CreateTechnician.html')

def editTechnician(request):
    return render(request,'Technicians/EditTechnician.html')

def deleteTechnician(request):
    return render(request,'Technicians/DeleteTechnician.html')



