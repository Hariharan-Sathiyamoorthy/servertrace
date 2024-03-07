from django import forms
from django.contrib.auth.models import User

from .models import Server,Technician,Log
class CreateServerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Server Name"}), required=True)
    ip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "IP Address"}), required=True)
    port = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Port"}), required=True)
    instance_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Instance ID"}), required=True)
    instance_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Instance Type"}), required=True)
    stotage = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Storage"}), required=True)
    # users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=True)

    class Meta:
        model = Server
        fields = ['name', 'ip', 'port', 'instance_id', 'instance_type', 'stotage']

class CreateLogForm(forms.ModelForm):
    server = forms.ModelChoiceField(queryset=Server.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    log = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',"placeholder": "Log"}), required=True)
    priority = forms.CharField(widget=forms.Select(attrs={'class': 'form-control'},choices=(("High","High"),("Low","Low"),("Medium","Medium"))),required=True)
    technician = forms.ModelChoiceField(queryset=Technician.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = Log
        fields = ['server','log', 'priority', 'technician']