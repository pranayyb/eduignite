import streamlit as st
import requests

# FastAPI endpoint
API_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="Lecture Mimic Bot", layout="centered")

st.title("🎓 Lecture Mimic Bot")
st.markdown("Ask a question and get an answer as if a student attended the lecture.")

# User Inputs
user_id = st.text_input("Your User ID", "user123")
question = st.text_area("Enter your question here")

st.markdown("### 📊 Loaded Lecture Analysis")
st.info("Using detailed lecture analysis generated from uploaded content.")

# Full Analysis - Replace with dynamic loading if needed
analysis = {
    "clr": {
        "avg_sentence_length(Average words per sentence; shorter sentences improve clarity.)": 17.67,
        "flesch_score(Measures reading ease; higher scores indicate clearer speech.)": 72.46,
        "dale_chall_score(Evaluates difficult word usage; lower scores mean more accessible speech.)": 5.93,
        "jargon_score(Measures technical or complex word use; high scores reduce clarity.)": 0.0356,
        "redundancy_score(Assesses unnecessary repetition; high scores make speech harder to follow.)": 0.1089,
        "clarity_score(Combines readability, jargon, and redundancy to measure speech clarity.)": 0,
        "filler_adjustment(Adjusts clarity based on the presence of filler words.)": 0.0007,
        "response_category(Classifies the response based on clarity and complexity.)": "Moderately Clear",
        "common_words(Lists frequently used words, indicating speech patterns.)": [
            ["would", 47],
            ["food", 29],
            ["see", 21],
            ["kind", 20],
            ["things", 15],
        ],
    },
    "com": {
        "lexical_diversity(Measures vocabulary richness; higher diversity indicates more varied word use and potential complexity.)": 0.1788,
        "syntactic_complexity(Assesses sentence structure complexity; more clauses and advanced grammar increase complexity.)": 1.169,
        "technical_term_density(Percentage of technical terms used; higher density indicates greater complexity.)": 0.0,
        "complexity_score(Overall measure of speech complexity based on vocabulary, syntax, and technical terms.)": 6.18,
        "complexity_category(Classifies speech complexity as low, moderate, or high based on analysis.)": "Moderately Complex",
    },
    "eng": {
        "example_count(Number of examples provided; more examples improve engagement by making content relatable.)": 2,
        "question_count(Number of questions asked; rhetorical or direct questions boost audience interaction.)": 3,
        "anecdote_count(Number of personal stories or anecdotes shared; increases relatability and engagement.)": 0,
        "sentence_variation(Diversity in sentence structure; greater variation keeps speech dynamic and engaging.)": 62,
        "call_to_action_count(Number of direct prompts for audience action; encourages participation and engagement.)": 0,
        "humor_count(Instances of humor used; appropriate humor makes speech more engaging and enjoyable.)": 0,
        "engagement_score(Overall measure of how engaging the speech is based on various factors.)": 10,
        "engagement_category(Classifies engagement level as low, moderate, or high based on analysis.)": "Highly Engaging",
    },
    "pac": {
        "words_per_minute(Words spoken per minute; higher WPM indicates faster speech, while lower WPM suggests slower pacing.)": 171.83,
        "avg_sentence_length(Average words per sentence; longer sentences may slow down pacing, while shorter ones speed it up.)": 17.67,
        "speech_rate_variability(Variation in speech speed; moderate variability keeps speech dynamic, while extreme shifts may cause inconsistency.)": 8.02,
        "long_pause_ratio(Ratio of long pauses in speech; well-placed pauses enhance clarity, but too many can disrupt pacing.)": 0.0,
        "pacing_category(Classifies speech pacing as slow, moderate, or fast based on analysis.)": "Too Fast",
    },
}

# Display summaries
with st.expander("🔍 See Analysis Summary"):
    st.markdown(
        f"- **Clarity**: {analysis['clr']['response_category(Classifies the response based on clarity and complexity.)']}"
    )
    st.markdown(
        f"- **Complexity**: {analysis['com']['complexity_category(Classifies speech complexity as low, moderate, or high based on analysis.)']}"
    )
    st.markdown(
        f"- **Engagement**: {analysis['eng']['engagement_category(Classifies engagement level as low, moderate, or high based on analysis.)']}"
    )
    st.markdown(
        f"- **Pacing**: {analysis['pac']['pacing_category(Classifies speech pacing as slow, moderate, or fast based on analysis.)']}"
    )

if st.button("Ask the Bot"):
    if not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Thinking like a student..."):
            payload = {"user_id": user_id, "question": question, "analysis": analysis}

            try:
                res = requests.post(API_URL, json=payload)
                res.raise_for_status()
                response = res.json()["response"]
                st.success("✅ Mimic Response:")
                st.write(response)
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
