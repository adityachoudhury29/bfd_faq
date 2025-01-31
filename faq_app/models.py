from django.db import models
from ckeditor.fields import RichTextField
import asyncio
from googletrans import Translator
import json
from .supported_languages import supp_lang

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    translations = models.JSONField(default=dict, blank=True)  # Store translations dynamically

    def get_translated_text(self, lang):
        """
        Retrieve translated question and answer for the given language.
        """
        if lang in self.translations:
            return self.translations[lang].get("question", self.question), self.translations[lang].get("answer", self.answer)
        return self.question, self.answer

    def translate_text(self, text, dest):
        translator = Translator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translator.translate(text, dest=dest))
        return result.text

    def save(self, *args, **kwargs):
        """
        Automatically translate the text into the selected language and store it in JSON format.
        If the question/answer has changed, update translations.
        """
        if not self.translations:
            self.translations = {}

        # Fetch existing values from DB (if the object already exists)
        if self.pk:
            existing_faq = FAQ.objects.filter(pk=self.pk).first()
            prev_question = existing_faq.question if existing_faq else None
            prev_answer = existing_faq.answer if existing_faq else None
        else:
            prev_question = None
            prev_answer = None

        # Check if question or answer has changed
        question_changed = prev_question != self.question
        answer_changed = prev_answer != self.answer

        for lang in supp_lang:
            if lang not in self.translations or question_changed:
                self.translations[lang] = self.translations.get(lang, {})
                self.translations[lang]["question"] = self.translate_text(self.question, lang)

            if lang not in self.translations or answer_changed:
                self.translations[lang] = self.translations.get(lang, {})
                self.translations[lang]["answer"] = self.translate_text(self.answer, lang)

        super().save(*args, **kwargs)
