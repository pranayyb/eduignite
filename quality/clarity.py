""" 
1] well structured
2] clear and concise
3] average sentence length
4] readability scores like Flesch-Kincaid or Dale-Chall Index (higher scores = more complex text).
5] Check for excessive jargon without explanations(NER) 

Can use textstat

"""

import textstat
import spacy
from collections import Counter
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
import re

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("words")
nltk.download("averaged_perceptron_tagger")
nltk.download("maxent_ne_chunker")
nltk.download("wordnet")
nltk.download("omw-1.4")
nltk.download("names")
nltk.download("vader_lexicon")
nlp = spacy.load("en_core_web_sm")
sia = SentimentIntensityAnalyzer()
import warnings

warnings.filterwarnings("ignore")


def calculate_clarity(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words_filtered = [w for w in words if w.isalnum() and w.lower() not in stop_words]

    # Sentence length metrics
    avg_sentence_length = sum(len(word_tokenize(sent)) for sent in sentences) / len(
        sentences
    )

    # Readability scores
    flesch_score = textstat.flesch_reading_ease(text)
    dale_chall_score = textstat.dale_chall_readability_score(text)

    # Jargon detection (Named Entities)
    doc = nlp(text)
    named_entities = [ent.text for ent in doc.ents]
    jargon_score = len(named_entities) / max(len(words_filtered), 1)

    # Redundancy detection (word repetition rate)
    word_counts = Counter(words_filtered)
    redundancy_score = sum(1 for count in word_counts.values() if count > 2) / max(
        len(words_filtered), 1
    )

    # Fillers detection (like, um, uh, you know, etc.)
    filler_words = {"um", "uh", "like", "you know", "er", "hmm", "ah"}
    filler_count = sum(1 for word in words if word.lower() in filler_words)
    filler_ratio = filler_count / max(len(words_filtered), 1)

    # Sentiment analysis (tone detection)
    sentiment_scores = sia.polarity_scores(text)
    sentiment = (
        "Positive"
        if sentiment_scores["compound"] > 0.3
        else "Negative" if sentiment_scores["compound"] < -0.3 else "Neutral"
    )

    # Word Preference Analysis (TF-IDF approach - simple count for now)
    common_words = Counter(words_filtered).most_common(5)

    # Detect repeated phrases for natural stress (n-gram analysis, bigrams)
    bigrams = list(nltk.bigrams(words_filtered))
    repeated_phrases = [
        " ".join(bigram) for bigram, count in Counter(bigrams).items() if count > 1
    ]

    # Clarity Score Calculation
    clarity_score = (
        (flesch_score / 100)
        - (dale_chall_score / 10)
        - (redundancy_score * 5)
        - (jargon_score * 3)
        - (filler_ratio * 2)
    )
    clarity_score = max(0, min(clarity_score, 10))  # Normalize between 0-10

    # AI Response Adjustments
    ideal_sentence_length = avg_sentence_length * ((10 - clarity_score) / 5)
    jargon_usage = jargon_score * (1 - (clarity_score / 10))
    complexity_modifier = dale_chall_score / (flesch_score + 1)
    redundancy_adjustment = redundancy_score * (1 - (clarity_score / 10))
    filler_adjustment = filler_ratio * (1 - (clarity_score / 10))

    response_weight = (
        clarity_score
        - (jargon_score * 3)
        - (redundancy_score * 5)
        + (flesch_score / 10)
        - (dale_chall_score / 5)
        - (filler_ratio * 2)
    )

    response_category = (
        "Highly Clear"
        if response_weight > 7
        else "Moderately Clear" if response_weight >= 4 else "Needs Explanation"
    )

    return {
        "avg_sentence_length": avg_sentence_length,
        "flesch_score": flesch_score,
        "dale_chall_score": dale_chall_score,
        "jargon_score": jargon_score,
        "redundancy_score": redundancy_score,
        "filler_ratio": filler_ratio,
        "clarity_score": clarity_score,
        "ideal_sentence_length": ideal_sentence_length,
        "jargon_usage": jargon_usage,
        "complexity_modifier": complexity_modifier,
        "redundancy_adjustment": redundancy_adjustment,
        "filler_adjustment": filler_adjustment,
        "response_weight": response_weight,
        "response_category": response_category,
        "sentiment": sentiment,
        "common_words": common_words,
        "repeated_phrases": repeated_phrases,
    }


if __name__ == "__main__":
    sample_text = "What do you think happens when we die, Keanu Reeves? I know that the ones who love us will miss us."
    result = calculate_clarity(sample_text)
    for key, value in result.items():
        print(f"{key}: {value}")


"""
The script returns:

avg_sentence_length → Average words per sentence
flesch_score → Readability score (higher = easier)
dale_chall_score → Vocabulary complexity (higher = harder)
clarity_score → Overall clarity (0-10, higher = clearer)
jargon_score → Presence of technical terms
redundancy_score → Repeated word usage
filler_ratio → Frequency of fillers ("um," "uh")
ideal_sentence_length → Adjusted sentence length for AI
jargon_usage → Amount of jargon AI should use
complexity_modifier → Adjusts sentence complexity
redundancy_adjustment → Matches redundancy level
filler_adjustment → Matches filler word usage
sentiment → Tone (Positive, Neutral, Negative)
common_words → Most frequently used words
repeated_phrases → Commonly repeated phrases
response_weight → Guides AI response tuning
response_category → Speaker's clarity level (Highly Clear, Moderately Clear, Needs Explanation)

"""


"""
Based on the values from clarity.py, you can draw several conclusions about the clarity of speech:

1. Average Sentence Length (avg_sentence_length)
Low (< 10 words) → Concise and easy to understand.
Medium (10-20 words) → Generally clear, but could be more direct.
High (> 20 words) → Likely complex or rambling.
👉 Longer sentences may need simplification for clarity.

2. Flesch Reading Ease Score (flesch_score)
90-100 → Very easy (e.g., simple conversations, children’s books).
60-80 → Standard (e.g., news articles, conversational speech).
30-60 → Difficult (e.g., academic papers, complex speech).
Below 30 → Very difficult (e.g., legal or highly technical language).
👉 Higher scores mean easier readability, making speech clearer.

3. Dale-Chall Readability Score (dale_chall_score)
Below 5.0 → Easily understood by most people.
5.0 - 8.0 → Challenging for average readers.
Above 8.0 → Complex, full of difficult words or jargon.
👉 Lower scores indicate better clarity and accessibility.

4. Jargon Score (jargon_score)
Low (< 0.05) → Very clear, little jargon.
Medium (0.05 - 0.15) → Some specialized terms, but understandable.
High (> 0.15) → Heavy use of jargon, might need explanation.
👉 Higher values suggest excessive jargon that reduces clarity.

5. Redundancy Score (redundancy_score)
Low (< 0.05) → No excessive repetition, concise speech.
Medium (0.05 - 0.15) → Some redundancy, could be optimized.
High (> 0.15) → Repetitive, might indicate lack of precision.
👉 Higher values suggest the person repeats words, reducing clarity.

6. Clarity Score (clarity_score) (0-10 scale, higher is better)
8-10 → Highly clear speech (concise, well-structured, easy to understand).
5-7 → Moderate clarity (understandable but might have redundancy or jargon).
Below 5 → Low clarity (complex, difficult, or unclear speech).
👉 Use this to adjust AI weights: Higher clarity = mimic simplicity, Lower clarity = mimic complexity.


How Can You Use This in Your AI Agent?
If clarity_score is high, AI should generate concise, simple responses.
If clarity_score is low, AI should allow more complex, verbose responses.
If jargon_score is high, AI should prioritize explanations.
If redundancy_score is high, AI should avoid repetition.


"""
