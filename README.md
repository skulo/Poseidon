# Poseidon 🔱

A file-sharing and quiz-generation web application built for university students. The platform enables students to upload, share and organize study materials in a hierarchical category system, and generate interactive multiple-choice quizzes from uploaded documents using the OpenAI API.

## Features

- **File management** — Upload, replace and delete study materials organized in a multi-level category hierarchy
- **Quiz generation** — Generate multiple-choice quizzes from uploaded documents (PDF, DOCX, PPTX, TXT) using OpenAI GPT-4o-mini
- **Role-based access control** — Four permission levels: visitor, user, moderator, admin
- **Moderation workflow** — Uploaded files go through a moderation process before becoming publicly available; moderators approve or reject submissions with mandatory reasoning for rejections
- **Email verification** — Account activation via email verification code with exponential resend cooldown
- **Token system** — Users earn quiz tokens by uploading approved files, which are spent on quiz generation
- **Rate limiting** — Download limits enforced per user account or IP address to prevent abuse
- **Automated email notifications** — Users receive email updates on moderation decisions including rejection reasons and earned tokens
- **Quiz results tracking** — Users can review, retake and delete their past quiz results

## Tech Stack

**Backend**
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Alembic (database migrations)
- PostgreSQL
- JWT authentication (HTTPOnly cookies)
- OpenAI API (GPT-4o-mini)
- slowapi (rate limiting)
- Docker

**Frontend**
- HTML5, CSS3, JavaScript (vanilla — no UI framework)

## Architecture

The application follows a three-layer architecture:

- **Frontend** — Vanilla HTML/CSS/JS with role-based dynamic DOM manipulation
- **Backend** — FastAPI handling authentication, authorization, file management, quiz generation and moderation
- **Database** — PostgreSQL with SQLAlchemy models covering users, documents, categories, quizzes, quiz results, moderation logs and the email verification system

## Permission Levels

| Role | Capabilities |
|------|-------------|
| Visitor | Browse files, download files (rate limited), fill out quizzes |
| User | All visitor rights + upload files, generate quizzes (token required), manage own content |
| Moderator | All user rights + approve/reject pending files, instant file publishing, no rate limits |
| Admin | All moderator rights + manage any user's files and quizzes |

## Quiz Generation

Quizzes are generated asynchronously in the background using OpenAI GPT-4o-mini. The system extracts text from the uploaded document, sends it to the model with a structured prompt, and validates the returned JSON before saving the questions and answers to the database. Each generation costs 1 token and is limited to documents under ~5500 words to ensure stable model output.

## Verification System

The email verification system is built to be scalable for multi-step verification flows. It tracks verification runs, proofs and completed verifications separately in the database. Verifications are valid for 365 days; expired verifications automatically revoke the user's verified status on next login.
