from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import *

class DepartmentImageInline(admin.TabularInline):
    model = DepartmentImage
    max_num = 5
    min_num = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [DepartmentImageInline, ]

admin.site.register(Category)
admin.site.register(Problem)
admin.site.register(Reply)
admin.site.register(Comment)

admin.site.register(Likes)
admin.site.register(Rating)
