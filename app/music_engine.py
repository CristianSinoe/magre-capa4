from __future__ import annotations

from datetime import datetime, UTC
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from app.config import DEFAULT_ROOT_NOTE, OUTPUTS_DIR, ROOT_FREQUENCIES, SAMPLE_RATE, SCALES
from app.models import MusicalParameters


def _adsr_envelope(length: int, attack: float, decay: float, sustain_level: float, release: float) -> np.ndarray:
    if length <= 0:
        return np.array([], dtype=np.float32)

    attack_samples = int(length * attack)
    decay_samples = int(length * decay)
    release_samples = int(length * release)
    sustain_samples = max(length - attack_samples - decay_samples - release_samples, 0)

    attack_curve = np.linspace(0.0, 1.0, max(attack_samples, 1), endpoint=False)
    decay_curve = np.linspace(1.0, sustain_level, max(decay_samples, 1), endpoint=False)
    sustain_curve = np.full(max(sustain_samples, 1), sustain_level)
    release_curve = np.linspace(sustain_level, 0.0, max(release_samples, 1), endpoint=True)

    envelope = np.concatenate([attack_curve, decay_curve, sustain_curve, release_curve])
    return envelope[:length].astype(np.float32)


def _oscillator(freq: float, duration: float, brightness: float, sample_rate: int) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    sine = np.sin(2 * np.pi * freq * t)
    triangle = 2 * np.abs(2 * ((freq * t) % 1) - 1) - 1
    mix = (1 - brightness) * sine + brightness * triangle
    return mix.astype(np.float32)


def _note_frequency(root_freq: float, semitone_offset: int) -> float:
    return root_freq * (2 ** (semitone_offset / 12))


def _build_pad(
    params: MusicalParameters,
    duration_seconds: int,
    root_note: str,
    sample_rate: int,
) -> np.ndarray:
    scale = SCALES[params.mode]
    root_freq = ROOT_FREQUENCIES.get(root_note, ROOT_FREQUENCIES[DEFAULT_ROOT_NOTE])
    chord_steps = [scale[0], scale[2], scale[4]]
    segment_seconds = max(duration_seconds / 4, 2)
    segment_samples = int(segment_seconds * sample_rate)
    total_samples = duration_seconds * sample_rate
    pad = np.zeros(total_samples, dtype=np.float32)

    for i in range(0, total_samples, segment_samples):
        chord = np.zeros(min(segment_samples, total_samples - i), dtype=np.float32)
        for step in chord_steps:
            note = _oscillator(
                _note_frequency(root_freq, step),
                len(chord) / sample_rate,
                params.brightness * 0.4,
                sample_rate,
            )
            chord += note[: len(chord)] / len(chord_steps)
        envelope = _adsr_envelope(len(chord), 0.15, 0.15, 0.85, 0.2)
        pad[i : i + len(chord)] += chord * envelope * params.pad_intensity * 0.45
        chord_steps = chord_steps[1:] + chord_steps[:1]

    return pad


def _build_melody(
    params: MusicalParameters,
    duration_seconds: int,
    root_note: str,
    sample_rate: int,
    rng: np.random.Generator,
) -> np.ndarray:
    total_samples = duration_seconds * sample_rate
    melody = np.zeros(total_samples, dtype=np.float32)
    if params.melody_activity <= 0.02:
        return melody

    scale = SCALES[params.mode]
    root_freq = ROOT_FREQUENCIES.get(root_note, ROOT_FREQUENCIES[DEFAULT_ROOT_NOTE]) * 2
    beat_duration = 60.0 / params.bpm
    note_duration = max(0.2, beat_duration / max(params.note_density, 0.5))
    step_seconds = max(note_duration * (1.2 - params.melody_activity * 0.5), 0.15)

    for start in np.arange(0, duration_seconds, step_seconds):
        if rng.random() > params.melody_activity:
            continue
        semitone = int(rng.choice(scale))
        octave_jump = 12 if rng.random() > 0.75 else 0
        freq = _note_frequency(root_freq, semitone + octave_jump)
        wave = _oscillator(freq, note_duration, params.brightness, sample_rate)
        env = _adsr_envelope(len(wave), 0.08, 0.15, 0.5, 0.2)
        start_idx = int(start * sample_rate)
        end_idx = min(start_idx + len(wave), total_samples)
        melody[start_idx:end_idx] += wave[: end_idx - start_idx] * env[: end_idx - start_idx] * 0.24

    return melody


def _build_pulse(
    params: MusicalParameters,
    duration_seconds: int,
    sample_rate: int,
    rng: np.random.Generator,
) -> np.ndarray:
    total_samples = duration_seconds * sample_rate
    pulse = np.zeros(total_samples, dtype=np.float32)
    beat_duration = 60.0 / params.bpm
    pulse_gain = 0.05 + (params.note_density - 0.5) * 0.03
    click_duration = max(0.03, 0.08 - params.rhythmic_complexity * 0.03)

    for start in np.arange(0, duration_seconds, beat_duration):
        if rng.random() > 0.55 + params.rhythmic_complexity * 0.35:
            continue
        noise = rng.normal(0, 1, int(sample_rate * click_duration)).astype(np.float32)
        decay = np.linspace(1.0, 0.0, len(noise), endpoint=True).astype(np.float32)
        shaped = noise * decay
        start_idx = int(start * sample_rate)
        end_idx = min(start_idx + len(shaped), total_samples)
        pulse[start_idx:end_idx] += shaped[: end_idx - start_idx] * pulse_gain

    return pulse


def _normalize_audio(audio: np.ndarray, volume: float) -> np.ndarray:
    peak = np.max(np.abs(audio))
    if peak > 0:
        audio = audio / peak
    return (audio * volume).astype(np.float32)


def generate_wav(
    params: MusicalParameters,
    duration_seconds: int,
    session_id: str,
    seed: int | None = None,
    root_note: str = DEFAULT_ROOT_NOTE,
    sample_rate: int = SAMPLE_RATE,
    output_dir: Path = OUTPUTS_DIR,
) -> tuple[Path, dict[str, float | int | str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(seed)

    pad = _build_pad(params, duration_seconds, root_note, sample_rate)
    melody = _build_melody(params, duration_seconds, root_note, sample_rate, rng)
    pulse = _build_pulse(params, duration_seconds, sample_rate, rng)

    audio = pad + melody + pulse
    fade_samples = min(sample_rate, len(audio) // 2)
    if fade_samples > 0:
        fade_in = np.linspace(0.0, 1.0, fade_samples, endpoint=True)
        fade_out = np.linspace(1.0, 0.0, fade_samples, endpoint=True)
        audio[:fade_samples] *= fade_in
        audio[-fade_samples:] *= fade_out

    normalized = _normalize_audio(audio, params.volume)
    int_audio = np.int16(np.clip(normalized, -1.0, 1.0) * 32767)

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    file_path = output_dir / f"{session_id}_{timestamp}.wav"
    wavfile.write(file_path, sample_rate, int_audio)

    technical_details = {
        "sample_rate": sample_rate,
        "channels": 1,
        "duration_seconds": duration_seconds,
        "root_note": root_note,
        "output_samples": len(int_audio),
        "peak_amplitude": float(np.max(np.abs(normalized))) if len(normalized) else 0.0,
    }
    return file_path, technical_details
