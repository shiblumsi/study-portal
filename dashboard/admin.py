from django.contrib import admin
from .models import *

admin.site.register(Note)
admin.site.register(Homework)
admin.site.register(Todo)