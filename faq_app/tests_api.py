import pytest
from rest_framework.test import APIClient
from faq_app.models import FAQ


@pytest.mark.django_db
def test_fetch_faqs():
    FAQ.objects.create(
        question="what is django",
        answer="django is a web framework.",
        question_hi="Django क्या है",
        question_bn="জ্যাঙ্গো কী?"
    )

    client = APIClient()
    response = client.get("/api/faqs/?lang=hi")

    assert response.status_code == 200
    assert response.json()[0]["question"] == "Django क्या है"
