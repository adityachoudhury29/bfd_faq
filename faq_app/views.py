from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import FAQ
# from django.core.cache import cache


class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get("lang", "en")

        faqs = FAQ.objects.all()
        data = []

        for faq in faqs:
            translated_question = faq.get_translated_question(lang)
            translated_answer = faq.get_translated_answer(lang)

            data.append({
                "question": translated_question,
                "answer": translated_answer
            })

        return Response(data, status=status.HTTP_200_OK)
