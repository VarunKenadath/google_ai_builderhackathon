# IT Service Desk AI Agent

A conversational IT support agent built on Google Cloud's Gemini 
Enterprise Agent Platform. Answers Google Workspace questions from a 
curated FAQ and automates ticket creation via a Cloud Run + Firestore 
backend.

## Architecture

![Architecture Diagram](docs/architecture.png)

User → Conversational Messenger → Default Playbook
                                      ├─ Info Agent → Vertex AI Search Data Store
                                      └─ Ticket Agent → OpenAPI Tool → Cloud Run → Firestore

## Tech Stack
- Google Conversational Agents (Vertex AI Agent Builder)
- Gemini 2.5 Flash
- Cloud Run (Python 3.10, Functions Framework)
- Firestore (Native Mode)
- Cloud Storage
- Vertex AI Search
