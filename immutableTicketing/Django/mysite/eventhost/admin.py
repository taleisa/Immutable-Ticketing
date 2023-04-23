from django.contrib import admin
from .models import web3User, Event, EventRequest, SignUpRequest

# Register your models here.
admin.site.register(web3User)
admin.site.register(Event)
admin.site.register(EventRequest)
admin.site.register(SignUpRequest)
