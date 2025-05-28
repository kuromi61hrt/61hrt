# 61hrt: The First Ever Transparent AI

## Overview

Most Large Language Models (LLMs) today operate as opaque systems — they provide answers, but not the reasoning behind them. Whether used in education, research, or decision-making, this black-box behavior limits trust and usability. Users often ask:  
**"Why did the model say this?"** or **"Can I trust this answer?"**

**61hrt** is built to challenge that. It’s a lightweight, fully transparent AI interface that not only delivers answers but also **breaks down its reasoning step-by-step**, cites its **information sources**, and shows **probabilities behind its thinking**. Inspired by Explainable AI (XAI) principles, 61hrt lets users **see how the model thinks**.

The model backend is powered by **Perplexity’s Sonar API**, known for its quality open-domain reasoning and source grounding. The front-end is designed using **Streamlit**, with a custom **monochrome interface** and minimalistic layout to reflect the model's clarity and purpose.

---

## Key Features

### ✅ Explainable Thought Process  
- The AI breaks down each step of its reasoning and decision-making process in detail.

### ✅ Source Transparency  
- Shows the exact sources the model refers to (with links), allowing users to verify the information.

### ✅ Confidence Estimates  
- Probabilities are given at each reasoning step, reflecting the model’s certainty.

### ✅ Final Answer  
- A clear, concise final answer is provided separately after the explanation.

### ✅ Custom Monochrome UI  
- Styled using HTML/CSS injected into Streamlit to offer a sharp, focused interface.

### ✅ Chat History + Recycle Bin + Archive  
- Sidebar includes full session memory management for professional workflows.

---

## Why 61hrt?

While most LLM chat interfaces behave like oracles—producing answers without context—**61hrt** is designed as a **thinking companion**.

This makes it valuable for:
- Researchers and analysts verifying factual accuracy  
- Students learning how reasoning chains work  
- Developers building transparent AI pipelines  

---

## Built With

- [Streamlit](https://streamlit.io/) — For creating the interactive web app  
- [Perplexity AI Sonar API](https://docs.perplexity.ai/) — LLM API backend for reasoning and source citations  
- Python 3.8+

---

