from django.contrib import admin
from .models import PhishingAttempt


# @admin.register(PhishingAttempt)
# class PhishingAttemptAdmin(admin.ModelAdmin):
#     list_display = ['email', 'ip_address', 'country', 'city', 'user_agent_short', 'date']
#     list_filter = ['country', 'date']
#     search_fields = ['email', 'ip_address', 'country', 'city']
#     readonly_fields = ['email', 'password', 'ip_address', 'user_agent', 'country', 'city', 'latitude', 'longitude', 'date']
#
#     def user_agent_short(self, obj):
#         return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
#     user_agent_short.short_description = 'Browser'


from django.contrib import admin
from .models import PhishingAttempt


@admin.register(PhishingAttempt)
class PhishingAttemptAdmin(admin.ModelAdmin):
    list_display = ['email', 'ip_address', 'country', 'city', 'user_agent_short', 'date']
    list_filter = ['country', 'date']
    search_fields = ['email', 'ip_address', 'country', 'city']

    def user_agent_short(self, obj):
        return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
    user_agent_short.short_description = 'Browser'