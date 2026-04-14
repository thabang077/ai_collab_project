import gradio as gr
import random
from ai_module import (
    ask_ai, PROVIDERS, DEFAULT_PROVIDER,
    detect_suggested_provider,
)
from main import (
    get_ai_joke, get_ai_roast,
    MOODS,
)

VERSION = "1.3.0"

def chat(message, history, provider, mood):
    msg = message.strip()
    if not msg:
        return "", history

    lower = msg.lower()

    if lower in ("joke", "jokes"):
        setup, punchline = get_ai_joke()
        reply = f"😂 **{setup}**\n\n{punchline}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        return "", history

    if lower in ("roast", "roast me") or lower.startswith("roast "):
        target = msg[6:].strip() if lower.startswith("roast ") and lower != "roast me" else "you"
        roast  = get_ai_roast(target)
        reply  = f"🔥 **[{target}]** {roast}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": reply})
        return "", history

    if lower == "providers":
        lines = ["**Available AI Providers:**\n"]
        for key, info in PROVIDERS.items():
            active = " ◀ **active**" if key == provider else ""
            lines.append(f"{info['icon']} **{info['label']}** — {info['tagline']}  `{key}`{active}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "\n".join(lines)})
        return "", history

    if lower == "moods":
        lines = ["**Available Moods:**\n"]
        for m, desc in MOODS.items():
            lines.append(f"• **{m}** — {desc[:60] + '…' if len(desc) > 60 else desc or 'Default tone'}")
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": "\n".join(lines)})
        return "", history

    if lower == "version":
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": f"🤖 AI CLI Assistant v{VERSION}"})
        return "", history

    if lower == "help":
        help_text = (
            "**Commands:**\n"
            "• `joke` — Get a random joke\n"
            "• `roast me` — Get roasted 🔥\n"
            "• `roast <name>` — Roast someone by name\n"
            "• `providers` — List all AI providers\n"
            "• `moods` — List all moods\n"
            "• `version` — Show version\n\n"
            "---\n\n"
            "**🔀 AI Providers — which one to use?**\n\n"
            "🟢 **GPT-4o (chatgpt)** — Best all-rounder. Great for writing, research, summaries, and general questions. Use this when you're unsure.\n\n"
            "🟡 **Qwen3 Coder 30B (mini)** — Built for code. Use it for writing functions, fixing bugs, explaining code, or anything programming-related.\n\n"
            "🔵 **HuggingSpace Command-A (reasoning)** — Best for heavy thinking. Use it for math problems, logic puzzles, equations, and step-by-step reasoning.\n\n"
            "💡 **How to switch providers:** Use the **Provider** dropdown in the sidebar — just click it and pick one. "
            "The assistant will also suggest the best provider automatically based on what you type."
        )
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": help_text})
        return "", history

    # ── Smart provider suggestion ─────────────────────────────────
    suggested = detect_suggested_provider(msg)
    note = ""
    if suggested and suggested != provider:
        sug = PROVIDERS[suggested]
        note = f"> 💡 *Tip: **{sug['icon']} {sug['label']}** is better for {sug['best_for']}. Switch AI provider in the sidebar.*\n\n"

    # ── Ask AI ────────────────────────────────────────────────────
    query = MOODS[mood] + msg
    try:
        response = ask_ai(query, provider=provider)
    except Exception as e:
        response = f"Error: {e}"

    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": note + response})
    return "", history


# ── UI — Gradio 6 compatible ──────────────────────────────────────
with gr.Blocks(title="🤖 AI CLI Assistant") as demo:
    gr.Markdown("# 🤖 AI CLI Assistant\nChat with multiple AI providers. Try `joke`, `roast me`, or `help`.")

    with gr.Row():
        with gr.Column(scale=1):
            provider_dd = gr.Dropdown(
                choices=list(PROVIDERS.keys()),
                value=DEFAULT_PROVIDER,
                label="🔀 Provider",
                info="Switch AI provider",
                allow_custom_value=False,
            )
            mood_dd = gr.Dropdown(
                choices=list(MOODS.keys()),
                value="default",
                label="🎭 Mood",
                info="Change response style",
                allow_custom_value=False,
            )
            gr.Markdown("**Quick Commands:**")
            joke_btn  = gr.Button("😂 Joke")
            roast_btn = gr.Button("🔥 Roast Me")
            help_btn  = gr.Button("❓ Help")

        with gr.Column(scale=3):
            chatbot = gr.Chatbot(height=480, label="Chat")
            with gr.Row():
                msg_box = gr.Textbox(
                    placeholder="Ask anything or type a command…",
                    show_label=False,
                    scale=5
                )
                send_btn = gr.Button("Send", variant="primary", scale=1)

    send_btn.click(chat, [msg_box, chatbot, provider_dd, mood_dd], [msg_box, chatbot])
    msg_box.submit(chat, [msg_box, chatbot, provider_dd, mood_dd], [msg_box, chatbot])

    joke_btn.click( lambda h, p, m: chat("joke",     h, p, m), [chatbot, provider_dd, mood_dd], [msg_box, chatbot])
    roast_btn.click(lambda h, p, m: chat("roast me", h, p, m), [chatbot, provider_dd, mood_dd], [msg_box, chatbot])
    help_btn.click( lambda h, p, m: chat("help",     h, p, m), [chatbot, provider_dd, mood_dd], [msg_box, chatbot])

demo.launch()
