# 🔋 Fuzzy AI Battery Optimizer

A mini AI + Fuzzy Logic project that analyzes a user's natural-language description of smartphone battery usage and produces a Power-Saving Score.

The project combines LangChain + Google Gemini for natural-language understanding with a genuine Fuzzy Inference System for approximate reasoning.

---

## 👨‍🎓 Student Details

- **Student Name:** Antony Alwin
- **Roll Number:** 19032
- **Course:** BSc IT
- **Subject:** IKS

---

## 🚀 Live Demo

https://fuzzy-ai-battery-optimizer-29dxz5ppesx3zovdfxabsw.streamlit.app

---

## 💻 GitHub Repository

https://github.com/alwin2006264/fuzzy-ai-battery-optimizer

---

## 📌 Project Description

Smartphone battery drain depends on several factors such as:

- Battery level
- Application usage
- Screen usage
- Network usage
- Device temperature

Instead of using only rigid threshold-based decisions, this project uses fuzzy logic to represent conditions such as low, medium, high, hot, very low, and extreme.

The user can describe their current phone usage using normal language.

For example:

> My battery is 18%. I've been playing games for two hours, brightness is high, mobile data is on and my phone is getting very hot.

The AI component extracts structured numerical information from this description. The fuzzy inference system then processes those values and calculates a Power-Saving Score from 0 to 100.

---AI Extracted Inputs
Battery       : 18.0%
App Usage     : 90.0%
Screen Usage  : 80.0%
Network Usage : 80.0%
Temperature   : 45.0°C
Fuzzy Logic Result
Power-Saving Score: 87.47 / 100
Rule Activation
None    : 0
Low     : 0
Medium  : 0
High    : 0.4
Extreme : 1.0
🧠 Fuzzy Logic System
The fuzzy system uses five input variables.
Battery
Very Low
Low
Medium
High
Application Usage
Low
Medium
High
Screen Usage
Low
Medium
High
Network Usage
Low
Medium
High
Temperature
Cool
Normal
Hot
The output variable is Power-Saving with:
None
Low
Medium
High
Extreme

## ✨ Main Features

### 🤖 AI / LLM Natural-Language Processing

- Uses LangChain with Google Gemini.
- Accepts natural-language battery descriptions.
- Extracts five structured input values.
- Uses Pydantic validation.
- Provides a local fallback parser if the Gemini request is unavailable.

### 🧠 Fuzzy Logic

- Genuine fuzzy inference system using scikit-fuzzy.
- Uses triangular and trapezoidal membership functions.
- Performs fuzzification.
- Contains 20 fuzzy rules.
- Uses fuzzy AND through minimum membership.
- Uses maximum aggregation for output categories.
- Uses centroid defuzzification.
- Produces a Power-Saving Score from 0 to 100.

### 🌐 Web Interface

- Built using Streamlit.
- Simple natural-language input interface.
- Displays AI-extracted values.
- Displays membership values.
- Displays rule activation values.
- Displays final Power-Saving Score.

### ☁️ Free Deployment

- Source code hosted on GitHub.
- Application deployed using Streamlit Community Cloud.

---

## 🛠️ Technologies / Tech Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web user interface |
| LangChain | LLM integration |
| Google Gemini | Natural-language understanding |
| Pydantic | Structured data validation |
| scikit-fuzzy | Fuzzy inference |
| NumPy | Numerical operations |
| SciPy | Scientific computing dependency |
| FastAPI | Backend/API support |
| Uvicorn | ASGI server |
| python-dotenv | Environment variable management |
| Git/GitHub | Version control and source hosting |
| Streamlit Community Cloud | Free live deployment |

---

## 📂 Project Structure

```text
fuzzy-ai-battery-optimizer/
│
├── app.py
├── main.py
├── ai_parser.py
├── fuzzy_system.py
├── backend.py
├── api.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env