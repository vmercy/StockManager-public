from django.contrib import admin

from .models import Category, Component, Compartment

admin.site.register(Category)
admin.site.register(Component)
admin.site.register(Compartment)