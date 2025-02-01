from django.db import models  # Importing Django's ORM module to define database models
from ckeditor.fields import RichTextField  # Importing RichTextField for rich-text support in answers
import asyncio  # Importing asyncio for handling asynchronous operations
from googletrans import Translator  # Importing Google Translator for automatic text translation
from .supported_languages import supp_lang  # Importing supported languages from a separate module
import json  # Importing JSON module for handling JSON data


# Defining the FAQ model
class FAQ(models.Model):
    question = models.TextField()  # Field to store the original question text
    answer = RichTextField()  # Field to store the original answer with rich-text formatting
    translations = models.JSONField(default=dict, blank=True)  # Field to store translations in JSON format

    # Method to retrieve the translated question and answer for a specific language
    def get_translated_text(self, lang):
        if lang in self.translations:
            return self.translations[lang].get(
                "question", self.question), self.translations[lang].get(
                "answer", self.answer)
        return self.question, self.answer

    # Method to translate a given text to a specified language
    def translate_text(self, text, dest):
        translator = Translator()  # Initializing the translator
        loop = asyncio.new_event_loop()  # Creating a new event loop for asynchronous execution
        asyncio.set_event_loop(loop)  # Setting the new event loop as the default
        result = loop.run_until_complete(translator.translate(text, dest=dest))  # Running translation asynchronously
        return result.text  # Returning the translated text

    # Overriding the save method to handle translations before saving to the database
    def save(self, *args, **kwargs):
        if not self.translations:
            self.translations = {}  # Initialize translations if not already set

        # Retrieve previous question and answer to check for changes
        if self.pk:
            existing_faq = FAQ.objects.filter(pk=self.pk).first()
            prev_question = existing_faq.question if existing_faq else None
            prev_answer = existing_faq.answer if existing_faq else None
        else:
            prev_question = None
            prev_answer = None

        question_changed = prev_question != self.question  # Check if question has changed
        answer_changed = prev_answer != self.answer  # Check if answer has changed

        # Iterate through supported languages and update translations if necessary
        for lang in supp_lang:
            if lang not in self.translations or question_changed:
                self.translations[lang] = self.translations.get(lang, {})
                self.translations[lang]["question"] = self.translate_text(
                    self.question, lang)

            if lang not in self.translations or answer_changed:
                self.translations[lang] = self.translations.get(lang, {})
                self.translations[lang]["answer"] = self.translate_text(
                    self.answer, lang)

        # Format the JSON data for better readability
        formatted_json = json.dumps(self.translations, indent=4, ensure_ascii=False)
        self.translations = formatted_json

        super().save(*args, **kwargs)  # Call the parent class's save method to store data in the database
