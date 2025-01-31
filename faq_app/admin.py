from django.contrib import admin
from .models import FAQ

class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "get_languages")  # Removed 'question_hi' and 'question_bn'

    def get_languages(self, obj):
        """
        Display available languages stored in the translations JSONField.
        """
        return ", ".join(obj.translations.keys()) if obj.translations else "No translations"

    get_languages.short_description = "Available Translations"

admin.site.register(FAQ, FAQAdmin)
