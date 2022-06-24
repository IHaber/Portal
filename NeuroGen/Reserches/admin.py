from django.contrib import admin
from . import models


class ResearchAdmin(admin.ModelAdmin):
    list_display = [
        'research_name',
        'research_pattern',
        'research_customer',
        'research_state']
    list_display_links = ['research_name']


admin.site.register(models.Region)
admin.site.register(models.Customer)
admin.site.register(models.Research, ResearchAdmin)
admin.site.register(models.ImageResearch)
admin.site.register(models.ImageResearchAnswer)
admin.site.register(models.VideoResearch)
admin.site.register(models.VideoResearchAnswer)

