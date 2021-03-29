from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Incident
from django.contrib.auth import get_user_model
import threading
from django.core.mail import EmailMessage, BadHeaderError

class EmailThread(threading.Thread):
     
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

#define run method
    def run(self):
        self.email_message.send()

UserModel = get_user_model()

@receiver(post_save, sender=Incident)
def notify_reviewer(sender, instance, created, **kwargs):
    incident = instance
    incidNum = str(incident.pk)
    incidSum = incident.incident_summary

    if created:     
        print("New Incident created")
    else:
        print("Incident " + incidNum +  " updated!")

    reviewers = UserModel.objects.filter(is_reviewer=True)
    recipients = list(i for i in UserModel.objects.filter(is_reviewer=True).values_list('email', flat=True) if bool(i))
    print(recipients)
    email_subject = ("Please review incident number: " + incidNum)
    message = ("Please review Incident.\n\nHere's the summary: " + incidSum + "\n\nSubmitted by " + incident.email)

    for reviewer in recipients:
        email = EmailMessage(email_subject, message, to=[reviewer])
        EmailThread(email).start()

  