import os
import gradio as gr
import litellm

MODEL = "gemini/gemini-3.8-flash"
SYSTEM = (
    "তুমি 'কৃষিসঙ্গী' — বাংলাদেশের কৃষকদের জন্য কৃষি পরামর্শদাতা। "
    "ধানের চাষ, সার, রোগবালাই, আবহাওয়া নিয়ে সংক্ষিপ্ত, ব্যবহারিক পরামর্শ দাও বাংলায়। "
    "নিশ্চিত না হলে কৃষি অফিসে যোগাযোগ করতে বলো।"
)

def ask_krishi(question: str) -> str:
    r = litellm.completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user",   "content": question},
        ],
    )
    return r.choices[0].message.content

def chat_fn(message, history):
    try:
        return ask_krishi(message)
    except Exception as e:
        return f"দুঃখিত, একটি সমস্যা হয়েছে: {e}"

demo = gr.ChatInterface(
    fn=chat_fn,
    title="কৃষিসঙ্গী (KrishiShongi)",
    description=(
        "বাংলাদেশের কৃষকদের জন্য কৃষি পরামর্শ। "
        "ধানের চাষ, সার, রোগবালাই, আবহাওয়া — যেকোনো প্রশ্ন করুন বাংলায়।"
    ),
    examples=[
        "ধানের পাতা হলুদ হয়ে যাচ্ছে, কী করব?",
        "বোরো ধানে ইউরিয়া কখন দিতে হয়?",
        "পোকা দমনে কী কী ব্যবস্থা নিতে পারি?",
    ],
)

# Render provides $PORT; bind to 0.0.0.0 so it's reachable
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    theme=gr.themes.Soft(),
)
