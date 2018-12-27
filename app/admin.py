from django.contrib import admin

# Register your models here.
from app.models import Member, Notice

admin.site.register(Member)
admin.site.register(Notice)