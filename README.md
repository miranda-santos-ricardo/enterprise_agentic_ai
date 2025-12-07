# 🚀 **Enterprise Agentic AI Orchestrator**
*A policy-driven, multi-agent AI system for processing sensitive enterprise documents with auditability, verification, and governance.*

---

# 🧠 **Overview**

Modern enterprises—especially in **regulated environments** such as banking, finance, insurance, and healthcare—cannot rely on “single LLM calls” or “simple RAG chatbots.”  
These approaches lack:

- **Traceability**  
- **Separation of responsibilities**  
- **Verification of model outputs**  
- **Policy-driven control**  
- **Audit logs for compliance**

This project solves that.

The **Enterprise Agentic AI Orchestrator** uses **three specialized agents** (Extractor → Analyst → Verifier), coordinated by a deterministic orchestrator and governed by explicit policy rules.

It demonstrates **how real AI systems must operate in enterprises**:  
controlled, auditable, transparent, and aligned with risk and compliance expectations.

---

# 🧩 **System Architecture**

The system consists of:

## **1. Extractor Agent**
- Reads TXT or PDF documents  
- Extracts structured JSON (title, summary, entities, keywords, etc.)  
- Ensures predictable output for downstream processing  

## **2. Analyst Agent**
- Performs reasoning based on the extracted structure  
- Identifies risks, findings, and contextual insights  
- Produces structured results (findings, risks, comments)  

## **3. Verifier Agent**
- Inspects LLM output deterministically  
- Flags issues (missing findings, low comment quality, high-severity risks)  
- Generates confidence scores  
- Produces a *valid/invalid* verdict  

## **4. Control Logic + Policies**
- Evaluates verification results against enterprise policies  
- Enforces minimum confidence thresholds  
- Restricts disallowed risk types  
- Produces **APPROVED** or **REJECTED** decisions  

## **5. Audit Logging**
- Every stage writes structured JSON entries to `audit_log.jsonl`  
- Includes inputs, outputs, context, stage transitions, risk counts, confidence scores  

## **6. Orchestrator**
- Executes agents in a fixed, auditable sequence  
- Tracks execution context  
- Routes data and applies policy  
- Ensures the system behaves deterministically  

---

# 📐 **High-Level Flow**

```
[ Document (PDF/TXT) ]
            |
            v
    Extractor Agent
            |
            v
     Analyst Agent
            |
            v
     Verifier Agent
            |
            v
  Policy Evaluation Engine
            |
            v
   APPROVED / REJECTED
            |
            v
      Audit Log (JSONL)
```

---

# ⚙️ **Installation**

### **1. Clone the repository**
```bash
git clone https://github.com/<your-username>/enterprise_agentic_ai.git
cd enterprise_agentic_ai
```

### **2. Create a virtual environment**

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### **3. Install dependencies**
```bash
pip install -r requirements.txt
```

Your `requirements.txt` is intentionally minimal and clean:

```
openai>=1.12.0
pypdf>=4.0.0
python-dotenv>=1.0.0
```

### **4. Configure environment variables**

Create a `.env` file:

```env
OPENAI_API_KEY=your-openai-api-key
MODEL_ID=gpt-4.1-mini
```

---

# ▶️ **How to Run**

### **Process a PDF document**
```bash
python src/main.py data/HR-Guide.pdf
```

### **Process a TXT document**
```bash
python src/main.py samples/sample_policy.txt
```

The orchestrator will automatically:

1. Load and extract text  
2. Run extraction → analysis → verification  
3. Apply enterprise policy  
4. Log every step to `audit_log.jsonl`  
5. Output a final **APPROVED** or **REJECTED** decision  

---

# 📄 **Example Output**

```
[Extractor] Completed.
[Analyst] Completed.
[Verifier] Issues found: ['COMMENTS_TOO_SHORT']
[Policy] Decision: REJECTED

Reasons:
- Verification marked output as invalid.
- Confidence 0.42 is below the policy minimum of 0.75.
```

---

# 🛡️ **Audit Logging**

Every execution step is recorded in:

```
audit_log.jsonl
```

Each line includes:

- request ID  
- document ID  
- stage  
- outputs (extraction, analysis, verification)  
- confidence scores  
- detected issues  
- applied policy  
- final decision  
- context (agent, stage, metadata)  

Example log snippet:

```json
{
  "request_id": "c132c941-d712-43b5-99ce-e773795f3651",
  "document_id": "HR-Guide",
  "has_extraction": true,
  "has_analysis": true,
  "has_verification": true,
  "context": {
    "policy_id": "policy-default",
    "stage": "verification",
    "last_agent": "verifier",
    "verification_confidence": 0.42,
    "verification_issue_count": 2
  }
}
```

---

# 📂 **Project Structure**

```
src/
  agents/
    extractor.py
    analyst.py
    verifier.py
  control/
    policy.py
  governance/
    logger.py
  memory/
    state.py
  orchestrator/
    orchestrator.py
  utils/
    document_loader.py
  main.py

data/
  HR-Guide.pdf

audit_log.jsonl

README.md
architecture.md
requirements.txt
```

---

# 🧱 **Extending the System**

You can extend the orchestrator by adding:

### ✔ New Agents  
(e.g., SummarizerAgent, ComplianceAgent, RedactionAgent)

### ✔ New Policies  
(add industry-specific rules)

### ✔ New input formats  
(DOCX loader, email ingestion, API ingestion)

### ✔ Advanced validation  
Cross-agent reasoning checks or self-verification

---

# 🎯 **Why This Project Matters**

This project demonstrates:

### **✔ Agentic AI applied to real enterprise constraints**  
### **✔ Full-stack AI governance**  
### **✔ Regulated-environment readiness**  
### **✔ Interview-ready architecture**

---

# 💬 **Contributions & Feedback**

Open to improvements and collaboration.
