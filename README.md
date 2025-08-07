# 🔍 AI-Powered Scala Codebase Analysis using GPT-4 + LangChain

This project demonstrates how to use **GPT-4** and **LangChain** to analyze a Scala codebase with **no documentation, comments, or tests**, and derive its **overall purpose and problem statement**.

---

## 📌 Objective

To determine whether a large language model (LLM), specifically **GPT-4**, can understand a legacy or undocumented Scala project by:

- Analyzing its source code in isolated chunks
- Summarizing each piece
- Synthesizing the overall intent of the project
- Generating example runs (inputs/outputs)

---

## 🚀 Steps Performed

### ✅ Step 1: Read the Code  
The Scala source code was fetched from a GitHub repository.  
To simulate a real-world challenge, **all comments, test cases, and README files were intentionally removed.**

---

### ✅ Step 2: Split Into Chunks  
To avoid exceeding GPT-4’s context window (token limit), the source code was split into smaller **chunks** using LangChain’s `RecursiveCharacterTextSplitter`.

---

### ✅ Step 3: Analyze Each Chunk  
Each chunk was sent to GPT-4 with the following prompt:

> You are an expert in Scala programming.  
> Analyze the following code and explain what it is doing and what kind of problem it helps solve.

---

### ✅ Step 4: Aggregate Summaries  
All chunk-level responses were collected into a single summary list.

---

### ✅ Step 5: Infer Overall Purpose  
The combined summaries were passed back to GPT-4 with this meta-prompt:

> Based on these summaries, what is the overall purpose of the codebase?  
> What problem is it solving?  
> Also, give 3 example runs with input and output if possible.

---

## 🧠 Technologies Used

- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4](https://platform.openai.com/docs/models/gpt-4)
- Python (LangChain orchestration)
- Scala (target codebase)

---

## 📁 Folder Structure


