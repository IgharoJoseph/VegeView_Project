from django.contrib import admin
from .models import Vegetable, PestDisease


@admin.register(Vegetable)
class VegetableAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'scientific_name', 'growing_duration_days', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'scientific_name', 'description')


@admin.register(PestDisease)
class PestDiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'problem_type', 'causal_agent', 'severity', 'created_at')
    list_filter = ('problem_type', 'severity', 'affected_vegetables')
    search_fields = ('name', 'causal_agent', 'symptoms')
    filter_horizontal = ('affected_vegetables',)
