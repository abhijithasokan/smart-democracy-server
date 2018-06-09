from django.contrib import admin

# Register your models here.
from . models import User,MLA,Constituency,Issue,Solution

admin.site.register(User)
admin.site.register(MLA)
admin.site.register(Constituency)
admin.site.register(Issue)
admin.site.register(Solution)