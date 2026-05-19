import functions_framework
from google.cloud import firestore
from datetime import datetime
import re

db = firestore.Client()

def categorize_ticket(issue_description: str) -> str:
    """Categorize ticket based on keywords in description."""
    desc = issue_description.lower()
    
    categories = {
        "email": ["gmail", "email", "inbox", "mail", "smtp", "outlook"],
        "drive": ["drive", "file", "folder", "shared drive", "storage", "upload"],
        "calendar": ["calendar", "meeting", "event", "schedule", "invite"],
        "meet": ["meet", "video call", "conference", "webcam", "microphone"],
        "account": ["password", "login", "sign in", "access", "locked", "2fa", "mfa"],
        "chat": ["chat", "space", "message", "google chat"],
        "docs": ["docs", "sheets", "slides", "document", "spreadsheet"],
        "admin": ["admin", "permissions", "group", "license", "provisioning"],
    }
    
    for category, keywords in categories.items():
        if any(re.search(rf"\b{kw}\b", desc) for kw in keywords):
            return category
    
    return "general"

def submit_ticket(corporate_alias: str, issue: str) -> dict:
    """Insert a ticket into Firestore and return ticket info."""
    category = categorize_ticket(issue)
    ticket_data = {
        "corporate_alias": corporate_alias,
        "issue": issue,
        "category": category,
        "status": "open",
        "created_at": datetime.utcnow(),
    }
    doc_ref = db.collection("issues").add(ticket_data)
    ticket_id = doc_ref[1].id
    return {
        "ticket_id": ticket_id,
        "category": category,
        "status": "open",
        "message": f"Ticket {ticket_id} created under category '{category}'."
    }

@functions_framework.http
def submit_ticket_http(request):
    """HTTP entry point for the agent OpenAPI tool."""
    if request.method == "OPTIONS":
        return ("", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST",
            "Access-Control-Allow-Headers": "Content-Type",
        })
    
    try:
        request_json = request.get_json(silent=True) or {}
        corporate_alias = request_json.get("corporate_alias")
        issue = request_json.get("issue")
        
        if not corporate_alias or not issue:
            return ({"error": "Both 'corporate_alias' and 'issue' are required."}, 400)
        
        result = submit_ticket(corporate_alias, issue)
        return (result, 200)
    
    except Exception as e:
        return ({"error": str(e)}, 500)
