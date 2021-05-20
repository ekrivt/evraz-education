from django.contrib import admin
from .models import UserProfile

admin.site.register(UserProfile)

admin.site.site_header="ticket_tracker"