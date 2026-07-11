# AceAI - AI-Powered Interview Prep Platform

🚀 **Live Frontend:** [https://ace-interview-ui.vercel.app/](https://ace-interview-lvxf.vercel.app/)  
⚙️ **Live Backend:** [https://web-production-01d6cc.up.railway.app/](https://web-production-01d6cc.up.railway.app/)

---

AceAI is an intelligent, AI-powered platform designed to simulate realistic job interviews, analyze candidate responses, and provide structured, actionable feedback to help job seekers master their interview preparation.

## Project Structure

This repository is structured as a monorepo containing both the frontend application and the backend API:

*   **`UI-main/`**: The frontend user interface built using Next.js, React, and Tailwind CSS.
*   **`llm-api-main/llm-api-main/`**: The backend REST API built with Flask, integrated with the Google Gemini API for intelligent question generation and response analysis.

---

## Features

- **Resume & Job Description Analysis**: Upload a PDF resume along with a job description to generate tailored, highly relevant interview questions.
- **Interactive Interview Simulation**: Simulate a real-time interview layout where questions are presented sequentially.
- **AI-Powered Response Coaching**: Analyzes spoken or written responses and provides:
  - **Constructive Feedback**: Detailed recommendations on how to improve your answers.
  - **Relevance Score**: High, Medium, or Low relevance rating compared to the question.
  - **Sentiment Analysis**: Positive, Neutral, or Negative sentiment evaluation.
  - **Filler Word Detection**: Analyzes usage of filler words (`um`, `uh`, `like`, `so`, etc.).
  - **Repetitive Language Analysis**: Tracks frequently repeated words.

---

## Local Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.10+)
- Gemini API Key

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd llm-api-main/llm-api-main
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your Gemini API Key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
5. Run the server:
   ```bash
   python app.py
   ```
   The backend will be running at `http://localhost:5000`.

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd UI-main
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file and point it to the local backend:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
