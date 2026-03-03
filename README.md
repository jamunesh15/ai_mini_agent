# AI-Powered BRD Mini-Agent (Amberflux Assessment)

This repository contains my submission for the AI Agent Engineering Intern screening test. [cite_start]This mini-agent automates the conversion of business descriptions into structured documentation and validates them against specific engineering rules[cite: 1, 15].

## 📋 Project Overview
The application takes a short business paragraph and performs three key actions:
1. [cite_start]**Generates a structured BRD**: Converts raw text into a JSON format with business overview, stakeholders, capabilities, requirements (IDs like r-001), and assumptions[cite: 18, 26, 30].
2. [cite_start]**Extracts API Intents**: Maps high-level requirements to potential backend API endpoints[cite: 19, 47].
3. **Deterministic Validation**: Ensures that if "upload" is mentioned, an "ingestion" requirement is present. [cite_start]If not, it returns a 422 error[cite: 20, 32, 51].

## 🛠️ Tech Stack
* [cite_start]**Backend**: Python (FastAPI) [cite: 2, 39]
* [cite_start]**AI Model**: Google Gemini API (`gemini-1.5-flash`) [cite: 45]
* [cite_start]**Frontend**: Plain HTML5, Vanilla JavaScript, and CSS [cite: 67]
* **Environment**: `python-dotenv` for secure API key management.

## 📂 Project Structure
* [cite_start]`main.py`: FastAPI server logic, CORS configuration, and LLM prompt integration[cite: 39, 54].
* [cite_start]`index.html`: Minimalist frontend with loading and error handling[cite: 59, 66].
* `requirements.txt`: List of necessary Python libraries.
* `.env`: Local file for your Gemini API Key (excluded from Git).
* `README.md`: This unified setup and project guide.

---

## 🚀 Setup and Installation

Follow these steps to get the project running locally:

### 1. Clone and Install Dependencies
Ensure you have Python 3.8+ installed. Open your terminal in the project folder and run:
```bash
pip install fastapi uvicorn google-generativeai python-dotenv