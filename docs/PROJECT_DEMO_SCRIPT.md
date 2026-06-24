# Project Demo Script

## Introduction
"Hi, I built AI Interview Coach, a full-stack interview preparation platform that turns resumes into personalized practice sessions. It combines a FastAPI backend, an Expo React Native frontend, and Gemini-powered AI for question generation and answer evaluation."

## Demo flow
1. Show the auth screen and explain the login/signup flow.
2. Upload a PDF resume and describe how the backend parses the resume text using PyMuPDF.
3. Create a new interview session for a target company and explain how the resume content informs question generation.
4. Demonstrate answering a question in the app and show how the system captures the response and calculates a score.
5. Navigate to the analytics dashboard or session review page to highlight how performance trends and weakness areas are surfaced.
6. Show the study plan output and explain how it turns weak topics into a structured prep plan.

## Talking points
- "The backend is built with FastAPI and includes JWT auth, secure file upload, and AI orchestration services."
- "Gemini is wrapped in a service layer so I can swap live API usage with deterministic fallback logic."
- "The resume is parsed and used as prompt context, which makes the questions feel more relevant than static question banks."
- "I added Docker and GitHub Actions so the project is deployable and maintainable."

## Closing
"This project demonstrates my ability to integrate modern AI tools, build cross-platform experiences, and deliver production-capable software with quality assurance."
