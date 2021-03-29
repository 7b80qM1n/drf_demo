from django.contrib import admin
from . import models
# Register your models here.

admin.AdminSite.site_header = 'Django 后台'

# admin.AdminSite.site_title = '123'
admin.site.register(models.User)