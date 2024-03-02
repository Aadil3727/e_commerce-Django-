from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Auth_user)
admin.site.register(models.Image_slider)
admin.site.register(models.Contact_Us)

