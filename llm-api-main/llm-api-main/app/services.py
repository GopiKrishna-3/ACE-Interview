import google.generativeai as genai
import json
import re
from app.config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)


def generate_interview_questions(resume_summary, job_description):
    """
    Generates 10 interview questions using the Gemini API.
    """
    try:
        prompt = (
            f"Based on the following resume and job description, generate 10 interview questions.\n\n"
            f"Resume: {resume_summary}\n"
            f"Job Description: {job_description}\n\n"
            f"Response Format: Return ONLY a JSON object with a 'questions' key containing a list of strings.\n"
            f'Example: {{"questions": ["Question 1", "Question 2", ...]}}'
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)

        return response.text.strip() if response.text else "No questions generated."

    except Exception as e:
        raise RuntimeError(f"Error generating questions: {e}")


def analyze_response(question, answer):
    """
    Analyzes a candidate's spoken answer to an interview question using Gemini.
    Returns: feedback, relevance, sentiment, filler_percentage, repeated_words_count.
    """
    # Count basic text stats locally
    words = answer.lower().split()
    filler_words = {
        "um", "uh", "like", "you know", "basically", "literally",
        "actually", "so", "right", "okay", "er", "hmm", "well"
    }
    filler_count = sum(1 for w in words if w in filler_words)
    filler_percentage = (filler_count / len(words) * 100) if words else 0.0

    from collections import Counter
    word_counts = Counter(words)
    repeated_words_count = sum(1 for w, c in word_counts.items() if c > 2 and len(w) > 3)

    try:
        prompt = (
            "You are an expert interview coach. Analyze the following interview answer "
            "and respond ONLY with a valid JSON object.\n\n"
            f"Question: {question}\n"
            f"Candidate's Answer: {answer}\n\n"
            "Respond with EXACTLY this JSON structure and nothing else:\n"
            '{"feedback": "<2-3 sentence constructive feedback>", '
            '"relevance": "<High|Medium|Low>", '
            '"sentiment": "<Positive|Neutral|Negative>"}'
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        raw = response.text.strip()

        # Strip markdown code fences if present
        raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()

        data = json.loads(raw)

        return {
            "feedback": data.get("feedback", "No feedback available."),
            "relevance": data.get("relevance", "Medium"),
            "sentiment": data.get("sentiment", "Neutral"),
            "filler_percentage": round(filler_percentage, 2),
            "repeated_words_count": repeated_words_count,
        }

    except json.JSONDecodeError:
        return {
            "feedback": "Could not parse AI feedback. Please try again.",
            "relevance": "Medium",
            "sentiment": "Neutral",
            "filler_percentage": round(filler_percentage, 2),
            "repeated_words_count": repeated_words_count,
        }
    except Exception as e:
        raise RuntimeError(f"Error analyzing response: {e}")
