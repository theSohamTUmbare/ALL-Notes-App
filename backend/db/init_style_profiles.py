# Create the Default JSON Structure (All Values = None)
from datetime import datetime
import json
import sqlite3

DB_PATH = "db/notes.db"

def insert_default_style_profile():
    default_profile = [
        {
            "profile_id": None,
            "name": None,
            "user_persona": None,
            "description": None,
            "created_at": None,
            "updated_at": None,
            "tone": {
                "formality": None,
                "voice": None,
                "use_examples": None
            },
            "detail": {
                "complexity_level": None,
                "explain_example": None
            },
            "abstraction": {
                "complexity_level": None,
                "include_glossary_of_terms": None,
                "math_verbose": None
            },
            "formatting": {
                "use_bullets": None,
                "use_numbered_lists": None,
                "use_headings": None,
                "heading_style": None,
                "bullet_style": None,
                "max_bullet_length_words": None,
                "paragraph_length": None,
                "prefer_tables_for_data": None,
                "emphasize_keywords": None
            },
            "structure": {
                "include_title": None,
                "include_summary_at_top": None,
                "summary_style": None,
                "include_key_terms_section": None,
                "include_examples_section": None,
                "include_actions_or_todos_at_end": None,
                "section_order": None,
                "default_section_order": None
            },
            "language": {
                "language": None,
                "complexity": None,
                "preferred_level_explain_like": None,
                "avoid_jargon": None
            },
            "stylistic_devices": {
                "use_examples": None,
                "use_metaphors": None,
                "use_anaologies": None,
                "use_acronyms_expanded_first": None,
                "use_abbreviations": None,
                "show_action_items": None,
                "highlight_definitions": None
            },
            "custom_instruction": None
        }
    ]

    json_data = json.dumps(default_profile, indent=2)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM style_profiles")
    cursor.execute("""
        INSERT INTO style_profiles (data_json, created_at, updated_at)
        VALUES (?, ?, ?)
    """, (json_data, datetime.now(), datetime.now()))

    conn.commit()
    conn.close()
    print("✅ Default style profile inserted successfully.")

if __name__ == "__main__":
    insert_default_style_profile()
