import pytest
from faq_app.models import FAQ


@pytest.mark.django_db
def test_faq_creation():
    faq = FAQ.objects.create(
        question="what is django",
        answer="django is a web framework.",
        question_hi="Django क्या है",
        question_bn="জ্যাঙ্গো কী?"
    )

    assert faq.id is not None
    assert faq.get_translated_question("hi") == "Django क्या है"
    assert faq.get_translated_question("bn") == "জ্যাঙ্গো কী?"
