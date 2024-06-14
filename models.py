from pydantic import BaseModel
from typing import Dict

class NoteFilters(BaseModel):
    filters: list[str]

class NoteMetadata(BaseModel):
   date: str
   doctor: str

class Note(BaseModel):
  diagnoses: list[str] = []
  medications: list[str] = []
  recommendations: list[str] = []
  metadata: NoteMetadata = NoteMetadata(date = "", doctor = "")

class Notes(BaseModel):
   Notes: list[Note]

class CustomNote(BaseModel):
   __base__ = Note