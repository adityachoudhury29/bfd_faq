import pytest  # Importing pytest for testing
from django.urls import reverse  # Importing reverse to generate URLs dynamically
from rest_framework.test import APIClient  # Importing APIClient for testing API endpoints
from faq_app.models import FAQ  # Importing the FAQ model


@pytest.mark.django_db  # Mark test to use the database
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


@pytest.mark.django_db  # Mark test to use the database
def test_faq_translation():
    """Test automatic translation and
    retrieval from the translations JSON field."""
    faq = FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    translated_question, translated_answer = faq.get_translated_text("hi")

    # Ensure translation is generated and stored in JSONField
    assert "hi" in faq.translations  # Check if translation exists for Hindi
    assert isinstance(translated_question, str)  # Ensure it's a string
    assert isinstance(translated_answer, str)  # Ensure it's a string
    assert translated_question != ""  # Should not be empty
    assert translated_answer != ""  # Should not be empty


@pytest.mark.django_db  # Mark test to use the database
def test_faq_list_api():
    """Test if API returns a list of FAQs."""
    client = APIClient()  # Instantiate API client for making requests

    # Create a sample FAQ entry
    FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    url = reverse("faq-list")  # Generate URL for the FAQ list endpoint
    response = client.get(url)  # Make a GET request

    assert response.status_code == 200  # Ensure successful response
    assert len(response.data) > 0  # Ensure at least one FAQ is returned
    assert "question" in response.data[0]  # Ensure question key exists
    assert "answer" in response.data[0]  # Ensure answer key exists


@pytest.mark.django_db  # Mark test to use the database
def test_faq_list_with_translation():
    """Test if API returns translated
    content when lang parameter is provided."""
    client = APIClient()  # Instantiate API client for making requests

    # Create a sample FAQ entry
    FAQ.objects.create(
        question="What is Django?",
        answer="Django is a high-level Python web framework."
    )

    url = reverse("faq-list") + "?lang=hi"  # Generate URL with language parameter
    response = client.get(url)  # Make a GET request

    assert response.status_code == 200  # Ensure successful response
    assert len(response.data) > 0  # Ensure at least one FAQ is returned
    assert response.data[0]["question"] != "What is Django?"  # Ensure translated question is different
