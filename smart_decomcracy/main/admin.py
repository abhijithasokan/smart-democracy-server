from django.contrib import admin

# Register your models here.
from . models import User,MLA,Constituency

admin.site.register(User)
admin.site.register(MLA)
admin.site.register(Constituency)