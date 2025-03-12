"""
1] Lexical diversity (unique words vs. total words) → Low diversity means repetitive, high diversity means complex.
2] Syntactic complexity (nested clauses, difficult sentence structures).
3] Technical terms density

spacy can be used

"""

import spacy
import textstat
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import nltk

nltk.download("punkt")
nlp = spacy.load("en_core_web_sm")


def analyze_complexity(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    total_words = len(words)
    unique_words = len(set(words))

    # Lexical diversity (unique words vs. total words ratio)
    lexical_diversity = unique_words / total_words if total_words else 0

    # Syntactic complexity (average dependency tree depth)
    doc = nlp(text)
    total_clauses = sum(
        1 for token in doc if token.dep_ in {"ccomp", "xcomp", "advcl", "acl", "relcl"}
    )
    syntactic_complexity = total_clauses / len(sentences) if sentences else 0

    # Technical term density (count of domain-specific words)
    technical_terms = {
        "algorithm",
        "quantum",
        "theorem",
        "derivative",
        "neural",
        "molecular",
        "syntactic",
        "statistical",
    }
    technical_term_count = sum(1 for word in words if word.lower() in technical_terms)
    technical_term_density = technical_term_count / total_words if total_words else 0

    # Readability score (higher = easier to understand)
    readability = textstat.flesch_reading_ease(text)

    # Complexity score calculation (inverse of readability, weighted sum)
    complexity_score = (
        (1 - lexical_diversity) * 3
        + syntactic_complexity * 2
        + technical_term_density * 4
        + (100 - readability) / 20
    )
    complexity_score = max(0, min(complexity_score, 10))  # Normalize between 0-10

    # Complexity category
    complexity_category = (
        "Highly Complex"
        if complexity_score > 7
        else "Moderately Complex" if complexity_score >= 4 else "Low Complexity"
    )

    return {
        "lexical_diversity(Measures vocabulary richness; higher diversity indicates more varied word use and potential complexity.)": lexical_diversity,
        "syntactic_complexity(Assesses sentence structure complexity; more clauses and advanced grammar increase complexity.)": syntactic_complexity,
        "technical_term_density(Percentage of technical terms used; higher density indicates greater complexity.)": technical_term_density,
        # "readability(Evaluates how easy or difficult the speech is to understand; lower readability suggests higher complexity.)": readability,
        "complexity_score(Overall measure of speech complexity based on vocabulary, syntax, and technical terms.)": complexity_score,
        "complexity_category(Classifies speech complexity as low, moderate, or high based on analysis.)": complexity_category,
    }


if __name__ == "__main__":
    sample_text = "The quantum entanglement theorem states that when two particles become entangled, their states remain correlated regardless of distance. This principle is fundamental to quantum computing and secure communication."
    result = analyze_complexity(sample_text)
    for key, value in result.items():
        print(f"{key}: {value}")


"""
Here's the full list of AI response guidelines:

AI Response Guidelines Based on Analyzed Complexity

1] Lexical Diversity (Unique Words vs. Total Words)
Low Diversity: Use repetitive vocabulary, reinforce key terms.
High Diversity: Introduce varied vocabulary, avoid repetition.

2] Syntactic Complexity (Sentence Structure & Clauses)
Low Complexity: Use short, direct sentences.
High Complexity: Use nested clauses, longer sentences, and advanced grammar.

3] Technical Term Density (Domain-Specific Words)
Low Density: Use simple, everyday language.
High Density: Use precise technical terms relevant to the domain.

4] Readability Score (Ease of Understanding)
80-100 (Easy): Use simple words, conversational tone.
50-80 (Moderate): Balance technical and simple terms.
0-50 (Difficult): Use dense, academic language with complex sentence structures.

5] Complexity Score & Category (Overall Difficulty)
0-3 (Low Complexity): Keep explanations simple, avoid jargon, focus on clarity.
4-7 (Moderate Complexity): Provide depth while ensuring clarity.
8-10 (High Complexity): Assume familiarity with technical terms, provide in-depth answers.

6] Adjust Response Style Based on Speaker Patterns
If the person frequently uses examples/analogies, incorporate similar comparisons.
If the person frequently asks rhetorical or interactive questions, use a similar questioning style.
If the person prefers formal/informal speech, match their tone accordingly.

7] Response Behavior Based on Complexity Analysis
For a Highly Complex Speaker (Score: 8+):
"Quantum entanglement delineates a non-local correlation between qubits, preserving coherence despite spatial separation, a principle paramount in cryptographic paradigms."
For a Moderately Complex Speaker (Score: 4-7):
"Quantum entanglement means that two particles stay connected even when far apart, which helps in quantum computing and secure communication."
For a Simple Speaker (Score: 0-3):
"Quantum entanglement is when two particles are linked, even if they are far away. This is useful for security and computers."

8] Final Instruction for AI:
Analyze the complexity of the question and adjust responses accordingly.
Mimic the analyzed person's vocabulary, sentence structure, and technical detail level.

"""
