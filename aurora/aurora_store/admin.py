from django.contrib import admin
from aurora_store.models import *
from aurora_store.models import Profile
# Register Profile model
admin.site.register(Profile)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.detail import DetailView
from aurora_store.models import Order


