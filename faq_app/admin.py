from django.contrib import admin
from .models import FAQ
import json


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "get_languages")

    def get_languages(self, obj):
        try:
            translations = json.loads(obj.translations) if isinstance(obj.translations, str) else obj.translations
            return ", ".join(translations.keys()) if translations else "No translations"
        except json.JSONDecodeError:
            return "Invalid JSON"
    
    get_languages.short_description = "Available Translations"

admin.site.register(FAQ, FAQAdmin)
