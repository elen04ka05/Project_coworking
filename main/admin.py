from django.contrib import admin

from .models import Workspace, QRCode, Report, Reservation

admin.site.register(Workspace)
admin.site.register(QRCode)
admin.site.register(Report)
admin.site.register(Reservation)
