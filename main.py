"""
Offline AI Chatbot & Social Media Content Generator
---------------------------------------------------
A fully offline, API-free Python GUI project for AI course demos.
Built with Tkinter only, so it runs without installing extra packages.
"""

import json
import os
import random
import sqlite3
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

APP_NAME = "Offline AI Studio"
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"
DB_PATH = DATA_DIR / "app_history.db"

DATA_DIR.mkdir(exist_ok=True)
EXPORT_DIR.mkdir(exist_ok=True)

# ---------- Offline knowledge and generation data ----------
CHAT_KNOWLEDGE = {
    "hello": ["Hello! Main tumhara offline AI assistant hun. Aaj kis cheez me help chahiye?"],
    "hi": ["Hi! Main offline mode me chal raha hun, lekin smart predefined responses ke sath help kar sakta hun."],
    "salam": ["Wa Alaikum Salam! Batao jani, project, study, coding ya content me kya help chahiye?"],
    "assalam": ["Wa Alaikum Salam! Main ready hun. Tum question likho, main short aur useful answer dunga."],
    "project": [
        "Project ko strong banane ke liye clear problem statement, features, GUI, documentation aur demo flow zaroor add karo.",
        "Best project presentation me 4 cheezen honi chahiye: idea, working demo, technology stack, aur future scope."
    ],
    "ai": [
        "Artificial Intelligence ka matlab system ko itna smart banana ke wo data aur rules ke base par decision le sake.",
        "AI projects me automation, decision making, prediction, recommendation ya content generation jaisi cheezen show ki ja sakti hain."
    ],
    "chatbot": [
        "Chatbot ek software agent hota hai jo user ke message ko samajhne ki koshish karta hai aur relevant reply deta hai.",
        "Is project ka chatbot API use nahi karta; ye keywords aur predefined response patterns se offline reply generate karta hai."
    ],
    "content": [
        "Content generation ka purpose topic ke mutabiq captions, ideas, hashtags aur post text banana hota hai.",
        "Acha social media content clear hook, useful body aur strong call-to-action par based hota hai."
    ],
    "python": [
        "Python beginner-friendly language hai aur GUI, automation, AI demos aur data handling ke liye best choice hai.",
        "Is app me Python Tkinter GUI, SQLite database aur rule-based generation logic use hua hai."
    ],
    "github": [
        "GitHub par project upload karne ke liye repository banao, files add karo, commit karo aur README zaroor include karo.",
        "README me project title, features, installation, usage, screenshots aur future scope likhna professional lagta hai."
    ],
    "readme": [
        "README file project ka front page hoti hai. Isme project description, features, setup steps aur usage instructions honi chahiye."
    ],
    "presentation": [
        "Presentation me pehle problem explain karo, phir solution, features, demo, tools, limitations aur future improvements batana.",
        "Demo ke waqt short scenario use karo: topic do, caption generate karo, chatbot se project explain karwao, phir export show karo."
    ],
    "social media": [
        "Social media content me audience, platform, tone aur purpose important hota hai. Instagram casual, LinkedIn professional aur YouTube descriptive hota hai."
    ],
    "api": [
        "API ke baghair bhi demo project ban sakta hai, lekin output predefined rules aur templates par depend karega, live AI model par nahi."
    ],
    "offline": [
        "Offline project ka advantage ye hai ke internet, API key ya paid service ki zarurat nahi hoti. Demo stable rehta hai."
    ],
    "help": [
        "Tum mujhse project idea, AI explanation, caption ideas, GitHub steps, presentation tips aur study help puch sakte ho."
    ],
}

DEFAULT_CHAT_RESPONSES = [
    "Interesting question! Offline mode me main keyword-based logic use karta hun. Tum apna question thora specific likho to main better answer de sakta hun.",
    "Mere predefined knowledge base ke mutabiq, is topic ko simple explanation, example aur use-case ke sath present karna best hoga.",
    "Ye point project documentation me add kiya ja sakta hai. Iska benefit ye hai ke audience ko working aur purpose dono samajh aate hain.",
    "Main API-free assistant hun, isliye responses templates aur smart rules se generate karta hun. Class demo ke liye ye stable approach hai.",
]

HOOKS = {
    "Instagram": [
        "Stop scrolling — this one is worth your attention!",
        "Here is something simple but powerful about {topic}.",
        "Your next smart move starts with {topic}.",
        "Small idea, big impact: {topic}."
    ],
    "Facebook": [
        "Today we are sharing something useful about {topic}.",
        "Here is a simple thought that can make {topic} easier to understand.",
        "Let’s talk about why {topic} matters in everyday life.",
        "A helpful reminder for everyone interested in {topic}."
    ],
    "LinkedIn": [
        "{topic} is becoming an important part of modern digital growth.",
        "In today’s fast-changing world, {topic} plays a key role in innovation.",
        "A practical perspective on {topic} can help individuals and teams work smarter.",
        "Understanding {topic} is no longer optional; it is a valuable skill."
    ],
    "YouTube": [
        "In this video, we explain {topic} in a simple and practical way.",
        "Want to understand {topic} without confusion? This video is for you.",
        "Today’s topic is {topic}, and we will break it down step by step.",
        "Learn the basics, benefits, and real-life use of {topic} in this video."
    ],
}

TONE_BODY = {
    "Professional": [
        "This concept is useful because it saves time, improves decision-making, and creates better digital experiences.",
        "By applying it correctly, users can improve productivity and communicate their ideas more effectively.",
        "It also shows how technology can solve practical problems in a simple and organized way."
    ],
    "Friendly": [
        "The best part is that it is easy to understand and can be used by almost anyone.",
        "Whether you are a student, creator, or beginner, this idea can help you work smarter.",
        "Start small, stay consistent, and you will see improvement with time."
    ],
    "Motivational": [
        "Every big achievement starts with a small step, and learning this topic can be that step for you.",
        "Keep improving, keep experimenting, and do not be afraid to try new ideas.",
        "Progress comes when you take action, even if the first version is not perfect."
    ],
    "Funny": [
        "Honestly, once you understand it, you may wonder why it looked so scary before.",
        "It is like giving your brain a software update, but without waiting for Windows restart.",
        "Use it smartly, and you might look like the genius of the group project."
    ],
}

CTA = {
    "Instagram": ["Save this post for later!", "Share it with a friend who needs this.", "Follow for more smart ideas."],
    "Facebook": ["What do you think about this?", "Share your thoughts in the comments.", "Tag someone who should read this."],
    "LinkedIn": ["What are your thoughts on this approach?", "Let’s connect and discuss more ideas.", "How would you apply this in your workflow?"],
    "YouTube": ["Like, comment, and subscribe for more useful videos.", "Watch till the end for the full explanation.", "Comment your next topic suggestion below."],
}

HASHTAG_BANK = {
    "AI": ["#ArtificialIntelligence", "#AI", "#MachineLearning", "#TechInnovation", "#FutureTech"],
    "Education": ["#Education", "#Learning", "#Students", "#StudyTips", "#Knowledge"],
    "Business": ["#Business", "#Marketing", "#Growth", "#Entrepreneurship", "#Branding"],
    "Fitness": ["#Fitness", "#Health", "#Motivation", "#Lifestyle", "#Wellness"],
    "Default": ["#ContentCreation", "#DigitalMarketing", "#Productivity", "#CreativeIdeas", "#OnlineGrowth"]
}

POST_IDEAS = [
    "Create a carousel explaining 5 simple points about {topic}.",
    "Share a before/after comparison showing how {topic} solves a problem.",
    "Post a short story about a beginner learning {topic}.",
    "Make a checklist of mistakes to avoid in {topic}.",
    "Create a quick tutorial with 3 easy steps related to {topic}.",
    "Share a myth vs fact post about {topic}.",
]

# ---------- Database ----------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                input TEXT NOT NULL,
                output TEXT NOT NULL,
                created_at TEXT NOT NULL
            )"""
        )
        conn.commit()


def save_history(entry_type, user_input, output):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO history(type, input, output, created_at) VALUES (?, ?, ?, ?)",
            (entry_type, user_input, output, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )
        conn.commit()


def load_history(limit=30):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("SELECT type, input, output, created_at FROM history ORDER BY id DESC LIMIT ?", (limit,))
        return cur.fetchall()


def clear_history_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM history")
        conn.commit()

# ---------- Smart offline generation ----------
def chatbot_reply(message):
    msg = message.lower().strip()
    if not msg:
        return "Please pehle apna question likho."
    matches = []
    for key, responses in CHAT_KNOWLEDGE.items():
        if key in msg:
            matches.extend(responses)
    if "what is" in msg or "kya hai" in msg or "kia he" in msg:
        matches.append("Simple words me, ye ek concept hai jise real-life problem solve karne ke liye use kiya ja sakta hai. Example aur use-case ke sath explain karna best rahega.")
    if "how" in msg or "kaise" in msg or "kese" in msg:
        matches.append("Step-by-step approach follow karo: pehle requirement samjho, phir design banao, phir implementation, testing aur final documentation complete karo.")
    if "features" in msg or "feature" in msg:
        matches.append("Strong features me clean GUI, history saving, export option, search/filter, and simple user flow include karna chahiye.")
    if not matches:
        matches = DEFAULT_CHAT_RESPONSES
    response = random.choice(matches)
    tips = [
        "\n\nTip: Is point ko presentation me example ke sath explain karoge to zyada clear lagega.",
        "\n\nSuggestion: Is answer ko README ya project description me bhi use kiya ja sakta hai.",
        "\n\nNote: Ye app offline hai, isliye ye predefined intelligence aur keyword matching use kar rahi hai.",
    ]
    return response + random.choice(tips)


def detect_category(topic):
    t = topic.lower()
    if any(w in t for w in ["ai", "artificial", "chatbot", "machine", "robot", "automation"]):
        return "AI"
    if any(w in t for w in ["study", "school", "student", "education", "learning", "course"]):
        return "Education"
    if any(w in t for w in ["business", "brand", "sales", "marketing", "startup"]):
        return "Business"
    if any(w in t for w in ["fitness", "gym", "health", "diet", "workout"]):
        return "Fitness"
    return "Default"


def generate_content(topic, platform, tone, length):
    topic_clean = topic.strip().title() if topic.strip() else "Your Topic"
    hook = random.choice(HOOKS[platform]).format(topic=topic_clean)
    body_count = {"Short": 1, "Medium": 2, "Long": 3}.get(length, 2)
    body = " ".join(random.sample(TONE_BODY[tone], k=min(body_count, len(TONE_BODY[tone]))))
    cta = random.choice(CTA[platform])
    category = detect_category(topic_clean)
    hashtags = HASHTAG_BANK[category] + random.sample(HASHTAG_BANK["Default"], k=2)
    hashtags = list(dict.fromkeys(hashtags))[:7]
    ideas = [idea.format(topic=topic_clean) for idea in random.sample(POST_IDEAS, k=3)]
    caption = f"{hook}\n\n{body}\n\n{cta}"
    return (
        f"PLATFORM: {platform}\n"
        f"TONE: {tone}\n"
        f"TOPIC: {topic_clean}\n\n"
        f"CAPTION / POST:\n{caption}\n\n"
        f"HASHTAGS:\n{' '.join(hashtags)}\n\n"
        f"POST IDEAS:\n1. {ideas[0]}\n2. {ideas[1]}\n3. {ideas[2]}\n\n"
        f"CONTENT STRATEGY TIP:\nStart with a strong hook, keep the message simple, and end with a clear call-to-action."
    )

# ---------- GUI ----------
class OfflineAIStudio(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x720")
        self.minsize(980, 640)
        self.configure(bg="#101827")
        self.current_output = ""
        self._setup_style()
        self._build_layout()
        self.refresh_history()

    def _setup_style(self):
        self.colors = {
            "bg": "#101827",
            "panel": "#172033",
            "card": "#202b43",
            "accent": "#38bdf8",
            "accent2": "#a78bfa",
            "text": "#f8fafc",
            "muted": "#cbd5e1",
            "success": "#22c55e",
            "danger": "#fb7185",
        }
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", background="#26344f", foreground=self.colors["text"], padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.colors["accent"])], foreground=[("selected", "#06121f")])
        style.configure("TCombobox", fieldbackground="#0f172a", background="#0f172a", foreground=self.colors["text"], arrowcolor=self.colors["accent"])

    def _build_layout(self):
        root = tk.Frame(self, bg=self.colors["bg"])
        root.pack(fill="both", expand=True)

        sidebar = tk.Frame(root, bg="#0b1220", width=285)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="⚡ Offline AI Studio", bg="#0b1220", fg=self.colors["text"], font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=24, pady=(28, 4))
        tk.Label(sidebar, text="Chatbot + Content Generator\nNo API • No Internet • Python GUI", bg="#0b1220", fg=self.colors["muted"], font=("Segoe UI", 10), justify="left").pack(anchor="w", padx=24, pady=(0, 24))

        self._info_card(sidebar, "Project Type", "Rule-based Generative AI Demo")
        self._info_card(sidebar, "Database", "SQLite history storage")
        self._info_card(sidebar, "Best For", "AI course presentation")

        tk.Label(sidebar, text="Demo Script", bg="#0b1220", fg=self.colors["accent"], font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=24, pady=(20, 6))
        script = "1. Ask chatbot about AI\n2. Generate Instagram caption\n3. Export output\n4. Show history tab"
        tk.Label(sidebar, text=script, bg="#0b1220", fg=self.colors["muted"], font=("Segoe UI", 10), justify="left").pack(anchor="w", padx=24)

        main = tk.Frame(root, bg=self.colors["bg"])
        main.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        header = tk.Frame(main, bg=self.colors["bg"])
        header.pack(fill="x")
        tk.Label(header, text="AI Chatbot & Social Media Content Generator", bg=self.colors["bg"], fg=self.colors["text"], font=("Segoe UI", 22, "bold")).pack(anchor="w")
        tk.Label(header, text="A fully offline project that simulates generative AI using smart templates and keyword-based responses.", bg=self.colors["bg"], fg=self.colors["muted"], font=("Segoe UI", 11)).pack(anchor="w", pady=(4, 14))

        self.notebook = ttk.Notebook(main)
        self.notebook.pack(fill="both", expand=True)

        self.chat_tab = tk.Frame(self.notebook, bg=self.colors["panel"])
        self.content_tab = tk.Frame(self.notebook, bg=self.colors["panel"])
        self.history_tab = tk.Frame(self.notebook, bg=self.colors["panel"])
        self.about_tab = tk.Frame(self.notebook, bg=self.colors["panel"])

        self.notebook.add(self.chat_tab, text="💬 Chatbot")
        self.notebook.add(self.content_tab, text="✍️ Content Generator")
        self.notebook.add(self.history_tab, text="📚 History")
        self.notebook.add(self.about_tab, text="ℹ️ About")

        self._build_chat_tab()
        self._build_content_tab()
        self._build_history_tab()
        self._build_about_tab()

    def _info_card(self, parent, title, value):
        card = tk.Frame(parent, bg=self.colors["card"])
        card.pack(fill="x", padx=20, pady=8)
        tk.Label(card, text=title, bg=self.colors["card"], fg=self.colors["accent"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=14, pady=(10, 0))
        tk.Label(card, text=value, bg=self.colors["card"], fg=self.colors["text"], font=("Segoe UI", 10)).pack(anchor="w", padx=14, pady=(3, 10))

    def _button(self, parent, text, command, bg=None):
        return tk.Button(parent, text=text, command=command, bg=bg or self.colors["accent"], fg="#06121f", activebackground=self.colors["accent2"], activeforeground="#06121f", relief="flat", padx=14, pady=9, font=("Segoe UI", 10, "bold"), cursor="hand2")

    def _text_widget(self, parent, height=12):
        text = tk.Text(parent, height=height, bg="#0f172a", fg=self.colors["text"], insertbackground=self.colors["accent"], relief="flat", wrap="word", font=("Consolas", 10), padx=12, pady=12)
        return text

    def _build_chat_tab(self):
        container = tk.Frame(self.chat_tab, bg=self.colors["panel"])
        container.pack(fill="both", expand=True, padx=22, pady=22)
        tk.Label(container, text="Offline AI Chatbot", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(container, text="Ask about AI, projects, GitHub, presentations, Python, chatbot, or content creation.", bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 12))

        self.chat_display = self._text_widget(container, height=20)
        self.chat_display.pack(fill="both", expand=True)
        self.chat_display.insert("end", "Assistant: Salam! Main offline AI assistant hun. Apna question likho.\n\n")
        self.chat_display.config(state="disabled")

        bottom = tk.Frame(container, bg=self.colors["panel"])
        bottom.pack(fill="x", pady=(12, 0))
        self.chat_entry = tk.Entry(bottom, bg="#0f172a", fg=self.colors["text"], insertbackground=self.colors["accent"], relief="flat", font=("Segoe UI", 11))
        self.chat_entry.pack(side="left", fill="x", expand=True, ipady=12, padx=(0, 10))
        self.chat_entry.bind("<Return>", lambda e: self.send_chat())
        self._button(bottom, "Send", self.send_chat).pack(side="left", padx=4)
        self._button(bottom, "Clear", self.clear_chat, bg="#334155").pack(side="left", padx=4)
        self._button(bottom, "Export", self.export_chat, bg=self.colors["success"]).pack(side="left", padx=4)

    def _build_content_tab(self):
        container = tk.Frame(self.content_tab, bg=self.colors["panel"])
        container.pack(fill="both", expand=True, padx=22, pady=22)
        tk.Label(container, text="Social Media Content Generator", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 18, "bold")).pack(anchor="w")
        tk.Label(container, text="Generate captions, hashtags, post ideas, and strategy tips using offline templates.", bg=self.colors["panel"], fg=self.colors["muted"], font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 12))

        form = tk.Frame(container, bg=self.colors["card"])
        form.pack(fill="x", pady=(0, 14))
        for i in range(8):
            form.grid_columnconfigure(i, weight=1)

        tk.Label(form, text="Topic", bg=self.colors["card"], fg=self.colors["muted"], font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))
        self.topic_entry = tk.Entry(form, bg="#0f172a", fg=self.colors["text"], insertbackground=self.colors["accent"], relief="flat", font=("Segoe UI", 11))
        self.topic_entry.grid(row=1, column=0, columnspan=3, sticky="ew", padx=14, pady=(0, 14), ipady=9)
        self.topic_entry.insert(0, "AI for students")

        tk.Label(form, text="Platform", bg=self.colors["card"], fg=self.colors["muted"], font=("Segoe UI", 10, "bold")).grid(row=0, column=3, sticky="w", padx=10, pady=(12, 4))
        self.platform_var = tk.StringVar(value="Instagram")
        ttk.Combobox(form, textvariable=self.platform_var, values=["Instagram", "Facebook", "LinkedIn", "YouTube"], state="readonly").grid(row=1, column=3, sticky="ew", padx=10, pady=(0, 14), ipady=7)

        tk.Label(form, text="Tone", bg=self.colors["card"], fg=self.colors["muted"], font=("Segoe UI", 10, "bold")).grid(row=0, column=4, sticky="w", padx=10, pady=(12, 4))
        self.tone_var = tk.StringVar(value="Professional")
        ttk.Combobox(form, textvariable=self.tone_var, values=["Professional", "Friendly", "Motivational", "Funny"], state="readonly").grid(row=1, column=4, sticky="ew", padx=10, pady=(0, 14), ipady=7)

        tk.Label(form, text="Length", bg=self.colors["card"], fg=self.colors["muted"], font=("Segoe UI", 10, "bold")).grid(row=0, column=5, sticky="w", padx=10, pady=(12, 4))
        self.length_var = tk.StringVar(value="Medium")
        ttk.Combobox(form, textvariable=self.length_var, values=["Short", "Medium", "Long"], state="readonly").grid(row=1, column=5, sticky="ew", padx=10, pady=(0, 14), ipady=7)

        self._button(form, "Generate", self.generate_social_content).grid(row=1, column=6, sticky="ew", padx=10, pady=(0, 14))
        self._button(form, "Export", self.export_current_output, bg=self.colors["success"]).grid(row=1, column=7, sticky="ew", padx=14, pady=(0, 14))

        self.content_output = self._text_widget(container, height=20)
        self.content_output.pack(fill="both", expand=True)

        actions = tk.Frame(container, bg=self.colors["panel"])
        actions.pack(fill="x", pady=(10, 0))
        self._button(actions, "Copy Output", self.copy_output, bg=self.colors["accent2"]).pack(side="left")
        self._button(actions, "Clear Output", lambda: self.content_output.delete("1.0", "end"), bg="#334155").pack(side="left", padx=10)

    def _build_history_tab(self):
        container = tk.Frame(self.history_tab, bg=self.colors["panel"])
        container.pack(fill="both", expand=True, padx=22, pady=22)
        top = tk.Frame(container, bg=self.colors["panel"])
        top.pack(fill="x")
        tk.Label(top, text="Saved History", bg=self.colors["panel"], fg=self.colors["text"], font=("Segoe UI", 18, "bold")).pack(side="left")
        self._button(top, "Refresh", self.refresh_history).pack(side="right", padx=5)
        self._button(top, "Clear All", self.clear_all_history, bg=self.colors["danger"]).pack(side="right", padx=5)

        self.history_box = self._text_widget(container, height=24)
        self.history_box.pack(fill="both", expand=True, pady=(14, 0))

    def _build_about_tab(self):
        container = tk.Frame(self.about_tab, bg=self.colors["panel"])
        container.pack(fill="both", expand=True, padx=28, pady=28)
        about = """PROJECT DESCRIPTION
Offline AI Studio is a GUI-based Python project that combines an AI-style chatbot and a social media content generator. It is designed for students who want to demonstrate Generative AI concepts without paid APIs or internet dependency.

HOW IT WORKS
The chatbot uses keyword matching and predefined intelligent responses. The content generator uses smart templates, platform-specific hooks, tone-based body text, hashtags, and post ideas.

MAIN FEATURES
• Offline chatbot
• Social media caption generator
• Hashtag generator
• Post idea generator
• SQLite history
• Export output as TXT files
• Attractive dashboard-style GUI
• No API key required

LIMITATION
This is not a real LLM like ChatGPT or Gemini. It is an offline simulation of AI behavior using rules and templates. For a real AI model, an API or local LLM such as Ollama can be added in future scope.

FUTURE SCOPE
• Add real local AI model support
• Add voice input
• Add image post generator
• Add analytics for generated content
• Add login system and cloud sync
"""
        text = self._text_widget(container, height=28)
        text.pack(fill="both", expand=True)
        text.insert("end", about)
        text.config(state="disabled")

    def send_chat(self):
        msg = self.chat_entry.get().strip()
        if not msg:
            return
        reply = chatbot_reply(msg)
        self.chat_display.config(state="normal")
        self.chat_display.insert("end", f"You: {msg}\n")
        self.chat_display.insert("end", f"Assistant: {reply}\n\n")
        self.chat_display.see("end")
        self.chat_display.config(state="disabled")
        self.chat_entry.delete(0, "end")
        save_history("Chatbot", msg, reply)
        self.refresh_history()

    def clear_chat(self):
        self.chat_display.config(state="normal")
        self.chat_display.delete("1.0", "end")
        self.chat_display.insert("end", "Assistant: Chat cleared. New question likho.\n\n")
        self.chat_display.config(state="disabled")

    def export_chat(self):
        content = self.chat_display.get("1.0", "end").strip()
        self._export_text(content, "chat_export")

    def generate_social_content(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showwarning("Missing Topic", "Please topic enter karo.")
            return
        output = generate_content(topic, self.platform_var.get(), self.tone_var.get(), self.length_var.get())
        self.current_output = output
        self.content_output.delete("1.0", "end")
        self.content_output.insert("end", output)
        save_history("Content", topic, output)
        self.refresh_history()

    def copy_output(self):
        output = self.content_output.get("1.0", "end").strip()
        if output:
            self.clipboard_clear()
            self.clipboard_append(output)
            messagebox.showinfo("Copied", "Output clipboard me copy ho gaya.")

    def export_current_output(self):
        output = self.content_output.get("1.0", "end").strip()
        if not output:
            messagebox.showwarning("No Output", "Export se pehle content generate karo.")
            return
        self._export_text(output, "content_export")

    def _export_text(self, content, prefix):
        if not content:
            messagebox.showwarning("No Content", "Export karne ke liye content available nahi.")
            return
        filename = f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        path = EXPORT_DIR / filename
        path.write_text(content, encoding="utf-8")
        messagebox.showinfo("Exported", f"File saved:\n{path}")

    def refresh_history(self):
        if not hasattr(self, "history_box"):
            return
        rows = load_history()
        self.history_box.config(state="normal")
        self.history_box.delete("1.0", "end")
        if not rows:
            self.history_box.insert("end", "No history yet. Generate content or chat to save entries.\n")
        for entry_type, user_input, output, created_at in rows:
            self.history_box.insert("end", f"[{created_at}] {entry_type}\n")
            self.history_box.insert("end", f"INPUT: {user_input}\n")
            self.history_box.insert("end", f"OUTPUT: {output[:650]}{'...' if len(output) > 650 else ''}\n")
            self.history_box.insert("end", "-" * 90 + "\n\n")
        self.history_box.config(state="disabled")

    def clear_all_history(self):
        if messagebox.askyesno("Confirm", "Saari history delete karni hai?"):
            clear_history_db()
            self.refresh_history()


def main():
    init_db()
    app = OfflineAIStudio()
    app.mainloop()


if __name__ == "__main__":
    main()
