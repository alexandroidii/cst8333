from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Scenario
from django.contrib.auth import get_user_model
import threading
from django.core.mail import EmailMessage, BadHeaderError
from django.conf import settings


class EmailThread(threading.Thread):
     
    def __init__(self, email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

#define run method
    def run(self):
        self.email_message.send()

UserModel = get_user_model()


# This will send an email to all reviewers when a scenario is saved to the database.
# The email includes a link to the scenario that will prompt for the login.
@receiver(post_save, sender=Scenario)
def notify_reviewer(sender, instance, created, **kwargs):
    scenario = instance
    scenNum = str(scenario.pk)
    scenSum = scenario.scenario_summary
    current_site = get_current_site(request=None)
    domain = current_site.domain
    link = domain + '/rlcs/scenarios/' + scenNum + "?login=true"
    if settings.DEBUG:
        if created:     
            print("New Scenario created")
        else:
            print("Scenario " + scenNum +  " updated!")

    reviewers = UserModel.objects.filter(is_reviewer=True)
    recipients = list(i for i in UserModel.objects.filter(is_reviewer=True).values_list('email', flat=True) if bool(i))
    if settings.DEBUG:
        print(recipients)
        
    email_subject = ("Please review scenario number: " + scenNum)
    message = ("Please review Scenario at: http://" + link + "\n\nHere's the summary: '" + scenSum + "'" +  "\n\nSubmitted by: " + scenario.email)

    for reviewer in recipients:
        email = EmailMessage(email_subject, message, to=[reviewer])
        EmailThread(email).start()

  