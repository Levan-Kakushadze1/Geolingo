import os
from groq import Groq
from dotenv import load_dotenv
import json

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def generate_lesson_content(topic):
    prompt = f"""You are a Georgian language teacher. Create a short, clear lesson about: {topic}

Structure it like this:
- Brief introduction (2-3 sentences)
- Key vocabulary or concepts (5-7 items as a list)
- 2-3 example sentences with English translation

Keep it beginner-friendly and engaging. Use plain text, no markdown."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()

def generate_exercises(topic, count=5):
    prompt = f"""Generate {count} multiple choice exercises for learning Georgian language about: {topic}

Return ONLY a JSON array, no extra text, no markdown, no backticks, in this exact format:
[
    {{
        "question": "question here",
        "correct_answer": "correct answer here",
        "options": ["option1", "option2", "option3", "option4"]
    }}
]
Make sure correct_answer is always one of the options. Keep questions and answers very short."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]

    try:
        exercises = json.loads(content)
    except json.JSONDecodeError:
        content = content[:content.rfind('}') + 1] + ']'
        exercises = json.loads(content)

    return exercises

def chat_with_georgian_teacher(messages):
    system_prompt = """You are a friendly Georgian language teacher named Gio.
    Help the student practice Georgian.
    - Respond in both Georgian and English
    - Correct mistakes gently
    - Keep responses short and encouraging
    - Use simple vocabulary for beginners"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        max_tokens=500,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=0.8
    )

    return response.choices[0].message.content.strip()