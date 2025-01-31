import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from faq_app.models import FAQ

@pytest.mark.django_db
def test_faq_model():
    """Test if FAQ model creates an object successfully."""
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    # Ensure the object is created
    assert faq.id is not None
    assert faq.question == "What is Django?"
    assert faq.answer == "Django is a high-level Python web framework."

@pytest.mark.django_db
def test_faq_translation():
    """Test automatic translation and retrieval from the translations JSON field."""
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    translated_question, translated_answer = faq.get_translated_text("hi")

    # Ensure translation is generated and stored in JSONField
    assert "hi" in faq.translations
    assert isinstance(translated_question, str)
    assert isinstance(translated_answer, str)
    assert translated_question != ""  # Should not be empty
    assert translated_answer != ""  # Should not be empty

@pytest.mark.django_db
def test_faq_list_api():
    """Test if API returns a list of FAQs."""
    client = APIClient()

    FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    url = reverse("faq-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) > 0
    assert "question" in response.data[0]
    assert "answer" in response.data[0]

@pytest.mark.django_db
def test_faq_list_with_translation():
    """Test if API returns translated content when lang parameter is provided."""
    client = APIClient()

    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    url = reverse("faq-list") + "?lang=hi"
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.data) > 0
    assert response.data[0]["question"] != "What is Django?"  # Should return translated text
