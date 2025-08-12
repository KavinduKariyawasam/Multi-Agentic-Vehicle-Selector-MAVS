# 🚗 Multi-Agentic Vehicle Selector (MAVS) [Ongoing]

A **multi-agent CrewAI application** with a **FastAPI backend** and a **Streamlit frontend** that helps you find the best vehicles for your budget and location using official manufacturer data.

---

## 📌 Overview

MAVS uses multiple specialized agents to:

1. **Collect** vehicle listings from official manufacturer websites
2. **Analyze** detailed specifications (MPG, safety features, etc.)
3. **Recommend** the top 3 vehicles based on your budget and criteria

The system is designed as a modular architecture so the backend and frontend can evolve independently.

---

## 🏗 Project Structure

```
Multi-Agentic-Vehicle-Selector-MAVS/
│
├── backend/
│   ├── app.py                  # FastAPI entrypoint
│   ├── crew.py                 # VehicleRecommenderCrew logic
│   ├── agents.py               # Agent definitions
│   ├── tasks.py                # Task definitions
│   ├── config/
│   │   ├── agent_prompts.py
│   │   ├── task_prompts.py
│   ├── logger/
│   │   └── logger.py           # Shared logging setup
│   ├── tools/
│   │   └── search_tools.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.py                  # Streamlit entrypoint
│   ├── components/
│   │   ├── inputs.py
│   │   ├── results.py
│   ├── services/
│   │   └── api_client.py
│   ├── utils/
│   │   └── parsing.py
│   └── test.py                 # Local UI test with mock data
│
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Multi-Agentic-Vehicle-Selector-MAVS.git
cd Multi-Agentic-Vehicle-Selector-MAVS
```

### 2. Backend setup

```bash
cd backend
conda create -n vehicle python=3.11
conda activate vehicle
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_MODEL=...
GROQ_API_KEY=...
TOGETHER_MODEL=...
TOGETHER_API_KEY=...
TOGETHER_BASE_URL=...
```

Run backend:

```bash
uvicorn app:app --reload --port 8000
```

---

### 3. Frontend setup

Open a second terminal:

```bash
cd frontend
conda activate vehicle
pip install -r requirements.txt
streamlit run app.py
```

---

## 🚀 Usage

1. Start the backend (`FastAPI`)
2. Start the frontend (`Streamlit`)
3. Open the browser at the URL Streamlit gives you
4. Enter:

   * Location (`USA`, `UK`, etc.)
   * Budget in USD
   * Optional list of allowed manufacturer websites
5. View your **Top 3 recommendations** with detailed reasoning

---

## 🛠 Features

* **Multi-Agent CrewAI** workflow
* **FastAPI** backend with clean error handling & logging
* **Streamlit** UI with side-by-side cards for top picks
* Configurable **agent prompts** & **task prompts**
* JSON parsing from LLM output for structured recommendations

---

## 🧪 Development Notes

* For UI testing without the backend, run:

  ```bash
  streamlit run test.py
  ```

  and adjust mock data inside `frontend/test.py`.
* Logs are centralized via `logger/logger.py`
* Agent roles, goals, and backstories are stored in `config/agent_prompts.py`
* Task instructions live in `config/task_prompts.py`

---

## 📄 License

MIT License – feel free to use, modify, and share.
