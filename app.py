import streamlit as strl
import json
import os
import time
from datetime import datetime

# Page Configuration
strl.set_page_config(page_title="Enterprise AI Ticket Triage", layout="wide")
strl.title("💼 Enterprise AI Customer Support & Triage Console")
strl.markdown("---")

# ==========================================
# 💾 LOCAL DATABASE ENGINE (No Cloud Needed)
# ==========================================
DB_FILE = "local_database.json"

def init_db():
    """Creates a local file to store tickets if it doesn't exist."""
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump([], f)

def save_ticket(ticket_data):
    """Saves a new ticket to the local file."""
    init_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    data.append(ticket_data)
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

def get_tickets():
    """Reads all tickets from the local file."""
    init_db()
    with open(DB_FILE, "r") as f:
        data = json.load(f)
    return data[::-1] # Reverse order (newest first)

# ==========================================
# 🧠 AI LOGIC ENGINE (Simulation Mode)
# ==========================================
def run_ai_logic(text):
    """Simulates the AI decision making instantly."""
    time.sleep(1.5) # Fake processing delay to look real
    text = text.lower()
    
    if "password" in text or "login" in text:
        return {
            "urgency": "LOW",
            "category": "Authentication",
            "reply": "We have received your password reset request. Please check your email for the recovery link."
        }
    elif "billing" in text or "invoice" in text or "money" in text:
        return {
            "urgency": "MEDIUM",
            "category": "Billing & Finance",
            "reply": "We are reviewing your transaction details. A representative will contact you shortly."
        }
    elif "down" in text or "crash" in text or "error" in text:
        return {
            "urgency": "URGENT",
            "category": "Critical Infrastructure",
            "reply": "CRITICAL ALERT: Engineering team has been dispatched to investigate the system outage."
        }
    else:
        return {
            "urgency": "MEDIUM",
            "category": "General Support",
            "reply": "Thank you for contacting support. We have logged your request."
        }

# ==========================================
# 🖥️ FRONTEND INTERFACE
# ==========================================
col1, col2 = strl.columns([1, 1.5])

# LEFT SIDE: Input Form
with col1:
    strl.subheader("📥 Submit a New Support Request")
    with strl.form("ticket_form", clear_on_submit=True):
        email = strl.text_input("Customer Email", placeholder="user@client.com")
        message = strl.text_area("Issue Details", placeholder="Describe the problem...")
        submitted = strl.form_submit_button("Submit Ticket")
        
    if submitted and message:
        with strl.spinner("AI Agent is analyzing ticket..."):
            # 1. Run AI Analysis
            ai_result = run_ai_logic(message)
            
            # 2. Package Data
            new_ticket = {
                "id": int(time.time()),
                "email": email,
                "message": message,
                "urgency": ai_result["urgency"],
                "category": ai_result["category"],
                "reply": ai_result["reply"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # 3. Save to Local Database
            save_ticket(new_ticket)
            
            strl.success("🚀 Ticket Triaged & Saved Successfully!")
            time.sleep(1)
            strl.rerun()

# RIGHT SIDE: Live Dashboard
with col2:
    strl.subheader("📊 Live Support Queue")
    
    tickets = get_tickets()
    
    if not tickets:
        strl.info("Queue is empty. Waiting for new tickets...")
    else:
        for t in tickets:
            # Dynamic Badges
            if t['urgency'] == "URGENT":
                icon = "🔴"
            elif t['urgency'] == "MEDIUM":
                icon = "🟡"
            else:
                icon = "🟢"
            
            label = f"{icon} [{t['urgency']}] {t['category']} - {t['email']}"
            
            with strl.expander(label):
                strl.write(f"**Issue:** {t['message']}")
                strl.info(f"**AI Draft:** {t['reply']}")
                strl.caption(f"Logged at: {t['timestamp']}")
                if strl.button("Approve & Send", key=t['id']):
                    strl.toast("Response sent to client!")
