from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scenario
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

@receiver(post_save, sender=Scenario)
def notify_reviewer(sender, instance, created, **kwargs):
    scenario = instance
    scenNum = str(scenario.pk)
    scenSum = scenario.scenario_summary
    print(kwargs)
    link = kwargs['domain'] + "/rlcis/scenario/" + scenNum
    if created:     
        print("New Scenario created")
    else:
        print("Scenario " + scenNum +  " updated!")

    reviewers = UserModel.objects.filter(is_reviewer=True)
    recipients = list(i for i in UserModel.objects.filter(is_reviewer=True).values_list('email', flat=True) if bool(i))
    print(recipients)
    email_subject = ("Please review scenario number: " + scenNum)
    message = ("Please review Scenario <a href='" + link + "'>#" + scenNum + "</a>.\n\nHere's the summary: " + scenSum + "\n\nSubmitted by " + scenario.email)

    for reviewer in recipients:
        email = EmailMessage(email_subject, message, to=[reviewer])
        EmailThread(email).start()

  