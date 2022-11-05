from django.contrib import admin
from .models import PurpleUsers, Message

# Register your models here.

admin.site.register(Message)
admin.site.register(PurpleUsers)