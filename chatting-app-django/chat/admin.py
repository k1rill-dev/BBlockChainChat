from django.contrib import admin
from chat.models import Message
from django.core.exceptions import ObjectDoesNotExist

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'sender', 'receiver')
    list_display_links = ('message', 'sender', 'receiver')
    list_filter = ('sender', 'receiver')
    search_fields = ('message', )


admin.site.register(Message, MessageAdmin)