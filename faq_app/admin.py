from django.contrib import admin  # Importing Django's admin module to register models in the admin interface
from .models import FAQ  # Importing the FAQ model from the current app's models
import json  # Importing JSON module to handle JSON data


# Defining an admin class for the FAQ model
class FAQAdmin(admin.ModelAdmin):
    # Configuring the admin panel to display the 'question' and available translations
    list_display = ("question", "get_languages")

    # Custom method to retrieve the available translation languages
    def get_languages(self, obj):
        try:
            # Ensure that 'translations' is parsed correctly from a JSON string if needed
            translations = json.loads(obj.translations) if isinstance(obj.translations, str) else obj.translations
            # Return a comma-separated list of available translation languages, or a default message
            return ", ".join(translations.keys()) if translations else "No translations"
        except json.JSONDecodeError:
            # Handle cases where 'translations' contains invalid JSON
            return "Invalid JSON"

    # Set a user-friendly name for the column in the Django admin interface
    get_languages.short_description = "Available Translations"


# Registering the FAQ model with the Django admin site using the FAQAdmin class
admin.site.register(FAQ, FAQAdmin)
