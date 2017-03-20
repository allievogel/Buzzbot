from django.contrib import admin

# Register your models here.
from .models import User, Answer


admin.site.register(User)
admin.site.register(Answer)
