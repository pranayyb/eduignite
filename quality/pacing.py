"""
1] Words per minute
2] Pauses and sentence length (umm..., uh....)

pyannote.audio

"""

import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
import nltk

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")


def analyze_pacing(text, duration_seconds):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    total_words = len(words)

    # Words per minute calculation
    wpm = (total_words / duration_seconds) * 60 if duration_seconds > 0 else 0

    # Average sentence length
    avg_sentence_length = sum(len(word_tokenize(sent)) for sent in sentences) / len(
        sentences
    )

    # Detect pauses (um, uh, etc.)
    filler_words = {"um", "uh", "like", "you know", "er", "hmm", "ah"}
    filler_count = sum(1 for word in words if word.lower() in filler_words)
    filler_ratio = filler_count / max(len(words), 1)

    # Speech rate variability (standard deviation of sentence lengths)
    sentence_lengths = [len(word_tokenize(sent)) for sent in sentences]
    speech_rate_variability = sum(
        abs(avg_sentence_length - length) for length in sentence_lengths
    ) / len(sentences)

    # Pause duration analysis (long pauses detected by multiple fillers in a row)
    long_pause_count = sum(
        1
        for i in range(len(words) - 1)
        if words[i].lower() in filler_words and words[i + 1].lower() in filler_words
    )
    long_pause_ratio = long_pause_count / max(len(words), 1)

    # Complexity score based on sentence structure
    doc = nlp(text)
    syntactic_complexity = sum(
        1 for token in doc if token.dep_ in {"ccomp", "xcomp", "advcl", "acl", "relcl"}
    ) / len(sentences)

    # Emphasis detection (repeated words)
    word_counts = Counter(words)
    emphasized_words = [word for word, count in word_counts.items() if count > 2]
    emphasis_ratio = len(emphasized_words) / max(len(words), 1)

    # Pacing category based on empirical data
    if wpm > 150:
        pacing_category = "Too Fast"
    elif 100 <= wpm <= 150:
        pacing_category = "Optimal"
    else:
        pacing_category = "Too Slow"

    return {
        "words_per_minute(Words spoken per minute; higher WPM indicates faster speech, while lower WPM suggests slower pacing.)": wpm,
        "avg_sentence_length(Average words per sentence; longer sentences may slow down pacing, while shorter ones speed it up.)": avg_sentence_length,
        # "filler_ratio(Percentage of filler words used; excessive fillers can disrupt pacing and make speech feel slower.)": filler_ratio,
        "speech_rate_variability(Variation in speech speed; moderate variability keeps speech dynamic, while extreme shifts may cause inconsistency.)": speech_rate_variability,
        "long_pause_ratio(Ratio of long pauses in speech; well-placed pauses enhance clarity, but too many can disrupt pacing.)": long_pause_ratio,
        # "syntactic_complexity(Complexity of sentence structure; more complex syntax can slow down pacing and require more processing time.)": syntactic_complexity,
        # "emphasis_ratio(Frequency of emphasized words; strategic emphasis can control pacing and highlight key points.)": emphasis_ratio,
        "pacing_category(Classifies speech pacing as slow, moderate, or fast based on analysis.)": pacing_category,
    }


if __name__ == "__main__":
    sample_text = "Quantum mechanics is a fundamental theory in physics that describes nature at the smallest scales. The behavior of particles is often counterintuitive, defying classical physics."
    duration = 10  # Assume the text was spoken in 10 seconds
    result = analyze_pacing(sample_text, duration)
    for key, value in result.items():
        print(f"{key}: {value}")
