from django.db import models

# Create your models here.
class Campaign(models.Model):
    STATUS_CHOICES = [
        ('on', 'On'),
        ('off', 'Off'),
    ]

    title = models.CharField(max_length=255)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='off')

    # User input
    messaging_conversations_started = models.PositiveIntegerField(default=0)
    spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    thumbnail = models.ImageField(upload_to="campaigns/", blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

    @property
    def cost_per_conversation(self):
        if self.messaging_conversations_started > 0:
            return round(self.spent / self.messaging_conversations_started, 2)
        return 0