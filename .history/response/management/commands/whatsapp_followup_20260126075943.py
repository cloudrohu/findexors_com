from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from response.models import Response
from response.whatsapp_followup import send_whatsapp

class Command(BaseCommand):
    help = "Send WhatsApp follow-ups"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # 🔹 Follow-up after 5 minutes
        leads_5min = Response.objects.filter(
            whatsapp_welcome_sent=True,
            whatsapp_followup_1_sent=False,
            create_at__lte=now - timedelta(minutes=5)
        )

        for lead in leads_5min:
            name = lead.contact_persone or "Sir/Madam"
            msg = f"""Hello {name},

Just checking 😊  
Please share your business details so we can assist you better."""
            send_whatsapp(lead.contact_no, msg)
            lead.whatsapp_followup_1_sent = True
            lead.save(update_fields=["whatsapp_followup_1_sent"])

        # 🔹 Follow-up after 24 hours
        leads_24hr = Response.objects.filter(
            whatsapp_followup_1_sent=True,
            whatsapp_followup_2_sent=False,
            create_at__lte=now - timedelta(hours=24)
        )

        for lead in leads_24hr:
            name = lead.contact_persone or "Sir/Madam"
            msg = f"""Hello {name},

We tried to contact you regarding your enquiry.
Reply YES if you are still interested."""
            send_whatsapp(lead.contact_no, msg)
            lead.whatsapp_followup_2_sent = True
            lead.save(update_fields=["whatsapp_followup_2_sent"])
