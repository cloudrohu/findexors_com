from django.contrib import admin
from .models import Staff, Response, Meeting, Followup, Comment, VoiceRecording
from rangefilter.filters import DateRangeFilter

# ===========================
#  Auto Set User Mixin
# ===========================
class AutoUserAdminMixin:
    """Automatically sets created_by / updated_by / uploaded_by in admin."""

    def save_model(self, request, obj, form, change):
        if not change or not obj.pk:
            if hasattr(obj, 'created_by') and not obj.created_by:
                obj.created_by = request.user
        if hasattr(obj, 'updated_by'):
            obj.updated_by = request.user
        if hasattr(obj, 'uploaded_by') and not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if hasattr(instance, 'created_by') and not instance.created_by:
                instance.created_by = request.user
            if hasattr(instance, 'updated_by'):
                instance.updated_by = request.user
            if hasattr(instance, 'uploaded_by') and not instance.uploaded_by:
                instance.uploaded_by = request.user
            instance.save()
        formset.save_m2m()

    def get_readonly_fields(self, request, obj=None):
        ro_fields = getattr(self, 'readonly_fields', [])
        if obj:  # Edit mode
            return ro_fields + ('created_by', 'updated_by', 'create_at', 'update_at')
        else:  # Add mode
            return ro_fields + ('create_at', 'update_at')

    def render_change_form(self, request, context, *args, **kwargs):
        form = context['adminform'].form
        if not form.initial.get('created_by'):
            form.initial['created_by'] = request.user
        if not form.initial.get('updated_by'):
            form.initial['updated_by'] = request.user
        return super().render_change_form(request, context, *args, **kwargs)


# ===========================
#  Response Info Mixin
# ===========================
class ResponseInfoMixin:
    """Show Response model info (contact, business, city) inside inline rows."""

    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else None
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else None
    response_business.short_description = "Business Name"

    def response_city(self, obj):
        return obj.response.city if obj.response else None
    response_city.short_description = "City"


# ===========================
#  Inline Models
# ===========================
class MeetingInline(ResponseInfoMixin, admin.TabularInline):
    model = Meeting
    extra = 1
    fields = ('response_contact', 'response_business', 'response_city',
              'status', 'meeting_date', 'assigned_to', 'comment')
    readonly_fields = ('response_contact', 'response_business', 'response_city')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class FollowupInline(ResponseInfoMixin, admin.TabularInline):
    model = Followup
    extra = 1
    fields = ('response_contact', 'response_business', 'response_city',
              'status', 'followup_date', 'assigned_to', 'comment')
    readonly_fields = ('response_contact', 'response_business', 'response_city')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class CommentInline(ResponseInfoMixin, admin.TabularInline):
    model = Comment
    extra = 1
    fields = ('response_contact', 'response_business', 'response_city', 'comment')
    readonly_fields = ('response_contact', 'response_business', 'response_city')
    exclude = ('created_by', 'updated_by', 'create_at', 'update_at')
    show_change_link = True


class VoiceRecordingInline(ResponseInfoMixin, admin.TabularInline):
    model = VoiceRecording
    extra = 1
    fields = ('response_contact', 'response_business', 'response_city', 'file', 'note')
    readonly_fields = ('response_contact', 'response_business', 'response_city')
    exclude = ('uploaded_by', 'uploaded_at')
    show_change_link = True


# ===========================
#  Response Admin
# ===========================
@admin.register(Response)
class ResponseAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    ...
    list_display = (
        'get_mr_id', 'contact_no', 'contact_persone', 'business_name',
        'business_category', 'get_requirement_types',  # ✅ fixed here
        'status', 'city', 'locality_city', 'assigned_to',
        'create_at', 'created_by', 'update_at', 'updated_by'
    )

    def get_mr_id(self, obj):
        """Display MR + zero-padded ID."""
        return f"MR{str(obj.id).zfill(3)}"
    get_mr_id.short_description = "Response ID"  # 👈 Column header name

    def get_requirement_types(self, obj):
        """Display comma-separated requirement types."""
        return ", ".join([str(r) for r in obj.requirement_types.all()])
    get_requirement_types.short_description = "Requirement Types"
    list_filter = ('status', 'city', 'assigned_to')
    search_fields = ('contact_no', 'business_name', 'contact_persone')
    readonly_fields = ('create_at', 'update_at')

    fieldsets = (
        ('📞 Contact Information', {
            'fields': ('contact_no', 'contact_persone', 'assigned_to', 'status')
        }),
        ('🏢 Business Details', {
            'fields': (
                'business_name', 'business_category', 'requirement_types',
                'city', 'locality_city'
            )
        }),
        ('🕓 Audit Trail', {
            'fields': ('created_by', 'updated_by', 'create_at', 'update_at')
        }),
    )

    tab_fieldsets = (
        ('📞 Contact Information', 'Contact Information'),
        ('🏢 Business Details', 'Business Details'),
        ('🕓 Audit Trail', 'Audit Trail'),
    )

    tab_inlines = [
        ('🗓 Meetings', MeetingInline),
        ('🔁 Followups', FollowupInline),
        ('💬 Comments', CommentInline),
        ('🎤 Voice Recordings', VoiceRecordingInline),
    ]

    inlines = [MeetingInline, FollowupInline, CommentInline, VoiceRecordingInline]

    tab_icons = {
        '📞 Contact Information': 'fas fa-phone',
        '🏢 Business Details': 'fas fa-building',
        '🕓 Audit Trail': 'fas fa-clock',
        '🗓 Meetings': 'fas fa-calendar-check',
        '🔁 Followups': 'fas fa-sync',
        '💬 Comments': 'fas fa-comments',
        '🎤 Voice Recordings': 'fas fa-microphone'
    }

from django.contrib.admin import DateFieldListFilter

@admin.register(Meeting)
class MeetingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'response','response_business',
        'response_category',  'response_locality','response_city', 'response_requirement_types',
        'status', 'meeting_date', 'assigned_to', 'comment', 'create_at'
    )
    list_filter = (
        'status',
        'assigned_to',
        ('meeting_date', DateRangeFilter),  # ✅ Custom date range picker
        ('response__city', admin.RelatedOnlyFieldListFilter),
        ('response__locality_city', admin.RelatedOnlyFieldListFilter),
        ('response__business_category', admin.RelatedOnlyFieldListFilter),
    )

    
    search_fields = (
        'response__business_name',
        'response__locality_city',

        'response__city',
        'response__requirement_types__name',
        'comment'
    )
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')
    list_per_page = 25
    ordering = ('-create_at',)

    # ====== Related Response Fields ======
    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else "-"
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else "-"
    response_business.short_description = "Business"

    def response_category(self, obj):
        return obj.response.business_category if obj.response else "-"
    response_category.short_description = "Category"

    def response_city(self, obj):
        return obj.response.city if obj.response else "-"
    response_city.short_description = "City"

    def response_locality(self, obj):
        return obj.response.locality_city if obj.response else "-"
    response_locality.short_description = "Locality"

    def response_requirement_types(self, obj):
        if obj.response and obj.response.requirement_types.exists():
            return ", ".join([r.name for r in obj.response.requirement_types.all()])
        return "-"
    response_requirement_types.short_description = "Requirement Type(s)"


@admin.register(Followup)
class FollowupAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'response', 'response_business',
        'response_category', 'response_city', 'response_locality', 'response_requirement_types',
        'status', 'followup_date', 'assigned_to', 'comment', 'create_at'
    )
    
    list_filter = (
        'status',
        'assigned_to',
        ('followup_date', DateRangeFilter),  # ✅ Custom date range picker
        ('response__city', admin.RelatedOnlyFieldListFilter),
        ('response__locality_city', admin.RelatedOnlyFieldListFilter),
        ('response__business_category', admin.RelatedOnlyFieldListFilter),
    )

    search_fields = (
        'response__business_name',
        'response__contact_no',
        'response__city',
        'response__locality_city',
        'response__requirement_types__name',
        'comment'
    )
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')
    list_per_page = 25
    ordering = ('-create_at',)

    # ====== Related Response Fields ======
    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else "-"
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else "-"
    response_business.short_description = "Business"

    def response_category(self, obj):
        return obj.response.business_category if obj.response else "-"
    response_category.short_description = "Category"

    def response_city(self, obj):
        return obj.response.city if obj.response else "-"
    response_city.short_description = "City"

    def response_locality(self, obj):
        return obj.response.locality_city if obj.response else "-"
    response_locality.short_description = "Locality"

    def response_requirement_types(self, obj):
        if obj.response and obj.response.requirement_types.exists():
            return ", ".join([r.name for r in obj.response.requirement_types.all()])
        return "-"
    response_requirement_types.short_description = "Requirement Type(s)"

@admin.register(Comment)
class CommentAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'response', 'response_contact', 'response_business',
        'comment', 'created_by', 'create_at'
    )
    search_fields = ('response__contact_no', 'comment')
    readonly_fields = ('create_at', 'update_at', 'created_by', 'updated_by')

    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else None
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else None
    response_business.short_description = "Business"


@admin.register(VoiceRecording)
class VoiceRecordingAdmin(AutoUserAdminMixin, admin.ModelAdmin):
    list_display = (
        'id', 'response', 'response_contact', 'response_business',
        'note', 'uploaded_by', 'uploaded_at'
    )
    search_fields = ('response__contact_no', 'note')
    readonly_fields = ('uploaded_by', 'uploaded_at')

    def response_contact(self, obj):
        return obj.response.contact_no if obj.response else None
    response_contact.short_description = "Contact No"

    def response_business(self, obj):
        return obj.response.business_name if obj.response else None
    response_business.short_description = "Business"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
