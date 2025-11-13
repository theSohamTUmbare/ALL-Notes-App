import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

DB_PATH = "db/notes.db"

#  DATABASE INITIALIZATION      

def init_db():
    """Initialize the SQLite database with notes and style_profiles tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- NOTES TABLE ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        input_source TEXT,
        content TEXT,
        concepts TEXT,
        tags TEXT,
        resources TEXT,
        rewritten_notes TEXT,
        evaluation TEXT,
        total_score REAL,
        indexing_status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # --- STYLE PROFILES TABLE ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS style_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data_json TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

#  NOTES CRUD OPERATIONS        

def add_note(title: str, input_source: str, content: str, **kwargs) -> int:
    """Insert a new note into the database and return its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO notes (
        title, input_source, content, concepts, tags, resources,
        rewritten_notes, evaluation, total_score, indexing_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        title,
        input_source,
        content,
        json.dumps(kwargs.get("concepts", [])),
        json.dumps(kwargs.get("tags", [])),
        json.dumps(kwargs.get("resources", {})),
        kwargs.get("rewritten_notes", ""),
        json.dumps(kwargs.get("evaluation", {})),
        kwargs.get("total_score", 0.0),
        kwargs.get("indexing_status", "pending")
    ))

    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return note_id


def get_note_by_id(note_id: int) -> Optional[Dict[str, Any]]:
    """Retrieve a single note by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes WHERE id=?", (note_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return _note_row_to_dict(row)
    return None


def get_all_notes() -> List[Dict[str, Any]]:
    """Retrieve all notes, newest first."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [_note_row_to_dict(r) for r in rows]


def update_note(note_id: int, **kwargs):
    """Update note fields dynamically based on provided kwargs."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fields, values = [], []
    for key, value in kwargs.items():
        if key in ["concepts", "tags", "resources", "evaluation"]:
            value = json.dumps(value)
        fields.append(f"{key} = ?")
        values.append(value)

    if not fields:
        return  # nothing to update

    values.append(datetime.now())
    values.append(note_id)

    cursor.execute(f"""
    UPDATE notes
    SET {', '.join(fields)}, updated_at = ?
    WHERE id = ?
    """, tuple(values))

    conn.commit()
    conn.close()


def delete_note(note_id: int):
    """Delete a note by ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()
    conn.close()


def _note_row_to_dict(row):
    """Convert raw database row to dict."""
    return {
        "id": row[0],
        "title": row[1],
        "input_source": row[2],
        "content": row[3],
        "concepts": json.loads(row[4] or "[]"),
        "tags": json.loads(row[5] or "[]"),
        "resources": json.loads(row[6] or "{}"),
        "rewritten_notes": row[7],
        "evaluation": json.loads(row[8] or "{}"),
        "total_score": row[9],
        "indexing_status": row[10],
        "created_at": row[11],
        "updated_at": row[12],
    }

#  STYLE PROFILE CRUD           
def save_style_profiles(style_data: List[Dict[str, Any]]):
    """Replace all style profiles with a new list of JSON profiles."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Store as one big JSON array
    json_data = json.dumps(style_data, indent=2)

    cursor.execute("DELETE FROM style_profiles")
    cursor.execute("""
        INSERT INTO style_profiles (data_json, created_at, updated_at)
        VALUES (?, ?, ?)
    """, (json_data, datetime.now(), datetime.now()))

    conn.commit()
    conn.close()


def get_style_profiles() -> List[Dict[str, Any]]:
    """Retrieve all stored style profiles as JSON list."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT data_json FROM style_profiles ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row and row[0]:
        return json.loads(row[0])
    return []


def update_style_profiles(style_data: List[Dict[str, Any]]):
    """Update the style profiles JSON while keeping timestamps."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    json_data = json.dumps(style_data, indent=2)
    cursor.execute("""
        UPDATE style_profiles
        SET data_json = ?, updated_at = ?
        WHERE id = (SELECT id FROM style_profiles ORDER BY created_at DESC LIMIT 1)
    """, (json_data, datetime.now()))

    conn.commit()
    conn.close()
