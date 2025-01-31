from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import FAQ

class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get("lang", "en")  # Get desired language
        faqs = FAQ.objects.all()
        data = [
            {
                "question": faq.get_translated_text(lang)[0],
                "answer": faq.get_translated_text(lang)[1],
            }
            for faq in faqs
        ]
        return Response(data, status=status.HTTP_200_OK)
