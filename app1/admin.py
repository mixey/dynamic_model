from django.contrib import admin
from app1.models import DynamicModels

models = DynamicModels().store

admin.site.register([model for model in models.values()])
