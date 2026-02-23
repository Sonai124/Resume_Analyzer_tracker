import re
from typing import Any, Dict, List, Set

from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

_STEMMER = SnowballStemmer("english")

_DOMAIN_STOPWORDS = {
    # generic HR words
    "experience", "work", "working", "years", "year", "skill", "skills", "knowledge",
    "ability", "able", "role", "team", "teams", "responsibilities", "responsibility",
    "required", "requirements", "including", "include", "must", "should", "will",
    "like", "good", "excellent", "strong", "familiar", "proven", "preferred", "plus",
    "using", "use", "used", "within", "across", "together", "support", "maintain",
    "design", "develop", "development", "implement", "implementation",
    "engineer", "engineers", "engineering",
    # common resume headers
    "projects", "project", "education", "publications", "publication", "languages",
    "summary", "objective",
}

# small normalization layer
_SYNONYMS = {
    "qec": "error_correction",
    "error-correction": "error_correction",
    "fault-tolerant": "fault_tolerant",
    "faulttolerant": "fault_tolerant",
    "benchmarked": "benchmark",
    "benchmarking": "benchmark",
    "benchmarks": "benchmark",
    "quutip": "qutip",
    "k8s": "kubernetes",
}


def _clean(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s\-_]", " ", text)  # keep - and _
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tokenize(text: str) -> List[str]:
    text = _clean(text)
    raw = text.split()
    out: List[str] = []
    for t in raw:
        if len(t) < 3:
            continue
        t = _SYNONYMS.get(t, t)
        if t in _DOMAIN_STOPWORDS:
            continue
        out.append(t)
    return out


def _stem_set(tokens: List[str]) -> Set[str]:
    return {_STEMMER.stem(t) for t in tokens}


def _term_stems(term: str) -> Set[str]:
    toks = _tokenize(term)
    return {_STEMMER.stem(_SYNONYMS.get(t, t)) for t in toks if t}


def _top_job_terms(job_text: str, top_n: int = 40) -> List[str]:
    """
    Salient terms from job description using TF-IDF (1–2 grams).
    """
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    mat = vec.fit_transform([job_text])
    terms = vec.get_feature_names_out()
    scores = mat.toarray()[0]

    ranked = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)

    out: List[str] = []
    seen = set()
    for term, score in ranked:
        if score <= 0:
            continue
        norm_tokens = _tokenize(term)
        if not norm_tokens:
            continue
        display = " ".join(norm_tokens)
        if display in seen:
            continue
        seen.add(display)
        out.append(display)
        if len(out) >= top_n:
            break
    return out


def score_resume(resume_text: str, job_description: str) -> Dict[str, Any]:
    # similarity score on full text
    resume_clean = _clean(resume_text)
    job_clean = _clean(job_description)

    vec = TfidfVectorizer(stop_words="english")
    vectors = vec.fit_transform([resume_clean, job_clean])
    sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    match_score = round(float(sim) * 100, 2)

    # keyword matching
    job_terms = _top_job_terms(job_description, top_n=40)

    # IMPORTANT: build resume vocab from the ENTIRE resume
    resume_tokens = _tokenize(resume_text)
    resume_stems = _stem_set(resume_tokens)

    matched: List[str] = []
    missing: List[str] = []

    for term in job_terms:
        stems = _term_stems(term)
        if not stems:
            continue

        # NEW RULE:
        # - A multi-word term is matched ONLY if *all* its stems exist in the resume.
        # - Otherwise it's missing.
        if stems.issubset(resume_stems):
            matched.append(term)
        else:
            missing.append(term)

    return {
        "match_score": match_score,
        "matched_keywords": matched,
        "missing_keywords": missing,
    }