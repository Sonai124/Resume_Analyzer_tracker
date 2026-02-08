import re
from typing import Any, Dict, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def _clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _top_keywords(text: str, top_n: int = 20) -> List[str]:
    """
    Very simple keyword extraction:
    TF-IDF over the single document, returns top terms.
    """
    vectorizer = TfidfVectorizer(stop_words="english")
    mat = vectorizer.fit_transform([text])
    terms = vectorizer.get_feature_names_out()
    scores = mat.toarray()[0]

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)
    return [term for term, score in ranked[:top_n] if score > 0]


def score_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    """
    Returns:
      - match_score: 0..100
      - matched_keywords
      - missing_keywords
    """
    resume = _clean_text(resume_text)
    job = _clean_text(job_description)

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume, job])

    sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    match_score = round(float(sim) * 100, 2)

    job_kw = set(_top_keywords(job, top_n=25))
    resume_kw = set(_top_keywords(resume, top_n=40))

    matched = sorted(job_kw.intersection(resume_kw))
    missing = sorted(job_kw.difference(resume_kw))

    return {
        "match_score": match_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }
