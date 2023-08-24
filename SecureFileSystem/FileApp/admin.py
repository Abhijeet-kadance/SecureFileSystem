from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Material)
class AdminDocument(admin.ModelAdmin):
    list_display = ('id', 'Material_Title', "Material_Contributor", 'Material_Published_Status', 'Materail_Created_Date')
    list_display_links = ('id', 'Material_Title', "Material_Contributor" )
    search_fields = ('Material_Title',)
    ordering = ('id','Material_Title')
    list_per_page: int = 20
    save_on_top = True