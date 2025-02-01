from django.core.cache import cache  # Importing Django's cache framework to store and retrieve cached data
from rest_framework.response import Response  # Importing Response class for API responses
from rest_framework.views import APIView  # Importing APIView for handling API requests
from rest_framework import status  # Importing status codes for API responses
from .models import FAQ  # Importing the FAQ model


# API View to retrieve the list of FAQs with caching
class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get("lang", "en")  # Get the requested language, default to English
        cache_key = f"faq_list_{lang}"  # Create a unique cache key based on the language
        cached_data = cache.get(cache_key)  # Try to retrieve the data from cache

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)  # Return cached data if available

        # If data is not in cache, fetch from the database
        faqs = FAQ.objects.all()
        data = [
            {
                "question": faq.get_translated_text(lang)[0],  # Get translated question
                "answer": faq.get_translated_text(lang)[1],  # Get translated answer
            }
            for faq in faqs
        ]

        # Store the fetched data in cache for 30 seconds
        cache.set(cache_key, data, timeout=30)

        return Response(data, status=status.HTTP_200_OK)  # Return the retrieved data
