from django.contrib import admin
from .models import User, Schema, Column, DataSet

# Register your models here.
admin.site.register(User)
admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(DataSet)

