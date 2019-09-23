from django.contrib import admin
from orderable.admin import OrderableTabularInline

from . import models


class InterestInline(OrderableTabularInline):
    model = models.Interest


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Interest Category"""
    inlines = [InterestInline]
