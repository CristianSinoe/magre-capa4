from app.models import AffectiveState, MusicalParameters
from app.safety import apply_safety_constraints


def test_bpm_never_exceeds_130():
    raw = MusicalParameters(
        bpm=180,
        mode="major",
        note_density=1.2,
        brightness=0.4,
        volume=0.12,
        rhythmic_complexity=0.6,
        pad_intensity=0.6,
        melody_activity=0.6,
    )
    current = AffectiveState(arousal=0.8, valence=0.4, stress=0.2, engagement=0.6)
    target = AffectiveState(arousal=0.9, valence=0.6, stress=0.2, engagement=0.7)
    safe, _ = apply_safety_constraints(raw, current, target)
    assert safe.bpm <= 130


def test_volume_never_exceeds_025():
    raw = MusicalParameters(
        bpm=100,
        mode="major",
        note_density=1.2,
        brightness=0.4,
        volume=0.4,
        rhythmic_complexity=0.6,
        pad_intensity=0.6,
        melody_activity=0.6,
    )
    current = AffectiveState(arousal=0.8, valence=0.4, stress=0.2, engagement=0.6)
    target = AffectiveState(arousal=0.9, valence=0.6, stress=0.2, engagement=0.7)
    safe, _ = apply_safety_constraints(raw, current, target)
    assert safe.volume <= 0.25


def test_high_stress_limits_volume():
    raw = MusicalParameters(
        bpm=115,
        mode="major",
        note_density=1.2,
        brightness=0.4,
        volume=0.22,
        rhythmic_complexity=0.6,
        pad_intensity=0.6,
        melody_activity=0.6,
    )
    current = AffectiveState(arousal=0.8, valence=0.4, stress=0.9, engagement=0.6)
    target = AffectiveState(arousal=0.3, valence=0.6, stress=0.2, engagement=0.7)
    safe, _ = apply_safety_constraints(raw, current, target)
    assert safe.volume <= 0.18


def test_safety_actions_are_recorded():
    raw = MusicalParameters(
        bpm=160,
        mode="major",
        note_density=2.8,
        brightness=0.9,
        volume=0.4,
        rhythmic_complexity=0.6,
        pad_intensity=0.6,
        melody_activity=0.6,
    )
    current = AffectiveState(arousal=0.8, valence=0.4, stress=0.9, engagement=0.6)
    target = AffectiveState(arousal=0.2, valence=0.6, stress=0.2, engagement=0.7)
    _, actions = apply_safety_constraints(raw, current, target)
    assert actions
