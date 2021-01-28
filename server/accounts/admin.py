from django.contrib import admin

from accounts.models import User, Person

admin.site.register(User)
admin.site.register(Person)
