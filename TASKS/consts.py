import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

RESOURCE_DIR = os.path.join(PROJECT_ROOT, "resources")

DF_CSV_PATH = os.path.join(RESOURCE_DIR, "csv", "adult.data.csv")
NUMPY_CSV_PATH = os.path.join(RESOURCE_DIR, "csv", "cereal.csv")

ROOM_JSON_PATH = os.path.join(RESOURCE_DIR, "json", "rooms.json")
STUDENT_JSON_PATH = os.path.join(RESOURCE_DIR, "json", "students.json")

BACKGROUND_MUSIC_PATH = os.path.join(RESOURCE_DIR, "music", "background.mp3")
