# 🤖 AI Resume Analyzer & Interview Question Generator

A full-stack AI-powered web application that analyzes resumes and generates
categorized interview questions using LLM and RAG pipeline.

Built as a Final Year Project — SDM College of Engineering and Technology, Dharwad
B.E. Artificial Intelligence & Machine Learning | VTU


---

## ✨ Features

- 📄 **Resume Parsing** — Supports PDF and DOCX formats
- 🔍 **AI Extraction** — Extracts name, email, skills, education, experience, projects
- 🧠 **RAG Pipeline** — Retrieval Augmented Generation for targeted questions
- ❓ **Interview Questions** — Technical, Project-Based, Behavioral, Situational
- 📥 **Export** — Download all questions as a TXT file
- 🎨 **Professional UI** — Built with Streamlit, Lora + Nunito Sans fonts

---

## 🛠️ Tech Stack

### Frontend
| Tech | Purpose |
|---|---|
| Streamlit | Web UI framework |
| HTML / CSS | Custom styling |
| Google Fonts | Lora + Nunito Sans |

### Backend
| Tech | Purpose |
|---|---|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pydantic | Data validation |

### AI / LLM
| Tech | Purpose |
|---|---|
| Gemini 2.0 Flash | LLM for extraction and question generation |
| LangChain | LLM orchestration and RAG pipeline |
| ChromaDB | Vector database |
| all-MiniLM-L6-v2 | Local embedding model |

### Document Parsing
| Tech | Purpose |
|---|---|
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |

---

## 📁 Project Structure

```
ai-resume-analyzer/
│
├── backend/
│   ├── __init__.py
│   ├── main.py                  ← FastAPI app + /analyze endpoint
│   ├── routers/
│   │   ├── resume.py            ← /resume/upload
│   │   └── questions.py         ← /questions/generate
│   ├── services/
│   │   ├── parser.py            ← PDF/DOCX text extraction
│   │   ├── extractor.py         ← Gemini structured extraction
│   │   ├── embedder.py          ← ChromaDB vector store
│   │   └── question_gen.py      ← RAG question generation
│   ├── models/
│   │   └── schemas.py           ← Pydantic models
│   └── utils/
│       └── helpers.py           ← Utility functions
│
├── pages/
│   ├── Upload_Resume.py
│   ├── Analysis_Result.py
│   └── Interview_Questions.py
│
├── data/
│   ├── uploads/
│   └── vectorstore/
│
├── shared.py                    ← Global CSS + reusable components
├── Home.py                      ← Streamlit entry point
├── .env                         ← API keys (not pushed to GitHub)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11+
- Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Step 1 — Clone the repository
```bash
git clone https://github.com/your-username/ai-resume-analyzer.git
cd ai-resume-analyzer
```

### Step 2 — Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Create `.env` file
Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

### Step 5 — Run the application

**Terminal 1 — Start FastAPI backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Start Streamlit frontend:**
```bash
streamlit run Home.py
```

### Step 6 — Open in browser
| Service | URL |
|---|---|
| Streamlit App | http://localhost:8501 |
| FastAPI Backend | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

---

## 🔄 How It Works

```
User uploads resume (PDF/DOCX)
           ↓
Streamlit sends POST /analyze to FastAPI
           ↓
parser.py extracts plain text
           ↓
extractor.py → Gemini → structured JSON
           ↓
question_gen.py → ChromaDB + RAG → questions
           ↓
FastAPI returns JSON to Streamlit
           ↓
Results displayed on Analysis & Questions pages
```

---

## 📦 Requirements

```
streamlit>=1.32.0
requests==2.31.0
fastapi==0.111.0
uvicorn==0.30.1
python-multipart==0.0.9
pydantic==2.7.1
langchain==0.3.25
langchain-core==0.3.83
langchain-community==0.3.24
langchain-google-genai==2.0.7
chromadb==0.5.23
sentence-transformers==2.7.0
pymupdf==1.24.3
python-docx==1.1.2
python-dotenv==1.0.1
numpy==1.26.4
tokenizers==0.22.0
```

---

## 👨‍💻 Developer

**Vishwa Sone**
B.E. Artificial Intelligence & Machine Learning
SDM College of Engineering and Technology, Dharwad
VTU — 2023-2026

---

