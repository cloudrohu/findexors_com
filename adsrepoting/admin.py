from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Campaign


# Resource class (Import/Export ke liye)
class CampaignResource(resources.ModelResource):
    class Meta:
        model = Campaign
        fields = (
            "id",
            "title",
            "date",
            "status",
            "messaging_conversations_started",
            "spent",
        )  # thumbnail export karne ki zarurat nahi


@admin.register(Campaign)
class CampaignAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = CampaignResource

    list_display = (
        "title",
        "date",
        "status",
        "messaging_conversations_started",
        "spent",
        "cost_per_conversation",
        "thumbnail_tag",   # 👈 Thumbnail preview
    )
    readonly_fields = ("cost_per_conversation", "thumbnail_tag")  # form me bhi image preview

    list_filter = ("status", "date")
    search_fields = ("title",)
    list_per_page = 20

    def thumbnail_tag(self, obj):
        if obj.thumbnail and hasattr(obj.thumbnail, "url"):
            return format_html(
                '<img src="{}" style="width:60px; height:60px; object-fit:cover; border-radius:6px;" />',
                obj.thumbnail.url
            )
        return "—"
    thumbnail_tag.short_description = "Thumbnail"

    def cost_per_conversation(self, obj):
        try:
            if obj.messaging_conversations_started and obj.spent:
                return round(obj.spent / obj.messaging_conversations_started, 2)
        except ZeroDivisionError:
            return "—"
        return "—"
    cost_per_conversation.short_description = "Cost per Conversation"
