from django.db import models
from ckeditor.fields import RichTextField
import asyncio
from googletrans import Translator
from django.core.cache import cache


class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()
    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    answer_hi = models.TextField(blank=True, null=True)
    answer_bn = models.TextField(blank=True, null=True)

    def get_translated_question(self, lang):
        cache_key = f"faq_{self.id}_question_{lang}"
        translated_question = cache.get(cache_key)

        if translated_question is None:
            if lang == "hi" and self.question_hi:
                translated_question = self.question_hi
            elif lang == "bn" and self.question_bn:
                translated_question = self.question_bn
            else:
                translated_question = self.question

        return translated_question

    def get_translated_answer(self, lang):
        cache_key = f"faq_{self.id}_answer_{lang}"
        translated_answer = cache.get(cache_key)

        if translated_answer is None:
            if lang == "hi" and self.answer_hi:
                translated_answer = self.answer_hi
            elif lang == "bn" and self.answer_bn:
                translated_answer = self.answer_bn
            else:
                translated_answer = self.answer

        return translated_answer

    def translate_text(self, text, dest):
        translator = Translator()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(translator.translate(text, dest=dest))
        return result.text

    def save(self, *args, **kwargs):
        if not self.question_hi:
            self.question_hi = self.translate_text(self.question, "hi")
        if not self.question_bn:
            self.question_bn = self.translate_text(self.question, "bn")
        if not self.answer_hi:
            self.answer_hi = self.translate_text(self.answer, "hi")
        if not self.answer_bn:
            self.answer_bn = self.translate_text(self.answer, "bn")
        super().save(*args, **kwargs)
