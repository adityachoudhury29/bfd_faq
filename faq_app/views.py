from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import FAQ


class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get("lang", "en")
        cache_key = f"faq_list_{lang}"  # Create a unique key for each language
        cached_data = cache.get(cache_key)  # Try to fetch from Redis

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        # If not in cache, fetch from the database
        faqs = FAQ.objects.all()
        data = [
            {
                "question": faq.get_translated_text(lang)[0],
                "answer": faq.get_translated_text(lang)[1],
            }
            for faq in faqs
        ]

        # Store the data in cache for 30 seconds
        cache.set(cache_key, data, timeout=30)

        return Response(data, status=status.HTTP_200_OK)
