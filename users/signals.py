from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Users as user
    

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid="update_superuser")
def update_supervisor_handler(sender, instance, created, **kwargs):
    
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