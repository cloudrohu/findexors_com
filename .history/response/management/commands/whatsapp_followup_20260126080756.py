from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from response.models import Response
from response.whatsapp import send_whatsapp


class Command(BaseCommand):
    help = "Send WhatsApp auto follow-ups"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # 5 minute follow-up
        leads_5min = Response.objects.filter(
            whatsapp_welcome_sent=True,
            whatsapp_followup_1_sent=False,
            create_at__lte=now - timedelta(minutes=5)
        )

        for lead in leads_5min:
            name = lead.contact_persone or "Sir/Madam"
            msg = f"""Hello {name},

We have received your response from our online advertisement.

Please share:
1) Business Type
2) City
3) Requirement (Website / Ads)
"""
            send_whatsapp(lead.contact_no, msg)
            lead.whatsapp_followup_1_sent = True
            lead.save(update_fields=["whatsapp_followup_1_sent"])

        # 24 hour follow-up
        leads_24hr = Response.objects.filter(
            whatsapp_followup_1_sent=True,
            whatsapp_followup_2_sent=False,
            create_at__lte=now - timedelta(hours=24)
        )

        for lead in leads_24hr:
            name = lead.contact_persone or "Sir/Madam"
            msg = f"""Hello {name},

We tried to connect regarding your enquiry.
Reply YES if you are still interested.
"""
            send_whatsapp(lead.contact_no, msg)
            lead.whatsapp_followup_2_sent = True
            lead.save(update_fields=["whatsapp_followup_2_sent"])
