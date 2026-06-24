from typing import Dict, Any, List
from pathlib import Path
import re
import os
from uuid import uuid4
from sqlalchemy.orm import Session
from fastapi import UploadFile
from app.models.resume import Resume
from app.utils.pdf_parser import extract_text_from_pdf

UPLOAD_DIR = Path('uploads') / 'resumes'


def ensure_upload_dir() -> None:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_upload_file(file: UploadFile, dest_path: Path) -> None:
    with dest_path.open('wb') as f:
        content = file.file.read()
        f.write(content)


class ResumeService:
    @staticmethod
    def create_resume(db: Session, user_id: int, file: UploadFile) -> Resume:
        ensure_upload_dir()
        ext = Path(file.filename).suffix.lower()
        uid = uuid4().hex
        filename = f"{uid}{ext}"
        dest = UPLOAD_DIR / filename
        save_upload_file(file, dest)

        # initial DB record
        resume = Resume(user_id=user_id, filename=file.filename, file_path=str(dest))
        db.add(resume)
        db.commit()
        db.refresh(resume)

        # extract text
        try:
            text, page_count = extract_text_from_pdf(str(dest))
        except Exception:
            text, page_count = ('', 0)

        analysis = ResumeService.analyze_text(text)

        resume.extracted_text = text
        # store a small analysis snapshot in meta if desired
        # here we simply update extracted_text; analysis can be stored in another table
        db.add(resume)
        db.commit()
        db.refresh(resume)
        return resume

    @staticmethod
    def analyze_text(text: str) -> Dict[str, List[str]]:
        # Rule-based extraction heuristics
        skills = ResumeService.extract_skills(text)
        projects = ResumeService.extract_projects(text)
        technologies = ResumeService.extract_technologies(text)
        achievements = ResumeService.extract_achievements(text)
        return {
            'skills': skills,
            'projects': projects,
            'technologies': technologies,
            'achievements': achievements,
        }

    @staticmethod
    def extract_skills(text: str) -> List[str]:
        # look for lines starting with Skills or Skills:
        matches = re.findall(r"(?im)^skills?:\s*(.+)$", text)
        skills = []
        for m in matches:
            parts = re.split(r"[,;|]\s*", m)
            for p in parts:
                tok = p.strip()
                if tok:
                    skills.append(tok)

        # fallback: find common tech tokens
        common = ['Python', 'Java', 'C++', 'C#', 'JavaScript', 'TypeScript', 'React', 'React Native', 'Django', 'FastAPI', 'PyTorch', 'TensorFlow', 'SQL', 'PostgreSQL', 'SQLite']
        for c in common:
            if c.lower() in text.lower() and c not in skills:
                skills.append(c)
        return skills

    @staticmethod
    def extract_projects(text: str) -> List[str]:
        # naive: look for lines containing 'Project' or 'Projects' headings
        matches = re.findall(r"(?im)^projects?:\s*(.+)$", text)
        projects = []
        for m in matches:
            parts = re.split(r"[,;]\s*", m)
            for p in parts:
                tok = p.strip()
                if tok:
                    projects.append(tok)
        # fallback: look for 'Project:' occurrences
        matches2 = re.findall(r"(?i)project:\s*(.+)", text)
        for m in matches2:
            tok = m.split('\n')[0].strip()
            if tok and tok not in projects:
                projects.append(tok)
        return projects

    @staticmethod
    def extract_technologies(text: str) -> List[str]:
        tech = []
        common = ['FastAPI', 'Django', 'React', 'React Native', 'PyTorch', 'TensorFlow', 'SQLite', 'PostgreSQL', 'Redis', 'Docker', 'Kubernetes', 'AWS']
        for c in common:
            if c.lower() in text.lower():
                tech.append(c)
        return tech

    @staticmethod
    def extract_achievements(text: str) -> List[str]:
        # Look for lines starting with Achievements or Awards
        matches = re.findall(r"(?im)^(achievements|awards|honors)?:\s*(.+)$", text)
        achievements = []
        for _, m in matches:
            parts = re.split(r"[,;]\s*", m)
            for p in parts:
                tok = p.strip()
                if tok:
                    achievements.append(tok)
        return achievements
