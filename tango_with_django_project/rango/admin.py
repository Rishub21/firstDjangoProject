from django.contrib import admin
# Register your models here.
from rango.models import Category, Page, UserProfile, celeryResponse

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),'totalups': ('likes',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(celeryResponse)




#class PageAdmin(admin.ModelAdmin):
#	list_display = ("title", "category", "url")
