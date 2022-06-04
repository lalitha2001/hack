from django.contrib import admin
from .models import admin_db, user_db

# Register your models here.
admin.site.register(user_db)
admin.site.register(admin_db)
 