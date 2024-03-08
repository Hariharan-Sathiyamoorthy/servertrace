from django import forms
from django.contrib.auth.models import User
from faker import Faker  

from .models import Server,Technician,Log
class CreateServerForm(forms.ModelForm):
    faker = Faker() 


    
    name = forms.RegexField(regex=r'^[a-zA-Z]*$',widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Server Name"}), required=True)
    application_images = [("Ubuntu","Ubuntu"),("CentOS","CentOS"),("Red Hat","Red Hat"),("Windows","Windows")]
    application_image = forms.CharField(label='Application Image',widget=forms.Select(attrs={'class': 'form-select'},choices=application_images),required=True)
    allow_ssh_trafic = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)
    ip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "IP Address"}), required=True)
    network = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Port"}), required=True)
    instance_id = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Instance ID"}), required=True)

    instance_types = [("t2.micro","t2.micro"),("t2.small","t2.small"),("t2.medium","t2.medium"),("t2.large","t2.large"),("t2.xlarge","t2.xlarge")]
    instance_type = forms.CharField(widget=forms.Select(attrs={'class': 'form-select'},choices=instance_types),required=True)
    # instance_type = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Instance Type"}), required=True)
    storage = forms.IntegerField(label='Storage in GB',min_value=8, max_value=100,widget=forms.TextInput(attrs={'class': 'form-control',"placeholder": "Storage"}), required=True)
    # users = forms.ModelMultipleChoiceField(queryset=User.objects.all(),widget=forms.SelectMultiple(attrs={'class': 'form-control'}), required=True)
    def __init__(self, *args, **kwargs):
        super(CreateServerForm, self).__init__(*args, **kwargs)
        self.fields['ip'].initial = self.faker.ipv4()
        self.fields['network'].initial = 'vpc-'+self.faker.uuid4()[:12]
        self.fields['instance_id'].initial = self.faker.uuid4()[:18]

    class Meta:
        model = Server
        fields = ['name', 'ip', 'network', 'instance_id', 'instance_type', 'storage',"application_image","allow_ssh_trafic"]

class CreateLogForm(forms.ModelForm):
    server = forms.ModelChoiceField(queryset=Server.objects.all(),widget=forms.Select(attrs={'class': 'form-select'}), required=True)
    log = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',"placeholder": "Log"}), required=True)
    priority = forms.CharField(widget=forms.Select(attrs={'class': 'form-select'},choices=(("High","High"),("Low","Low"),("Medium","Medium"))),required=True)
    technician = forms.ModelChoiceField(queryset=Technician.objects.filter(is_active=True),widget=forms.Select(attrs={'class': 'form-select'}), required=True)
    status = forms.CharField(widget=forms.Select(attrs={'class': 'form-select'},choices=(('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'))),required=True)
    def __init__(self, *args, **kwargs):
        self.isTech = kwargs.pop('isTech', None)
        logStatus = kwargs.pop('logStatus', None)
        super(CreateLogForm, self).__init__(*args, **kwargs)

        if self.isTech == False:
            self.fields['status'].initial = logStatus
            self.fields['status'].widget.attrs['disabled'] = 'disabled'
            self.fields['status'].help_text = "Status can only be updated by a technician"
    def clean(self):
        cleaned_data = super().clean()
        if self.isTech == False and 'status' in self.errors:
            del self.errors['status']
        return cleaned_data
    class Meta:
        model = Log
        fields = ['server','log', 'priority', 'technician','status']

class CreateTechnicianForm(forms.ModelForm):

    issues_resolved = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    is_active = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),required=False)
    class Meta:
        model = Technician
        fields = [ 'issues_resolved', 'is_active']