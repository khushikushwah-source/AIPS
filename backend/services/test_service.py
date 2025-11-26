# backend/services/test_service.py
"""
Test / question helpers.

Provides:
 - get_test_with_questions(test_id): returns test doc plus embedded question objects
 - list_questions_for_test(test_id): returns list of question docs
"""

from typing import List, Dict, Any
import logging

from backend.config.settings import settings
from backend.services import firebase_service  # using the service module

logger = logging.getLogger(__name__)


def get_test_with_questions(test_id: str) -> Dict[str, Any]:
    """
    Retrieve a test document and expand its question_ids into full question docs.
    Returns dict: { test: <test_doc>, questions: [<question_docs>] }
    """
    test_doc = firebase_service.get_doc(settings.COLLECTION_TESTS, test_id)
    if not test_doc:
        return {}

    q_ids = test_doc.get("question_ids", []) or []
    questions = []

    for qid in q_ids:
        q = firebase_service.get_doc(settings.COLLECTION_QUESTIONS, qid)
        if q:
            questions.append(q)
        else:
            logger.warning("Question %s listed in test %s not found", qid, test_id)

    return {"test": test_doc, "questions": questions}


def list_questions_for_test(test_id: str) -> List[Dict[str, Any]]:
    """
    Convenience wrapper that returns just the question list for a test.
    """
    data = get_test_with_questions(test_id)
    return data.get("questions", [])


def sample_random_questions_by_difficulty(test_id: str, desired_count: int = 5, difficulty: str = None) -> List[Dict[str, Any]]:
    """
    Example helper: from the questions linked to a test, pick up to `desired_count`
    optionally filtering by difficulty. This is a simple deterministic selection (first N).
    For random selection, import random and shuffle.
    """
    questions = list_questions_for_test(test_id)
    if difficulty:
        questions = [q for q in questions if q.get("difficulty") == difficulty]
    # simple slice
    return questions[:desired_count]
