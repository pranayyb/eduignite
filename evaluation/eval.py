"""
Evaluation Metrics:

Correctness: Accuracy of answers.
Confidence Level: How confidently AI answers.
Concept Understanding: Depth of explanation.
Misconceptions: Presence of incorrect reasoning.

"""

import numpy as np
import textstat
import nltk
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt")

model = SentenceTransformer("all-MiniLM-L6-v2")

quiz_data = [
    {
        "question": "What are the components of food?",
        "answer_key": "Food consists of carbohydrates, proteins, fats, vitamins, and minerals.",
        "ai_response": "The components of food include carbohydrates, proteins, fats, vitamins, and minerals, which help in body growth and energy.",
    },
    {
        "question": "What is a balanced diet?",
        "answer_key": "A balanced diet contains all essential nutrients in the right proportions.",
        "ai_response": "A balanced diet is important. It has proteins, carbs, and vitamins, but I am not sure if I remember all the components correctly.",
    },
]


def semantic_similarity(ans1, ans2):
    emb1 = model.encode(ans1, convert_to_tensor=True)
    emb2 = model.encode(ans2, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(emb1, emb2)[0][0])


def clarity_score(text):
    flesch_score = textstat.flesch_reading_ease(text)
    dale_chall_score = textstat.dale_chall_readability_score(text)
    avg_sentence_length = sum(
        len(nltk.word_tokenize(sent)) for sent in nltk.sent_tokenize(text)
    ) / max(1, len(nltk.sent_tokenize(text)))

    if flesch_score < 50 or dale_chall_score > 9:
        return 1  # Too complex
    elif 50 <= flesch_score <= 70:
        return 2
    else:
        return 3


def confidence_level(response):
    uncertainty_phrases = ["i think", "i’m not sure", "i guess", "maybe", "probably"]
    for phrase in uncertainty_phrases:
        if phrase in response.lower():
            return 1
    return 3


def engagement_score(response):
    example_keywords = ["for example", "such as", "like"]
    question_keywords = ["what if", "have you ever", "did you know"]
    score = 1

    if any(word in response.lower() for word in example_keywords):
        score += 1
    if any(word in response.lower() for word in question_keywords):
        score += 1

    return min(3, score)


def evaluate_response(answer_key, ai_response):
    scores = {}

    scores["accuracy"] = round(semantic_similarity(answer_key, ai_response) * 10, 2)

    scores["relevance"] = round(
        semantic_similarity(answer_key, ai_response[: len(answer_key)]) * 10, 2
    )

    scores["clarity"] = clarity_score(ai_response) * 3.3

    scores["confidence"] = confidence_level(ai_response) * 3.3

    scores["engagement"] = engagement_score(ai_response) * 3.3

    weights = {
        "accuracy": 0.4,
        "relevance": 0.2,
        "clarity": 0.15,
        "confidence": 0.15,
        "engagement": 0.1,
    }
    final_score = sum(scores[factor] * weight for factor, weight in weights.items())

    return scores, round(final_score, 2)


results = []
for data in quiz_data:
    scores, final_score = evaluate_response(data["answer_key"], data["ai_response"])
    results.append(
        {"question": data["question"], "scores": scores, "final_score": final_score}
    )

for res in results:
    print(f"\n Question: {res['question']}")
    print(f"   Accuracy: {res['scores']['accuracy']}/10")
    print(f"   Relevance: {res['scores']['relevance']}/10")
    print(f"   Clarity: {res['scores']['clarity']}/10")
    print(f"   Confidence: {res['scores']['confidence']}/10")
    print(f"   Engagement: {res['scores']['engagement']}/10")
    print(f"   Final Score: {res['final_score']}/10")
