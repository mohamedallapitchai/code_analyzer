# 🔍 AI-Powered Codebase Analyzer using GPT-4 + LangChain (Early Version)

This is an **experimental tool** that uses **GPT-4** and **LangChain** to analyze a codebase — even when it has **no documentation, comments, or tests** — and infer its **purpose, functionality, and problem statement**.

Currently, this project is in a **primitive stage**, run manually via a Python script or an editor. It supports **any programming language** as long as the code is provided in text form.

---

## 📌 What It Does

This tool aims to evaluate how well a large language model (LLM) like **GPT-4** can:

- Understand and summarize raw source code
- Infer the high-level purpose of a project
- Generate illustrative examples (if possible)

---

## 🧪 Current Workflow

### ✅ Step 1: Read the Code  
The code is manually loaded from a local directory or GitHub clone.  
Documentation, comments, and test files are excluded to simulate a barebones codebase.

---

### ✅ Step 2: Split Into Chunks  
The source code is split into chunks (if needed) using LangChain’s `RecursiveCharacterTextSplitter` to avoid exceeding the model's token limits.

---

### ✅ Step 3: Analyze Each Chunk  
Each chunk is sent to GPT-4 with this prompt:

> You are an expert software engineer.  
> Analyze the following code and explain what it is doing and what kind of problem it helps solve.

---

### ✅ Step 4: Aggregate Summaries  
The tool collects all responses into a combined list.

---

### ✅ Step 5: Infer Project Purpose  
The summary list is sent back to GPT-4 with this prompt:

> Based on these summaries, what is the overall purpose of the codebase?  
> What problem is it solving?  
> Provide 2–3 sample runs with input/output, if possible.

---

## 🧠 Technologies Used

- Python 3.x
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4](https://platform.openai.com/)
- (Optional) Jupyter Notebook / IDE for script execution

---

## ▶️ How to Run

Right now, there's no CLI or web interface. You can run the script manually:

```bash
python analyze_code.py

To-Do / Roadmap
 Support zipped repositories or GitHub URLs

 Add CLI interface

 Add streamlit/gradio-based UI

 Integrate multiple models (e.g., Claude, Gemini)

 Auto-detect language and prompt accordingly


Feedback Welcome
This is an early-stage experiment.
If you're working on similar problems or have suggestions, feel free to contribute or reach out!

