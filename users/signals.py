from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Users as user


"""
Authors: Robert Lange and Alexander Riccio
Course: CST8333
Date: 2019-12-19

Django signals are utilized with the users application to handle all post_save activities. That includes all db related commits or save 
activities relating to the Users model. 

The instance of the Users model is tested against:
1) If the user is added - they are done so and added to the default group submitter. All users are submitters by default since when they 
   register then cannot submit a CCS Case unless they belong to the submitters group.

2) Should a user become a superuser, the signal is triggered which sets them to superuser. Note that the method to do so encompasses
   setting them to hidden is_staff boolean entity since by Django design, it is required to be is_staff.  The default PermissionMixin 
   includes is_superuser in the auth.models framework.

3) Should a user superuser status get change to no longer be superuser, the signal is triggered which clears them as superuser 
   and clears is_staff.  The default PermissionMixin permissions includes is_superuser in the auth.models framework. This is why
   is is not specifically defined in the users model.

Created: Handles new user signal entity activities added to the model

Updated: Handles modified or updated entity activities within the model

"""   

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid="update_superuser_submitter")
def update_supervisor_submitter_handler(sender, instance, created, **kwargs):
    
    if hasattr(instance,'_dirty'): #prevent recursion
        return

    if not instance.groups.filter(name='submitter').exists():
            # Add submitter group to all users.
            submitter_group = Group.objects.get(name='submitter')       
            instance.groups.add(submitter_group)

    if created:
        instance.is_staff = True
    else:    
        if instance.is_superuser:
            instance.is_staff = True
        else:
            instance.is_staff = False

    if instance.is_reviewer:
        if not instance.groups.filter(name='reviewer').exists():
            try:
                # If user is selected as reviewer, set their group to reviewer
                submitter_group = Group.objects.get(name='reviewer')       
                instance.groups.add(submitter_group)
            except Group.DoesNotExist:
                instance.is_reviewer = False
    else:
            if instance.groups.filter(name='reviewer').exists():
                # If user is removed as reviewer and the group exists, remove from group
                submitter_group = Group.objects.get(name='reviewer')       
                instance.groups.remove(submitter_group)

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty     #done - now remove