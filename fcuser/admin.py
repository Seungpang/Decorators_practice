from django.contrib import admin
from .models import Fcuser, FcuserValidation

# Register your models here.


class FcuserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')


admin.site.register(Fcuser, FcuserAdmin)
admin.site.register(FcuserValidation)