from __future__ import annotations

from app.config import SAFE_LIMITS
from app.models import AffectiveState, MusicalParameters


def _clamp_parameter(
    params_dict: dict[str, float | str],
    actions: list[str],
    name: str,
    low: float,
    high: float,
) -> None:
    value = params_dict[name]
    if not isinstance(value, (int, float)):
        return
    corrected = max(low, min(high, float(value)))
    if corrected != float(value):
        params_dict[name] = corrected
        actions.append(f"{name} ajustado de {value:.3f} a {corrected:.3f} por límites de seguridad.")


def apply_safety_constraints(
    raw_params: MusicalParameters,
    current_state: AffectiveState,
    target_state: AffectiveState,
) -> tuple[MusicalParameters, list[str]]:
    params_dict = raw_params.model_dump()
    actions: list[str] = []

    for name, (low, high) in SAFE_LIMITS.items():
        _clamp_parameter(params_dict, actions, name, low, high)

    if current_state.stress > 0.75:
        if params_dict["volume"] > 0.18:
            previous = params_dict["volume"]
            params_dict["volume"] = 0.18
            actions.append(
                f"volume reducido de {previous:.3f} a 0.180 por estrés actual alto."
            )
        if params_dict["brightness"] > 0.55:
            previous = params_dict["brightness"]
            params_dict["brightness"] = 0.55
            actions.append(
                f"brightness reducido de {previous:.3f} a 0.550 por estrés actual alto."
            )
        if target_state.arousal < current_state.arousal and params_dict["bpm"] > 110:
            previous = params_dict["bpm"]
            params_dict["bpm"] = 110.0
            actions.append(
                f"bpm reducido de {previous:.3f} a 110.000 por estrés alto y objetivo de relajación."
            )

    if target_state.arousal < 0.4 and params_dict["note_density"] > 1.5:
        previous = params_dict["note_density"]
        params_dict["note_density"] = 1.5
        actions.append(
            f"note_density reducido de {previous:.3f} a 1.500 por arousal objetivo bajo."
        )

    if params_dict["volume"] > 0.25:
        previous = params_dict["volume"]
        params_dict["volume"] = 0.25
        actions.append(
            f"volume reducido de {previous:.3f} a 0.250 para evitar audio intenso."
        )

    safe_params = MusicalParameters(**params_dict)
    return safe_params, actions
