from django.contrib import admin
from django.contrib.auth.models import User

from auth_user.models import Role, UserHasRole

# Register your models here.
admin.site.register(Role)
admin.site.register(UserHasRole)