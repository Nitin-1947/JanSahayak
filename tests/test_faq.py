def test_faq_import():

    from app.knowledge.faq_service import (
        FAQService
    )

    assert FAQService is not None