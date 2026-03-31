from django.contrib import admin

from .models import User, Administrator, Visitor

admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Visitor)

