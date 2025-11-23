# Company-Research-Assistant
AI-powered Company Research Assistant that performs live web research, handles multiple user personas, and generates structured account plans using Groq LLaMA 3.1 and Streamlit. Includes section-level editing, DuckDuckGo search integration, and a clean modular architecture.
# 🚀 Company Research Assistant – Account Plan Generator  
### Built for Eightfold.ai – AI Agent Building Assignment  
### Powered by **Groq LLaMA 3.1**, **DuckDuckGo Search**, and **Streamlit**

---

## 📌 Overview

This project delivers a fully functional **AI Company Research Assistant** capable of:

- Conversational research about any company  
- Handling **multiple user personas** (SDR, AE, PM, Analyst)  
- Live web research using **DuckDuckGo (ddgs)**  
- Generating a clean, structured **Account Plan in Markdown**  
- Allowing iterative **section-level edits**  
- Providing an interactive, real-time **Streamlit UI**

It is designed to be production-quality, modular, and perfectly aligned with all assignment requirements.

---

# 🏗️ Architecture Overview

The system is organized into clear, maintainable modules:
Company-Research_assistant
|-- app.py -> Streamlit UI (chat interface + sidebar controls)
|-- agent.py -> AI agent logic, Groq API calls, Plan generator
|-- prompts.py -> All system prompts for chat + plan generation
|-- web_researcher.py -> DuckDuckGo search integration
|-- requirements.txt
|-- README.md
|-- .env.example
|-- .env -> GROQ_API_KEY(not committed)


---

## 🧠 Component Breakdown

### **1. Streamlit Frontend (`app.py`)**
Manages:
- Chat window  
- Account plan generator  
- Section-level editor  
- Web research runner  
- Markdown export  

### **2. AI Agent (`agent.py`)**
Implements:
- Conversation management  
- Prompt assembly  
- Groq LLaMA 3.1 chat completions  
- Conversation summarization  
- Markdown account-plan generation  
- Section updating logic  

### **3. Prompts (`prompts.py`)**
Contains:
- **CHAT_SYSTEM_PROMPT** – regulates conversation tone, follow-ups, persona adaptation  
- **PLAN_SYSTEM_PROMPT** – enforces structure of the generated account plan  

### **4. DuckDuckGo Research (`web_researcher.py`)**
Uses `ddgs` to:
- Retrieve fresh company information  
- Format results as LLM-ready text  
- Provide a lightweight RAG pipeline  

---

# ⚙️ Setup Instructions

### **1. Clone the Repository**
git clone <YOUR_REPO_URL>
cd Company-Research-Assistant

### **2. Install Dependencies**
pip instal -r requirements.txt

### **3. Configure Environment Variables**
Copy '.env.example' -> '.env'
  cp .env.example .env

Edit .env
  GROQ_API_KEY = your_real_groq_api_key_here
Create a free key at:
👉 https://console.groq.com/keys

### **4. Run the Application**
streamlit run app.py

🧪 How the AI Agent Works
Step 1: User Starts a Conversation
The agent:
* Interprets persona
* Asks follow-up questions
* Guides the discovery process

Step 2: Multi-Persona Adaptability
The agent behaves differently when interacting with:
* SDR (Sales Development Representative)
* Account Executive
* Product Manager
* Analyst
* Consultant

Step 3: Run Live Web Research
User inputs:
* Company name
* Optional keywords
DuckDuckGo search results → summarized by LLaMA 3.1 → added to conversation context.

Step 4: Generate the Account Plan
One click produces a Markdown account plan that includes:
* Account Overview
* Stakeholders
* Business Objectives
* Pain Points
* Solutions & Opportunities
* Recommended Strategy
* Next Steps

Step 5: Section-Level Editing
User selects:
* A section
* Instructions
The agent rewrites only that part while preserving the rest.

Step 6: Download
Plan is downloadable as a .md file


🧩 Design Decisions
1. Groq LLaMA 3.1 Instant Model
* Fastest inference on the market
* Free for developers
* Very low latency → excellent for chat

2. Retrieval-Augmented Workflow (RAG-lite)
DuckDuckGo + LLM summarization helps:
* Reduce hallucinations
* Stay up-to-date
* Provide real-world data

3. Session-State Memory
Streamlit stores:
* Conversation history
* Account plan
* Research context

4. Markdown as Output Format
Ideal for:
* Copying to documents
* Exporting
* Editing
* Integrating with tools like Notion or Confluence

🛠️ Technologies Used
| Component | Technology                |
| --------- | ------------------------- |
| LLM       | Groq LLaMA-3.1 8B Instant |
| Framework | Streamlit                 |
| Search    | DuckDuckGo (`ddgs`)       |
| Config    | python-dotenv             |
| Language  | Python 3.9+               |
