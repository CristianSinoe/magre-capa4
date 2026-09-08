from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
STATIC_DIR = BASE_DIR / "static"
OUTPUTS_DIR = BASE_DIR / "outputs"
DATA_DIR = BASE_DIR / "data"
DATABASE_PATH = DATA_DIR / "sessions.db"

SAMPLE_RATE = 44_100
DEFAULT_DURATION_SECONDS = 20
MIN_DURATION_SECONDS = 10
MAX_DURATION_SECONDS = 60
TEST_DURATION_SECONDS = 5
DEFAULT_ROOT_NOTE = "C"

SAFE_LIMITS = {
    "bpm": (60.0, 130.0),
    "volume": (0.05, 0.25),
    "brightness": (0.1, 0.8),
    "note_density": (0.5, 3.0),
    "rhythmic_complexity": (0.1, 1.0),
    "pad_intensity": (0.1, 1.0),
    "melody_activity": (0.0, 1.0),
}

SCALES = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "lydian": [0, 2, 4, 6, 7, 9, 11],
}

ROOT_FREQUENCIES = {
    "C": 261.63,
    "A": 220.00,
}
