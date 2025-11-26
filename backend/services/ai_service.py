# backend/services/ai_service.py
"""
AI service: lightweight scoring + feedback generator.

This file contains:
 - score_answers(answers): scores a list of answer dicts and returns summary
 - generate_feedback(attempt_answers, optional_context): returns per-question feedback

Expected `answers` format:
[
  {
    "question_id": "<q id>",
    "type": "mcq" | "coding" | "short",
    "response": "<user response>",
    "expected_answer": "<optional expected answer or keywords>"
  },
  ...
]

Return value from score_answers:
{
  "score": int,
  "max_score": int,
  "per_question": [
    {"question_id": "...", "score": 1, "max_score":1, "feedback": "..."}, ...
  ]
}
"""

from typing import List, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)


def _score_mcq(response: Any, expected: Any) -> int:
    """Simple exact-match scoring for MCQ."""
    try:
        return 1 if str(response).strip().lower() == str(expected).strip().lower() else 0
    except Exception:
        return 0


def _score_short(response: str, expected_keywords: List[str]) -> int:
    """
    Heuristic scoring for short answers:
    - give fractional credit by counting matched keywords.
    - returns integer points (0..1) for simplicity in demo.
    """
    if not response or not expected_keywords:
        return 0
    text = response.lower()
    matches = 0
    for kw in expected_keywords:
        if kw.lower() in text:
            matches += 1
    ratio = matches / len(expected_keywords)
    return 1 if ratio >= 0.5 else 0  # threshold adjustable


def _score_coding(response: str, expected_keywords: List[str]) -> int:
    """
    Very simple coding evaluation: look for presence of key phrases or function names.
    For production, replace this with unit tests or judge system.
    """
    return _score_short(response, expected_keywords)


def score_answers(answers: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Score a list of answers and return structured result.
    Each answer dict may include: question_id, type, response, expected_answer or expected_keywords
    """
    per_question = []
    total = 0
    max_score = 0

    for a in answers:
        qid = a.get("question_id")
        qtype = a.get("type", "short")
        response = a.get("response")
        expected = a.get("expected_answer", None)
        expected_keywords = a.get("expected_keywords", []) or []

        score = 0
        q_max = 1

        if qtype == "mcq":
            score = _score_mcq(response, expected)
        elif qtype == "short":
            # expected_keywords is preferred for short answers
            score = _score_short(response, expected_keywords)
        elif qtype == "coding":
            score = _score_coding(response, expected_keywords)
        else:
            # fallback: simple presence check
            score = 1 if response else 0

        total += score
        max_score += q_max

        feedback = _build_simple_feedback(qtype, score, q_max, expected_keywords, response)
        per_question.append({
            "question_id": qid,
            "score": score,
            "max_score": q_max,
            "feedback": feedback
        })

    return {
        "score": total,
        "max_score": max_score,
        "per_question": per_question
    }


def _build_simple_feedback(qtype, score, q_max, expected_keywords, response):
    """
    Construct a short, actionable feedback string for the user.
    """
    if score >= q_max:
        return "Good answer — covered the key points."
    # if MCQ and wrong, prompt to review core concept
    if qtype == "mcq":
        return "Incorrect. Review the core concept and options again."
    # for short/coding suggest missing keywords
    if expected_keywords:
        missing = [kw for kw in expected_keywords if kw.lower() not in (response or "").lower()]
        if missing:
            return f"Partial — consider addressing: {', '.join(missing)}"
    if not response:
        return "No response provided. Try to answer briefly and include key terms."
    return "Answer could be improved — be more specific and include key terms."



# ---------- LLM / richer feedback hook ----------
def generate_feedback(per_question_results: List[Dict[str, Any]], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Placeholder for advanced feedback generation (e.g., using an LLM).
    Input: per_question_results from score_answers
    Output: same structure with 'detailed_feedback' per question (strings)
    """
    # For demo we reuse the simple feedback already present.
    # Replace this section with an LLM call (OpenAI, local model) if available.
    detailed = []
    for pq in per_question_results:
        # Example enhancement: expand short feedback with tips
        base = pq.get("feedback", "")
        if pq.get("score", 0) == 0:
            tip = "Tip: Break your answer into definition, example, and when to use it."
        elif pq.get("score", 1):
            tip = "Tip: Add a short example or numeric result to strengthen the answer."
        else:
            tip = ""
        detailed.append({
            "question_id": pq.get("question_id"),
            "score": pq.get("score"),
            "feedback": base,
            "detailed_feedback": f"{base} {tip}".strip()
        })
    return {"results": detailed}
