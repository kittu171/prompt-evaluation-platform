# Prompt Evaluation Platform

An AI-powered Prompt Evaluation Platform that automatically generates multiple prompt variants, generates AI responses, evaluates them across multiple quality criteria, selects the best prompt, and produces an improved final prompt.

## 🚀 Features

* Generate multiple prompt variants
* Generate AI responses for each prompt
* Evaluate responses using:

  * Correctness
  * Relevance
  * Clarity
  * Conciseness
  * Instruction Following
* Calculate an overall score
* Select the best-performing prompt
* Automatically generate an improved prompt
* REST API using FastAPI
* Dockerized application
* Swagger/OpenAPI documentation

## 🏗️ Workflow

```text
Original Prompt
      ↓
Generate Prompt Variants
      ↓
Generate AI Responses
      ↓
Evaluate Responses
      ↓
Calculate Scores
      ↓
Select Best Prompt
      ↓
Generate Improved Prompt
      ↓
Return JSON Result
```

## 🛠️ Tech Stack

* Python
* FastAPI
* Ollama / LLM
* Docker
* REST API
* OpenAPI / Swagger

## 📁 Project Structure

```text
prompt-evaluation-platform/
│
├── prompt_optimizer.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── .venv/
```

> `.venv/` is excluded from the Docker build context.

## ▶️ Run Locally

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python prompt_optimizer.py
```

## 🐳 Docker

Build the Docker image:

```powershell
docker build -t prompt-evaluation-platform .
```

Run the container:

```powershell
docker run --rm -p 8000:8000 prompt-evaluation-platform
```

If the application uses Ollama running on the host machine, configure the Ollama connection according to the application settings.

## 📡 API

The application exposes an API endpoint for prompt optimization.

Example request:

```json
{
  "prompt": "Explain RAG."
}
```

The API returns:

* Generated prompt variants
* Generated responses
* Evaluation scores
* Best prompt
* Best score
* Final improved prompt

## 📊 Example Evaluation

```text
Version 1 → 8.8/10
Version 2 → 7.2/10
Version 3 → 8.0/10

Best Version → Version 1
Best Score   → 8.8/10
```

## 🎯 Purpose

The goal of this project is to demonstrate how an AI system can automatically evaluate and optimize prompts instead of relying only on manually written prompts.

This project can be useful for:

* Prompt engineering
* LLM evaluation
* Generative AI applications
* AI agents
* Automated prompt optimization
* AI application development

## 🔮 Future Improvements

* Add a web-based dashboard
* Add more evaluation metrics
* Support multiple LLM providers
* Add evaluation history
* Add authentication
* Add database storage
* Add automated tests
* Add CI/CD pipeline
* Deploy the API to a cloud platform

## 👩‍💻 Author

**Kittu**

Generative AI / AI Engineering enthusiast focused on building practical LLM applications, RAG systems, AI agents, and prompt evaluation platforms.

GitHub: [kittu171](https://github.com/kittu171)

---

## 📌 Project Status

**Status: Completed ✅**

This project was built as a practical demonstration of an AI-powered prompt evaluation and optimization platform using local LLMs, FastAPI, LangChain, Ollama, and Docker.