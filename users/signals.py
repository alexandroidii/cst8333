from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
    

User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid="update_superuser")
def update_supervisor_handler(sender, instance, created, **kwargs):
    
    if hasattr(instance,'_dirty'): #prevent recursion
        return

    if created:
        instance.is_staff = True
    else:    
        if instance.is_superuser:
            instance.is_staff = True
        else:
            instance.is_staff = False

    try:
        instance._dirty = True
        instance.save()
    finally:
        del instance._dirty     #done - now remove