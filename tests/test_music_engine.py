from pathlib import Path

from scipy.io import wavfile

from app.models import MusicalParameters
from app.music_engine import generate_wav


def test_generate_audio_file(tmp_path: Path):
    params = MusicalParameters(
        bpm=90,
        mode="major",
        note_density=1.0,
        brightness=0.4,
        volume=0.14,
        rhythmic_complexity=0.4,
        pad_intensity=0.7,
        melody_activity=0.5,
    )
    output_path, technical_details = generate_wav(
        params,
        duration_seconds=5,
        session_id="testsession",
        seed=123,
        output_dir=tmp_path,
    )

    assert output_path.exists()
    sample_rate, data = wavfile.read(output_path)
    assert sample_rate == 44100
    assert technical_details["sample_rate"] == 44100
    assert data.size > 0
