# All Notes Intelligence

All Notes Intelligence is a full-stack, multi-agent workspace that ingests raw material (text, PDFs, images), distills high-fidelity notes, and rewrites them in a preferred voice while keeping every insight discoverable through semantic search and chat.

## Highlights

- **Automated note intelligence** – chain ingestion, cleaning, concept extraction, tagging, external resource discovery, and stylistic rewriting via a LangGraph pipeline.
- **Personalized style control** – learn or apply style profiles that drive tone, structure, and formatting decisions for rewritten notes.
- **Context-aware chat** – query stored notes through a FastAPI endpoint backed by Chroma vector search for grounded responses.
- **Streamlit workspace** – create, browse, search, and manage notes with a fast local UI that coordinates with the pipeline API.
- **SQLite persistence** – store canonical notes, style profiles, and evaluation feedback with automatic migrations on startup.

## System Architecture

!(agentic_workflow_diagram)[./agentic_workflow_diagram.png]

## Tech Stack

- **Frontend:** Streamlit, Requests
- **API:** FastAPI, Uvicorn, Pydantic
- **Orchestration:** LangGraph, LangChain, RunnableParallel
- **LLM + AI Tooling:** Google Generative AI (Gemini), KeyBERT, YAKE, custom agent classes
- **Storage:** SQLite (application state), ChromaDB (vector search)
- **Document Processing:** PyMuPDF (fitz), Pillow, PyTesseract, OCR utilities
- **Infrastructure:** Python 3.11 virtual environment (see `allNotes/`), optional Google Gemini key management

## Repository Layout

```
backend/
  main.py                FastAPI entrypoint and router registration
  graph_pipeline.py      LangGraph workflow connecting agent nodes
  agents/                Specialized agents (ingestion, notes, style, tagging, web search)
  nodes/                 Node wrappers that orchestrate agents within the pipeline
  api/                   REST route definitions (notes, pipeline run, style profiles, chat)
  db/                    SQLite + Chroma helpers and initialization scripts

frontend/
  Home.py                Streamlit launcher (multipage UI)
  components.py          State management, pipeline invocation, API helpers
  pages/                 Streamlit pages for notes list, detail view, chat, style profile UI

requirements.txt         Workspace-level dependencies (mirrors `frontend` and `backend` needs)
tasks.txt                Developer task backlog
```

## Prerequisites

- Python 3.11 (recommended; projects expect 3.11.x)
- Tesseract OCR installed and on PATH (required for scanned PDF/image ingestion)
- Google Generative AI API key with access to `gemini-2.0-flash-lite`
- (Optional) GPU-compatible PyTorch install if you plan to swap in local transformers

## Quick Start

1. **Clone the repository and create a virtual environment**
	```bash
	git clone <repo-url>
	cd ALL Notes Project
	python -m venv .venv
	.venv\Scripts\activate  # Windows
	```
2. **Install shared dependencies**
	```bash
	pip install -r requirements.txt
	```
3. **Install service-specific extras (if running independently)**
	```bash
	pip install -r backend/requirements.txt
	pip install -r frontend/requirements.txt
	```
4. **Configure environment variables** (see next section).
5. **Start the backend**
	```bash
	uvicorn backend.main:app --reload --port 8000
	```
6. **Launch the frontend** (in a new shell)
	```bash
	streamlit run frontend/Home.py
	```

## Environment Configuration

Set the following variables before running the pipeline or chat features:

| Variable | Description |
| --- | --- |
| `GENAI_API_KEY` | Google Gemini API key consumed by agent constructors. |
| `CHROMA_DB_PATH` | Optional override for the Chroma persistent directory; defaults to `backend/db/chroma_store`. |
| `SQLITE_DB_PATH` | Optional override for the SQLite database file; defaults to `backend/db/app.db`. |

You can place these values in a `.env` file and load them via `python-dotenv`, or export them directly in the shell before launching Uvicorn/Streamlit.

## Running the Pipeline Programmatically

For scripted ingestion (outside of the Streamlit UI), use the helper in [backend/run_pipeline.py](backend/run_pipeline.py):

```bash
python backend/run_pipeline.py
```

Adapt the `initial_state` payload to point to your data source, API key, and style profile before invoking `run_workflow`.

![](/frontend.png)

## API Reference

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/` | Health check. |
| `GET` | `/notes/` | List all stored notes. |
| `GET` | `/notes/{note_id}` | Fetch a single note. |
| `DELETE` | `/notes/{note_id}` | Delete a note and remove its vector entry. |
| `POST` | `/pipeline/run` | Execute the LangGraph workflow for a supplied pipeline state. |
| `POST` | `/pipeline/learn` | Update a style profile from uploaded content or text. |
| `GET` | `/style_profiles/` | Retrieve active style profiles. |
| `POST` | `/chat/query` | Perform a semantic chat request against stored notes. |
| `GET` | `/search?query=...&k=5` | Retrieve the top `k` semantic matches from ChromaDB. |

Refer to [backend/api/routes_pipeline.py](backend/api/routes_pipeline.py) and [backend/api/routes_notes.py](backend/api/routes_notes.py) for payload schemas and response formats.

## Style Profiles

- Profiles live in [backend/agents/style_profile.json](backend/agents/style_profile.json) and are loaded into SQLite on startup.
- The Streamlit Style Profile page lets you edit preferences and optionally upload writing samples to refine parameters via the learner endpoint.
- At pipeline execution, the selected profile steers tone, structure, formatting, and evaluation thresholds used by the `StyleRewriterAgent`.

## Data and Persistence

- SQLite database created automatically in `backend/db` with tables for notes, evaluations, and style profiles (see [backend/db/database_manager.py](backend/db/database_manager.py)).
- ChromaDB persists embeddings under `backend/db/chroma_store`, enabling semantic search, chat summarization, and note deduplication.
- Attachments are currently stored in-memory; extend the `create_note` handler to persist binary assets if required.

## Development Guidelines

- Keep agent responsibilities single-purpose; new agents should expose a `run` method returning serializable structures.
- When extending the pipeline, register new nodes in [backend/graph_pipeline.py](backend/graph_pipeline.py) and update the `PipelineState` schema in [backend/state_schema.py](backend/state_schema.py).
- Streamlit UI logic lives in modular functions within [frontend/components.py](frontend/components.py); avoid placing long-running operations directly inside page scripts.
- Run `uvicorn` with `--reload` during development and refresh the Streamlit tab to see UI changes instantly.


---

Feel free to open issues or submit pull requests that improve agent accuracy, UI ergonomics, or backend resilience.
