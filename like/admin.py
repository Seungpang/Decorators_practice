from django.contrib import admin
from .models import Like

# Register your models here.
class LikeAdmin(admin.ModelAdmin):
    list_display = ('writer', 'board')


admin.site.register(Like, LikeAdmin)
