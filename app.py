import streamlit as strl
import json
import os
import time
from datetime import datetime
from groq import Groq
from supabase import create_client, Client

# Page Configuration
strl.set_page_config(page_title="Enterprise AI Ticket Triage", layout="wide")
strl.title("💼 Enterprise AI Customer Support & Triage Console")
strl.markdown("---")

# ==========================================
# 🔐 PRODUCTION CLOUD CREDENTIALS (SECURED VIA ENVIRONMENT VARIABLES)
# ==========================================
# Pull keys securely from operating system environment memory instead of hardcoding
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Validation check to guide the developer or user if keys are missing
if not GROQ_API_KEY or not SUPABASE_URL or not SUPABASE_KEY:
    strl.error("⚠️ Infrastructure Credentials Missing! Please set your environment variables: GROQ_API_KEY, SUPABASE_URL, and SUPABASE_KEY.")
    strl.stop()

# Initialize Cloud Clients
groq_client = Groq(api_key=GROQ_API_KEY)
supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 💾 EXCLUSIVE CLOUD DATABASE ENGINE
# ==========================================
def save_ticket(ticket_data):
    """Saves tickets directly to Supabase cloud table."""
    supabase_client.table("tickets").insert(ticket_data).execute()

def get_tickets():
    """Fetches real-time ticket stream directly from Supabase cloud infrastructure."""
    try:
        response = supabase_client.table("tickets").select("*").execute()
        return response.data[::-1] if response.data else []
    except Exception as e:
        strl.error(f"Cloud Connection Failed: {e}")
        return []

# ==========================================
# 🧠 SEMANTIC AI INFERENCE ENGINE
# ==========================================
def run_ai_logic(text):
    """Performs live semantic inference utilizing an active production model."""
    prompt = f"""
    Analyze this customer support ticket: "{text}"
    Return a strict JSON object with exactly three fields:
    1. "urgency": Either "LOW", "MEDIUM", or "URGENT"
    2. "category": A relevant enterprise category name
    3. "reply": A professional corporate email auto-response addressing the problem.
    Return ONLY valid raw JSON. No commentary. No markdown formatting blocks.
    """
    
    completion = groq_client.chat.completions.create(
        model="openai/gpt-oss-20b", 
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        timeout=5.0
    )
    
    return json.loads(completion.choices.message.content)

# ==========================================
# 🖥️ FRONTEND INTERFACE
# ==========================================
col1, col2 = strl.columns([1, 1.5])

with col1:
    strl.subheader("📥 Submit a New Support Request")
    with strl.form("ticket_form", clear_on_submit=True):
        email = strl.text_input("Customer Email", placeholder="abc@gmail.com")
        message = strl.text_area("Issue Details", placeholder="Describe the problem...")
        submitted = strl.form_submit_button("Submit Ticket")
        
    if submitted and message:
        with strl.spinner("Groq AI Engine running live semantic analysis..."):
            ai_result = run_ai_logic(message)
            
            new_ticket = {
                "id": int(time.time()),
                "email": email,
                "message": message,
                "urgency": ai_result.get("urgency", "MEDIUM"),
                "category": ai_result.get("category", "General Support"),
                "reply": ai_result.get("reply", "Under review."),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            save_ticket(new_ticket)
            strl.success("🚀 Production Ticket Logged to Supabase Cloud!")
            time.sleep(0.5)
            strl.rerun()

with col2:
    strl.subheader("📊 Live Support Queue (Cloud Source)")
    tickets = get_tickets()
    
    if not tickets:
        strl.info("Cloud storage database is currently empty.")
    else:
        for t in tickets:
            if t.get('urgency') == "URGENT":
                icon = "🔴"
            elif t.get('urgency') == "MEDIUM":
                icon = "🟡"
            else:
                icon = "🟢"
            
            label = f"{icon} [{t.get('urgency')}] {t.get('category')} - {t.get('email')}"
            
            with strl.expander(label):
                strl.write(f"**Issue:** {t.get('message')}")
                strl.info(f"**AI Live Draft:** {t.get('reply')}")
                strl.caption(f"Logged at: {t.get('timestamp')}")
                if strl.button("Approve & Send", key=str(t.get('id'))):
                    strl.toast("Response dispatched across network!")