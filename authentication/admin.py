from django.contrib import admin
from .models import User


# Register your models here.
admin.site.register(User)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)