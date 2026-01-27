# response/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Response
from .whatsapp import send_whatsapp_welcome


@receiver(post_save, sender=Response)
def response_created(sender, instance, created, **kwargs):
    if created:
        # Only Ads / Website leads
        if instance.lead_source in ["instagram", "facebook", "google", "website"]:
            if instance.contact_no and not instance.whatsapp_welcome_sent:
                send_whatsapp_welcome(instance)
                instance.whatsapp_welcome_sent = True
                instance.save(update_fields=["whatsapp_welcome_sent"])
