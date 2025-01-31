from django.contrib import admin
from .models import FAQ


class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "get_languages")

    def get_languages(self, obj):
        return ", ".join(obj.translations.keys()
                         ) if obj.translations else "No translations"
    get_languages.short_description = "Available Translations"


admin.site.register(FAQ, FAQAdmin)
