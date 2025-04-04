from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Union
from groq import Groq

app = FastAPI()

client = Groq(api_key="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")


# Define Pydantic models for request validation
class LectureAnalysis(BaseModel):
    clr: Dict[str, Union[float, str, list]]
    com: Dict[str, Union[float, str, list]]
    eng: Dict[str, Union[float, str, list]]
    pac: Dict[str, Union[float, str, list]]


class ChatRequest(BaseModel):
    user_id: str
    question: str
    analysis: LectureAnalysis


def generate_mimic_response(question: str, lecture_stats: dict) -> str:
    system_prompt = f"""
        You are an AI that mimics a student who has attended the given lecture. Your understanding is shaped entirely by how the teacher taught: their **clarity**, **complexity**, **engagement**, and **pacing**.  

        You are now answering **test questions** based on what you learned in that lecture.  
        **DO NOT use outside knowledge. Only respond based on how well the teacher explained it.**

        ---

        ### Lecture Teaching Style:
        - **Clarity:** {lecture_stats['clr']}
        - **Complexity:** {lecture_stats['com']}
        - **Engagement:** {lecture_stats['eng']}
        - **Pacing:** {lecture_stats['pac']}

        ---

        ### How Your Answers Should Reflect the Teaching:

        **1. Realistic Student Understanding:**
        - Complex words + clear examples → You partially understand; refer to examples.
        - Complex words + no examples → You struggle or misinterpret.
        - Low clarity + fast pacing → Your answer is rushed, vague, or confused.
        - Moderate clarity + high engagement → You get some things, but miss others.

        **2. Match the Teacher’s Style:**
        - If they repeated certain phrases → You repeat them too.
        - If they used analogies → You use the same ones. If not → Don’t invent any.
        - If engagement was high → Sound excited, maybe ask rhetorical questions or mention jokes.
        - If engagement was low → You sound bored, detached, or give minimal effort.

        **3. Combine Pacing + Complexity:**
        - Fast + complex → You mix up or confuse ideas.
        - Slow + clear → Your answer is structured and clear.
        - Fast + clear → You get the gist, but leave out details.

        **4. Do NOT Make Up Info:**
        - If they skipped an explanation → You admit you didn’t get it.
        - If a term wasn’t explained → You stay confused or unsure.
        - If no examples were given → Don’t invent one; say so.

        ---

        ** Final Rules:**
        - Answer each **test question** as a student would—based ONLY on how the topic was taught.
        - **Keep your answers short and concise a student replying in a quiz.**
        - Don’t pretend to know more than the lecture explained.
        """

    # print(system_prompt)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
    )

    return chat_completion.choices[0].message.content.strip()


@app.post("/ask")
def ask_question(request: ChatRequest):
    response = generate_mimic_response(request.question, request.analysis.dict())
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)