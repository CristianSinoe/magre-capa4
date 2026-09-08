from app.controller import compute_raw_parameters
from app.models import AffectiveState


def test_lower_target_arousal_reduces_bpm():
    current = AffectiveState(arousal=0.8, valence=0.5, stress=0.3, engagement=0.5)
    lower_target = AffectiveState(arousal=0.3, valence=0.5, stress=0.3, engagement=0.5)
    higher_target = AffectiveState(arousal=0.9, valence=0.5, stress=0.3, engagement=0.5)

    lower_params, _ = compute_raw_parameters(current, lower_target)
    higher_params, _ = compute_raw_parameters(current, higher_target)

    assert lower_params.bpm < higher_params.bpm


def test_high_valence_selects_bright_modes():
    current = AffectiveState(arousal=0.4, valence=0.4, stress=0.2, engagement=0.5)
    target = AffectiveState(arousal=0.5, valence=0.85, stress=0.2, engagement=0.6)
    params, _ = compute_raw_parameters(current, target)
    assert params.mode in {"major", "lydian"}


def test_low_valence_selects_minor_or_dorian():
    current = AffectiveState(arousal=0.4, valence=0.4, stress=0.2, engagement=0.5)
    target = AffectiveState(arousal=0.5, valence=0.2, stress=0.2, engagement=0.6)
    params, _ = compute_raw_parameters(current, target)
    assert params.mode in {"minor", "dorian"}
