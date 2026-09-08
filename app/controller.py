from __future__ import annotations

from app.models import AffectiveState, MusicalParameters


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def select_mode(current_state: AffectiveState, target_state: AffectiveState) -> str:
    target_valence = target_state.valence
    current_valence = current_state.valence

    if target_valence >= 0.7:
        return "lydian" if current_valence >= 0.55 else "major"
    if target_valence >= 0.45:
        return "major" if current_valence >= 0.5 else "dorian"
    return "dorian" if target_valence >= 0.25 else "minor"


def compute_raw_parameters(
    current_state: AffectiveState,
    target_state: AffectiveState,
) -> tuple[MusicalParameters, list[str]]:
    delta_arousal = target_state.arousal - current_state.arousal
    delta_valence = target_state.valence - current_state.valence
    delta_stress = target_state.stress - current_state.stress
    delta_engagement = target_state.engagement - current_state.engagement

    notes: list[str] = []
    mode = select_mode(current_state, target_state)

    bpm = 92 + (delta_arousal * 30) - (current_state.stress * 10)
    note_density = 1.4 + (delta_arousal * 1.0) + (delta_engagement * 0.6) - (
        current_state.stress * 0.5
    )
    volume = 0.14 + (delta_arousal * 0.04) + (delta_valence * 0.03) - (
        current_state.stress * 0.04
    )
    brightness = 0.45 + (delta_valence * 0.2) - (current_state.stress * 0.15)
    rhythmic_complexity = 0.45 + (delta_engagement * 0.35) + (delta_arousal * 0.15)
    pad_intensity = 0.55 + ((1 - target_state.arousal) * 0.25) + (
        current_state.stress * 0.15
    )
    melody_activity = 0.4 + (delta_engagement * 0.35) + (delta_arousal * 0.2)

    if target_state.arousal < current_state.arousal:
        notes.append("Se reducen tempo, densidad y energía para bajar arousal.")
        bpm -= 8
        note_density -= 0.2
        volume -= 0.01

    if target_state.arousal > current_state.arousal:
        notes.append("Se incrementan tempo y actividad melódica para subir arousal.")
        bpm += 6
        melody_activity += 0.08

    if current_state.stress > 0.7 and target_state.arousal < current_state.arousal:
        notes.append("Estrés alto con objetivo de relajación: pulso más suave y pad dominante.")
        bpm -= 8
        brightness -= 0.07
        rhythmic_complexity -= 0.1
        pad_intensity += 0.08

    if target_state.engagement >= 0.65:
        notes.append("Engagement objetivo alto: se permite más melodía y variación.")
        melody_activity += 0.08
        rhythmic_complexity += 0.06
    else:
        notes.append("Objetivo relajado: más textura y menos eventos rítmicos.")
        pad_intensity += 0.05
        rhythmic_complexity -= 0.06

    if target_state.valence > current_state.valence:
        notes.append("La valencia objetivo favorece modos más luminosos.")
    elif target_state.valence < current_state.valence:
        notes.append("La valencia objetivo conserva un color más sobrio y estable.")

    params = MusicalParameters(
        bpm=_clamp(bpm, 50.0, 140.0),
        mode=mode,
        note_density=_clamp(note_density, 0.3, 3.5),
        brightness=_clamp(brightness, 0.05, 0.95),
        volume=_clamp(volume, 0.03, 0.3),
        rhythmic_complexity=_clamp(rhythmic_complexity, 0.05, 1.0),
        pad_intensity=_clamp(pad_intensity, 0.1, 1.0),
        melody_activity=_clamp(melody_activity, 0.0, 1.0),
    )
    return params, notes
