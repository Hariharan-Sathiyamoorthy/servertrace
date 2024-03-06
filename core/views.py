from django.shortcuts import render
from .models import Server,Technician,Log
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json



# Create your views here.
# from django.http import HttpResponse

def getDashBoard(request):

    # get total number of servers
    servers = Server.objects.all()
    # get total number of technicians
    technicians = Technician.objects.all()
    # get total number of logs
    logs = Log.objects.filter(priority="High")
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
    }
    # print(context)
    return render(request,'Dashboard/Dashboard.html',context)
