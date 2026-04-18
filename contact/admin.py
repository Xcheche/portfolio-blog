from django.contrib import admin
from contact.models import Contact
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject')


admin.site.register(Contact, ContactAdmin)    