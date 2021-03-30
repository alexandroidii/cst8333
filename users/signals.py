from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Users

    
    # Create signal for first time login
    # https://stackoverflow.com/questions/49385582/can-i-check-if-a-user-is-logged-in-for-the-first-time-after-this-user-is-logged
    # More info on signals explained in https://youtu.be/FdVuKt_iuSI?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p

    @receiver(post_save, sender=Users)
    def update_first_login(sender, user, *args, **kwargs):
        if user.last_login is None:
            # First time this user has logged in
        kwargs['request'].session['first_login'] = True #Add first login attribute to session
    # Update the last_login value as normal
        update_last_login(sender, user, **kwargs)

    user_logged_in.disconnect(update_last_login)
    user_logged_in.connect(update_first_login)

