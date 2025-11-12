from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database_manager import init_db
from api.routes_notes import router as notes_router
from api.routes_pipeline import router as pipeline_router

app = FastAPI(title="Notes Intelligence API", version="1.0")

# --- CORS setup (for frontend connection) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Initialize database ---
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized and ready.")

# --- Register routes ---
app.include_router(notes_router, prefix="/notes", tags=["Notes"])
app.include_router(pipeline_router, prefix="/pipeline", tags=["Pipeline"])

@app.get("/")
def root():
    return {"message": "Welcome to Notes Intelligence Backend!"}
