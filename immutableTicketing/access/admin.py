from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from access.models import web3User, Event, Gate, EventRequest, SignUpRequest

class web3UserInline(admin.StackedInline):
    model = web3User
    can_delete = False
    verbose_name_plural = 'Web3User'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (web3UserInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


admin.site.register(Event)
admin.site.register(Gate)
admin.site.register(EventRequest)
admin.site.register(SignUpRequest)