"""
1] examples, analogies, and real-world applications ("For example," "Imagine," or "Just like...").
2] Question frequency (rhetorical/interactive questions)

nltk 

"""

import nltk
import spacy
from collections import Counter
import textstat
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re

nltk.download("punkt")
nltk.download("stopwords")
nlp = spacy.load("en_core_web_sm")


def analyze_engagement(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    words_filtered = [
        w.lower() for w in words if w.isalnum() and w.lower() not in stop_words
    ]

    # Detect examples and analogies
    example_keywords = {
        "for example",
        "imagine",
        "just like",
        "consider",
        "think about",
    }
    example_count = sum(1 for phrase in example_keywords if phrase in text.lower())

    # Detect questions
    question_count = text.count("?")

    # Direct audience engagement (use of 'you', 'we', 'let's')
    direct_audience_words = {"you", "we", "let’s", "your", "us"}
    direct_engagement_count = sum(
        1 for word in words_filtered if word in direct_audience_words
    )

    # Detect emotional words
    emotional_words = {
        "exciting",
        "tragic",
        "amazing",
        "terrible",
        "wonderful",
        "shocking",
    }
    emotional_word_count = sum(1 for word in words_filtered if word in emotional_words)

    # Storytelling and anecdotes detection
    anecdote_phrases = {
        "i remember",
        "back in my day",
        "once upon a time",
        "when i was",
    }
    anecdote_count = sum(1 for phrase in anecdote_phrases if phrase in text.lower())

    # Sentence variation analysis
    sentence_lengths = [len(word_tokenize(sentence)) for sentence in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentences) if sentences else 0
    sentence_variation = (
        max(sentence_lengths) - min(sentence_lengths) if sentences else 0
    )

    # Call-to-action words
    call_to_action_phrases = {
        "think about it",
        "try this",
        "you should",
        "consider this",
    }
    call_to_action_count = sum(
        1 for phrase in call_to_action_phrases if phrase in text.lower()
    )

    # Humor detection
    humor_words = {"haha", "funny", "laugh", "hilarious", "joke"}
    humor_count = sum(1 for word in words_filtered if word in humor_words)

    # Readability score
    readability = textstat.flesch_reading_ease(text)

    # Engagement Score Calculation (Weighted Sum)
    engagement_score = (
        (example_count * 2)
        + (question_count * 1.5)
        + (direct_engagement_count * 2)
        + (emotional_word_count * 1.5)
        + (anecdote_count * 2)
        + (sentence_variation * 0.1)
        + (call_to_action_count * 2)
        + (humor_count * 1.5)
        + (readability / 10)
    )
    engagement_score = max(0, min(engagement_score, 10))  # Normalize between 0-10

    # Categorize engagement level
    engagement_category = (
        "Highly Engaging"
        if engagement_score > 7
        else "Moderately Engaging" if engagement_score >= 4 else "Low Engagement"
    )

    return {
        "example_count": example_count,
        "question_count": question_count,
        "direct_engagement_count": direct_engagement_count,
        "emotional_word_count": emotional_word_count,
        "anecdote_count": anecdote_count,
        "avg_sentence_length": avg_sentence_length,
        "sentence_variation": sentence_variation,
        "call_to_action_count": call_to_action_count,
        "humor_count": humor_count,
        "readability": readability,
        "engagement_score": engagement_score,
        "engagement_category": engagement_category,
    }


if __name__ == "__main__":
    sample_text = "Have you ever wondered why the sky is blue? Imagine looking at a prism. Just like that, light scatters. Back in my day, I used to think it was magic! Think about it—science explains everything! Haha!"
    result = analyze_engagement(sample_text)
    for key, value in result.items():
        print(f"{key}: {value}")


"""
Here's how the AI should interpret each score and adjust its response:

Examples & Analogies Score → High score means AI should use more real-world examples, analogies, and comparisons.
Question Score → Higher values mean the speaker frequently engages the audience with rhetorical or interactive questions; AI should incorporate more questions.
Direct Audience Address Score → If high, AI should use direct pronouns like "you," "we," and "let’s" to create a conversational tone.
Emotional Words Score → Higher values indicate expressive speech; AI should use more emotionally charged words.
Anecdote & Storytelling Score → If high, AI should include personal experiences or storytelling elements in responses.
Sentence Variation Score → Higher values mean diverse sentence structures; AI should mix short and long sentences for a dynamic feel.
Call-to-Action Score → If high, AI should guide the audience with persuasive prompts like "Think about it," or "Try this."
Humor Score → High values indicate the use of humor; AI should include light-hearted or witty elements.
Readability Score → If high, the speaker uses simpler language; AI should avoid complex vocabulary.
"""
