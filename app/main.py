from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import OUTPUTS_DIR, STATIC_DIR
from app.controller import compute_raw_parameters
from app.models import GenerateRequest, GenerateResponse, SessionMetadata, generate_session_id
from app.music_engine import generate_wav
from app.safety import apply_safety_constraints
from app.storage import create_session_record, get_session, init_db, list_sessions, save_session


@asynccontextmanager
async def lifespan(_: FastAPI):
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    init_db()
    yield


app = FastAPI(
    title="MAG-RE Capa 4",
    description="Prototipo técnico de actuador musical generativo para MAG-RE.",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")


@app.get("/", response_class=FileResponse)
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_intervention(request: GenerateRequest) -> GenerateResponse:
    try:
        session_id = generate_session_id()
        raw_params, generation_notes = compute_raw_parameters(
            request.current_state, request.target_state
        )
        safe_params, safety_actions = apply_safety_constraints(
            raw_params, request.current_state, request.target_state
        )
        wav_path, technical_details = generate_wav(
            safe_params,
            duration_seconds=request.duration_seconds,
            session_id=session_id,
            seed=request.seed,
        )
        record = create_session_record(
            session_id=session_id,
            session_name=request.session_name,
            input_state=request.current_state.model_dump(),
            target_state=request.target_state.model_dump(),
            raw_parameters=raw_params.model_dump(),
            safe_parameters=safe_params.model_dump(),
            safety_actions=safety_actions,
            generation_notes=generation_notes,
            technical_details=technical_details,
            output_wav_path=f"/outputs/{wav_path.name}",
        )
        save_session(record)
    except Exception as exc:  # pragma: no cover - defensive path
        raise HTTPException(status_code=500, detail=f"Error generando intervención: {exc}") from exc

    metadata = SessionMetadata(
        input_state=record.input_state,
        target_state=record.target_state,
        raw_parameters=record.raw_parameters,
        safe_parameters=record.safe_parameters,
        safety_actions=record.safety_actions,
        generation_notes=record.generation_notes,
        technical_details=record.technical_details,
    )
    return GenerateResponse(
        session_id=session_id,
        audio_url=record.output_wav_path,
        metadata=metadata,
    )


@app.get("/api/sessions")
async def get_sessions():
    return list_sessions()


@app.get("/api/sessions/{session_id}")
async def get_session_by_id(session_id: str):
    session = get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Sesión no encontrada.")
    return session
