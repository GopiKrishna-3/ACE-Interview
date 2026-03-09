from flask import Blueprint, request, jsonify
from PyPDF2 import PdfReader
import traceback
from app.services import generate_interview_questions, analyze_response

# Create a Blueprint for routes
api_bp = Blueprint("api", __name__)


def extract_text_from_pdf(pdf_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


@api_bp.route("/", methods=["GET"])
def home():
    return jsonify({"status": "AceAI backend is running", "endpoints": ["/upload", "/analyze"]}), 200


@api_bp.route("/upload", methods=["POST"])
def upload():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Resume file is required."}), 400

        resume_file = request.files["file"]
        job_description = request.form.get("job_description", "").strip()

        if not resume_file:
            return jsonify({"error": "Resume file is required."}), 400

        if not job_description:
            return jsonify({"error": "Job description is required."}), 400

        resume_summary = extract_text_from_pdf(resume_file)

        if not resume_summary or not resume_summary.strip():
            return jsonify({"error": "Could not extract text from the PDF. Please try a different file."}), 400

        print(f"[UPLOAD] Extracted {len(resume_summary)} chars from PDF.")
        print(f"[UPLOAD] Job description length: {len(job_description)} chars.")

        response = generate_interview_questions(resume_summary, job_description)

        print(f"[UPLOAD] Gemini response received ({len(response)} chars).")
        return jsonify({"apiResponse": response}), 200

    except ValueError as e:
        print(f"[UPLOAD ERROR] ValueError: {e}")
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        print(f"[UPLOAD ERROR] RuntimeError: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[UPLOAD ERROR] Unexpected: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


@api_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Accepts { "question": "...", "response": "..." } JSON body.
    Returns structured feedback from Gemini.
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "JSON body is required."}), 400

        question = data.get("question", "").strip()
        answer = data.get("response", "").strip()

        if not question or not answer:
            return jsonify({"error": "Both 'question' and 'response' fields are required."}), 400

        print(f"[ANALYZE] Question: {question[:80]}...")
        result = analyze_response(question, answer)
        print(f"[ANALYZE] Result: {result}")
        return jsonify(result), 200

    except RuntimeError as e:
        print(f"[ANALYZE ERROR] RuntimeError: {e}")
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        print(f"[ANALYZE ERROR] Unexpected: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500