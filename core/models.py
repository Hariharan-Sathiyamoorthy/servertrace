from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserProfile



# Server model
#vpc group
#Appliction OS and Image
#allow ssh trafic
class Server(models.Model):
    name = models.CharField(max_length=100)
    application_image = models.CharField(max_length=100, default="Ubuntu")
    ip = models.GenericIPAddressField()
    network = models.CharField(max_length=100, default="VPC-aaabbbcc")
    instance_id = models.CharField(max_length=100)
    instance_type = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)
    allow_ssh_trafic = models.BooleanField(default=False)
    instance_state = models.CharField(max_length=100, default="Running")

    users = models.ManyToManyField(UserProfile)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-updated_at']

    def __str__(self):
        return self.name
# Update the Technician model to include a reference to the UserProfile model
@receiver(post_save, sender=UserProfile)
def create_technician(sender, instance, created, **kwargs):
    if created and instance.is_techie:
        Technician.objects.create(name=instance)

#Technician model
class Technician(models.Model):
    name = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    issues_resolved = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.name.user.username


# Log model
class Log(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    log = models.TextField()
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name="created_logs")
    modified_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="modified_logs", null=True, blank=True)
    priorities = (("High","High"),("Low","Low"),("Medium","Medium"))
    priority = models.CharField(max_length=20, choices=priorities,default="Low")
    STATUS_CHOICES = (('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-updated_at', '-updated_at']

    def __str__(self):
        return self.log