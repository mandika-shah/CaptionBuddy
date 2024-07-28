from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Photo,Caption



# Register your models here.
admin.site.register(Photo)
admin.site.register(Caption)