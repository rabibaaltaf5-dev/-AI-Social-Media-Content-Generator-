# Offline AI Studio

**Offline AI Studio** is a GUI-based Python project that includes:

- Offline AI-style chatbot
- Social media content generator
- Caption generator
- Hashtag generator
- Post idea generator
- SQLite history
- Text export feature
- Attractive dashboard-style interface

This project is made for AI course demonstration and does **not require any API key, paid service, or internet connection**.

## Project Type

Rule-based Generative AI simulation using Python.

## Technologies Used

- Python
- Tkinter GUI
- SQLite database
- Random/template-based generation logic

## How to Run

### Method 1: Windows Easy Run
Double-click:

```bash
run_windows.bat
```

### Method 2: VS Code Terminal
Open the folder in VS Code and run:

```bash
python run.py
```

or:

```bash
py run.py
```

## Main Features

### 1. Offline Chatbot
The chatbot answers common questions about AI, projects, GitHub, presentation, Python, and content creation using keyword-based response matching.

### 2. Social Media Content Generator
The user enters a topic and selects:

- Platform: Instagram, Facebook, LinkedIn, YouTube
- Tone: Professional, Friendly, Motivational, Funny
- Length: Short, Medium, Long

The app generates:

- Caption/post
- Hashtags
- Post ideas
- Strategy tip

### 3. History
All chatbot and content generator outputs are saved in a local SQLite database.

### 4. Export
Generated chat/content can be exported as `.txt` files in the `exports` folder.

## Important Note

This project does not use ChatGPT, Gemini, or any online AI API. It simulates AI behavior through offline predefined responses and templates.

## Future Scope

- Add real local AI model support using Ollama
- Add voice input
- Add login system
- Add analytics for generated posts
- Add image generation support
- Add advanced NLP-based intent detection

## Presentation Explanation

This project demonstrates the concept of Generative AI in an offline environment. Instead of relying on paid APIs, it uses predefined templates, keyword detection, and platform-specific content rules to generate chatbot replies and social media posts.
