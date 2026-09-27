# 💼 Enterprise AI Triage Microservice
### *An Intelligent Corporate Support Pipeline & Cloud Infrastructure*

An autonomous customer support request tracking microservice. Operating as an intelligent network traffic controller, the system intercepts incoming client communication, evaluates its deep semantic context to prioritize operational crises, and dynamically structures a custom corporate response layer.

---

## 🛠️ Production Tech Stack
* **Frontend Interface (Streamlit):** Maps out a clean, dual-column console featuring data ingestion on the left and a live tracking dashboard queue on the right.
* **Cognitive Inference Brain (GroqCloud API):** Deploys the `openai/gpt-oss-20b` model running under raw JSON mode constraints to achieve ultra-low latency semantic classification without rigid keyword loops.
* **Data Persistence Layer (Supabase Cloud):** An isolated, remote PostgreSQL relational database instance ensuring permanent transaction tracking and dynamic live history streams over the web.

---

## ⚙️ The 4-Step Production Pipeline
1. **Ingestion:** A customer dispatches a nuanced operational description directly into the responsive web console form interface.
2. **AI Inference:** The Python backend securely routes the string payload to the Groq LPU hardware network. The AI computes an urgency rating (**🔴 Urgent, 🟡 Medium, 🟢 Low**), assigns an enterprise IT category, and scripts a professional email auto-response.
3. **Cloud Persistence:** The backend consumes the structured JSON payload and instantly streams an insert command across the web into your remote Supabase table rows.
4. **Real-Time Rendering:** The monitoring console updates its viewport cache dynamically from the cloud stream, rendering an expandable ticket management card to the triage engineer.

---

## 🛡️ Security & Environment Hardening
This repository is configured using professional industry standards to protect access keys:
* **Decoupled Architecture:** Secret tokens are pulled dynamically from host machine runtime environment memory context (`os.environ.get`) rather than plain text script variables.
* **Repository Guard Rails:** A custom `.gitignore` file tracking block explicitly isolates system configurations, preventing local data buffer files from uploading to the cloud.

---

## 🐋 Portable Container Deployment
To run this application inside an isolated virtual container sandbox environment, build and initialize your Dockerfile structure using these commands:
```bash
# 1. Compile the portable container image layout
docker build -t enterprise-triage-app .

# 2. Spin up the container instance while injecting your environment runtime keys
docker run -d -p 8501:8501 --name live_triage_container \
  -e GROQ_API_KEY="your-groq-key" \
  -e SUPABASE_URL="your-supabase-url" \
  -e SUPABASE_KEY="your-supabase-key" \
  enterprise-triage-app
```
