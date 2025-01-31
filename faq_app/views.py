from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import FAQ
from .serializers import FAQSerializer
from django.core.cache import cache

class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get("lang", "en")

        cache_key = f"faqs_{lang}"
        cached_faqs = cache.get(cache_key)

        if cached_faqs:
            return Response(cached_faqs, status=status.HTTP_200_OK)

        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True, context={"request": request})

        cache.set(cache_key, serializer.data, timeout=3600)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
