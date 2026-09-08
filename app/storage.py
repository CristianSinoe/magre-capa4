from __future__ import annotations

import json
import sqlite3
from datetime import datetime, UTC
from pathlib import Path

from app.config import DATABASE_PATH, DATA_DIR
from app.models import SessionRecord, SessionSummary


def get_connection(database_path: Path = DATABASE_PATH) -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                session_name TEXT,
                input_state TEXT NOT NULL,
                target_state TEXT NOT NULL,
                raw_parameters TEXT NOT NULL,
                safe_parameters TEXT NOT NULL,
                safety_actions TEXT NOT NULL,
                generation_notes TEXT NOT NULL,
                technical_details TEXT NOT NULL,
                output_wav_path TEXT NOT NULL
            )
            """
        )
        conn.commit()


def save_session(record: SessionRecord, database_path: Path = DATABASE_PATH) -> None:
    with get_connection(database_path) as conn:
        conn.execute(
            """
            INSERT INTO sessions (
                session_id,
                timestamp,
                session_name,
                input_state,
                target_state,
                raw_parameters,
                safe_parameters,
                safety_actions,
                generation_notes,
                technical_details,
                output_wav_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record.session_id,
                record.timestamp.isoformat(),
                record.session_name,
                json.dumps(record.input_state),
                json.dumps(record.target_state),
                json.dumps(record.raw_parameters),
                json.dumps(record.safe_parameters),
                json.dumps(record.safety_actions),
                json.dumps(record.generation_notes),
                json.dumps(record.technical_details),
                record.output_wav_path,
            ),
        )
        conn.commit()


def list_sessions(database_path: Path = DATABASE_PATH) -> list[SessionSummary]:
    with get_connection(database_path) as conn:
        rows = conn.execute(
            """
            SELECT session_id, timestamp, session_name, output_wav_path
            FROM sessions
            ORDER BY timestamp DESC
            """
        ).fetchall()
    return [
        SessionSummary(
            session_id=row["session_id"],
            timestamp=datetime.fromisoformat(row["timestamp"]),
            session_name=row["session_name"],
            output_wav_path=row["output_wav_path"],
        )
        for row in rows
    ]


def get_session(session_id: str, database_path: Path = DATABASE_PATH) -> SessionRecord | None:
    with get_connection(database_path) as conn:
        row = conn.execute(
            "SELECT * FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()

    if row is None:
        return None

    return SessionRecord(
        session_id=row["session_id"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        session_name=row["session_name"],
        input_state=json.loads(row["input_state"]),
        target_state=json.loads(row["target_state"]),
        raw_parameters=json.loads(row["raw_parameters"]),
        safe_parameters=json.loads(row["safe_parameters"]),
        safety_actions=json.loads(row["safety_actions"]),
        generation_notes=json.loads(row["generation_notes"]),
        technical_details=json.loads(row["technical_details"]),
        output_wav_path=row["output_wav_path"],
    )


def create_session_record(
    *,
    session_id: str,
    session_name: str | None,
    input_state: dict,
    target_state: dict,
    raw_parameters: dict,
    safe_parameters: dict,
    safety_actions: list[str],
    generation_notes: list[str],
    technical_details: dict,
    output_wav_path: str,
) -> SessionRecord:
    return SessionRecord(
        session_id=session_id,
        timestamp=datetime.now(UTC),
        session_name=session_name,
        input_state=input_state,
        target_state=target_state,
        raw_parameters=raw_parameters,
        safe_parameters=safe_parameters,
        safety_actions=safety_actions,
        generation_notes=generation_notes,
        technical_details=technical_details,
        output_wav_path=output_wav_path,
    )
