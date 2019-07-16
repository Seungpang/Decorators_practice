from django.contrib import admin
from .models import BoardPermission
# Register your models here.

class BoardPermissionAdmin(admin.ModelAdmin):
    list_display = ('permission_type', 'permission_level')


admin.site.register(BoardPermission, BoardPermissionAdmin)
