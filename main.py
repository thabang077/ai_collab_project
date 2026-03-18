from ai_module import ask_ai
import os
import sys
import random
import re
import json
from datetime import datetime

# ── Version ────────────────────────────────────────────────────
VERSION = "1.3.0"

# ── ANSI Colors ────────────────────────────────────────────────
CYAN    = "\033[96m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
RED     = "\033[91m"
MAGENTA = "\033[95m"
BLUE    = "\033[94m"
WHITE   = "\033[97m"
ORANGE  = "\033[33m"
PINK    = "\033[38;5;213m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RESET   = "\033[0m"

# ── Color name → ANSI map (used by `color` command) ────────────
COLOR_MAP = {
    "cyan":    CYAN,
    "green":   GREEN,
    "yellow":  YELLOW,
    "red":     RED,
    "magenta": MAGENTA,
    "blue":    BLUE,
    "white":   WHITE,
    "orange":  ORANGE,
    "pink":    PINK,
}

# ── Themes ─────────────────────────────────────────────────────
# dark=pink, sunset=orange, ocean=blue
THEMES = {
    "default": {"user": YELLOW, "ai": GREEN,  "system": CYAN},
    "dark":    {"user": PINK,   "ai": PINK,   "system": PINK},
    "hacker":  {"user": GREEN,  "ai": GREEN,  "system": GREEN},
    "ocean":   {"user": BLUE,   "ai": BLUE,   "system": BLUE},
    "sunset":  {"user": ORANGE, "ai": ORANGE, "system": ORANGE},
}

PROMPT_STYLES = ["classic", "arrow", "simple", "minimal", "bracket"]

AI_NAMES = [
    "Nova", "Orion", "Atlas", "Echo", "Zenith",
    "Pixel", "Astra", "Cosmo", "Nimbus", "Luna",
]

# ── Mood map (prefixed to user query before ask_ai) ────────────
MOODS = {
    "default":  "",
    "concise":  (
        "Be extremely concise. Answer in one or two sentences max. "
        "No fluff, no preamble, straight to the point. "
    ),
    "formal": (
        "Respond in a polished, professional, and formal tone. "
        "Use complete sentences, avoid contractions, and maintain decorum. "
    ),
    "friendly": (
        "Respond in a warm, casual, and upbeat tone — like texting a good friend. "
        "Use light humor where natural, keep it approachable and encouraging. "
    ),
    "funny": (
        "Reply with wit, sarcasm, and sharp humor. Slip in a clever joke or pun if it fits. "
        "Keep it entertaining while still being helpful. "
    ),
    "teacher": (
        "Explain as if the person is a complete beginner with zero prior knowledge. "
        "Use simple language, relatable analogies, and short examples. Avoid jargon. "
    ),
    "expert": (
        "Assume the person is a domain expert. Skip basics, use precise technical language, "
        "reference advanced concepts freely, and be thorough. "
    ),
}


# ── Helpers ────────────────────────────────────────────────────

def sys_msg(color, text):
    """Print a colored system message."""
    print(f"{color}{text}{RESET}")

def divider(color=DIM):
    print(f"{color}{'─' * 44}{RESET}")


# ── Hardcoded Badass Jokes (fallback + random pool) ────────────
HARDCODED_JOKES = [
    (
        "I asked God for a bike, but I know God doesn't work that way.",
        "So I stole a bike and asked for forgiveness."
    ),
    (
        "My therapist says I have a preoccupation with vengeance.",
        "We'll see about that."
    ),
    (
        "Why do orphans love boomerangs?",
        "It's the only thing that ever comes back."
    ),
    (
        "I told my wife she should embrace her mistakes.",
        "She gave me a hug."
    ),
    (
        "What's the difference between a pizza and my ex?",
        "A pizza can actually feed a family."
    ),
    (
        "Scientists say the universe is made of protons, neutrons, and electrons.",
        "They forgot to mention morons."
    ),
    (
        "My doctor told me I need to watch my drinking.",
        "So now I do it in front of a mirror."
    ),
    (
        "I tried to write a joke about unemployment.",
        "It didn't work out."
    ),
    (
        "What's the difference between a good programmer and a bad programmer?",
        "About three Stack Overflow tabs."
    ),
    (
        "Why did the existentialist fail the exam?",
        "He left it blank — nothing has meaning anyway."
    ),
    (
        "My wife said I had to stop acting like a flamingo.",
        "I had to put my foot down."
    ),
    (
        "How many narcissists does it take to change a light bulb?",
        "One. They hold the bulb and wait for the world to revolve around them."
    ),
    (
        "I told my boss three companies were after me and I needed a raise.",
        "He asked which companies. I said: gas, electric, and water."
    ),
    (
        "Why did the software developer go broke?",
        "Because he cleared his cache and cookies and lost everything."
    ),
    (
        "My life coach told me to write a letter to the person who hurt me most.",
        "I'm now waiting for the mailman to deliver it to myself."
    ),
]

# ── Hardcoded Savage Roasts (fallback + random pool) ───────────
HARDCODED_ROASTS = [
    "You're not the dumbest person alive, but you better hope they don't die.",
    "Your birth certificate is an apology letter from the hospital.",
    "You have the energy of a low-battery notification — always dying, never actually shutting up.",
    "You're the reason instructions on shampoo bottles say 'repeat' — someone had to dumb it down for you.",
    "Your LinkedIn says 'open to opportunities' because even your career ghosted you.",
    "Somewhere a tree is working overtime producing oxygen just for you, and it deeply regrets it.",
    "You're the human equivalent of a software update at 2 AM — nobody asked for you, you take forever, and you barely improve anything.",
    "You're proof that evolution occasionally hits Ctrl+Z.",
    "Your parents looked at you and invented the phrase 'unconditional love' — because no conditions would've kept them around.",
    "You're like a cloud — when you disappear, it's a beautiful day.",
    "The only thing your ex misses about you is the feeling of not having you around.",
    "You have a face made for radio and a voice made for text.",
    "I'd roast you properly but my therapist says I need to stop setting fire to garbage.",
    "You're the type who gets outsmarted by a CAPTCHA on a daily basis.",
    "NASA is studying you — not because you're special, but because they've never seen a black hole with a LinkedIn profile.",
]

# ── Joke Style Selector ────────────────────────────────────────
JOKE_STYLES = [
    "misdirection — the setup sounds totally innocent, then the punchline is a gut punch from nowhere",
    "dark irony — the darkest possible interpretation of an everyday situation",
    "absurdist logic taken to its horrifying natural conclusion",
    "a fake-deep observation about life that ends in pure nihilistic chaos",
    "self-aware meta humor where the joke eats itself alive",
    "a savage comparison that makes you feel personally attacked and laughing at the same time",
]

# ── Roast Style Selector ───────────────────────────────────────
ROAST_STYLES = [
    "surgical precision — one quiet, specific observation that dismantles their entire identity",
    "fake compliment that flips into a devastating gut punch in the last four words",
    "existential dread — make them question why they were born and what they're doing with their life",
    "statistical improbability — frame how astronomically unlikely it is that they turned out this bad",
    "tech/software metaphor — compare them to the most broken, unwanted piece of software imaginable",
    "comparison to something universally disappointing, useless, or abandoned",
]

# ── AI-powered Joke ────────────────────────────────────────────
def get_ai_joke():
    """70% AI-generated, 30% hardcoded — always nuclear-level funny."""
    # 30% chance: use a hardcoded banger for instant delivery
    if random.random() < 0.30:
        return random.choice(HARDCODED_JOKES)

    style = random.choice(JOKE_STYLES)
    examples = random.sample(HARDCODED_JOKES, 2)
    ex1 = f"Q: {examples[0][0]}\nA: {examples[0][1]}"
    ex2 = f"Q: {examples[1][0]}\nA: {examples[1][1]}"

    prompt = (
        "You are a battle-hardened stand-up comedian who has performed at the Comedy Cellar, "
        "roasted celebrities on live TV, and never once told a safe joke. "
        "Your jokes have made people spit out drinks, miss their subway stop, and text the joke "
        "to five people immediately. You do not do mild. You do not do safe. "
        "You only produce jokes that hit like a freight train.\n\n"
        f"Style for this joke: {style}\n\n"
        "Here are two examples of the MINIMUM quality I expect:\n"
        f"{ex1}\n"
        f"{ex2}\n\n"
        "Now write ONE original joke that is FUNNIER and MORE UNEXPECTED than both examples above. "
        "The punchline must be something nobody sees coming. "
        "NO recycled jokes. NO safe territory. If it doesn't make someone wheeze with laughter "
        "or feel slightly attacked, it's not good enough — try harder.\n\n"
        "Format EXACTLY as:\n"
        "Q: <setup>\n"
        "A: <punchline>\n"
        "Output ONLY those two lines. Zero extra text. Zero preamble."
    )
    try:
        response = ask_ai(prompt).strip()
        lines = [l.strip() for l in response.splitlines() if l.strip()]
        setup = punchline = None
        for line in lines:
            if line.lower().startswith("q:"):
                setup = line[2:].strip()
            elif line.lower().startswith("a:"):
                punchline = line[2:].strip()
        if setup and punchline:
            return setup, punchline
        if len(lines) >= 2:
            return lines[0], lines[1]
        # Last resort: hardcoded banger
        return random.choice(HARDCODED_JOKES)
    except Exception:
        return random.choice(HARDCODED_JOKES)


# ── AI-powered Roast ───────────────────────────────────────────
def get_ai_roast(target):
    """70% AI-generated, 30% hardcoded — always soul-destroying."""
    subject = "me" if target in ("you", "me") else target

    # 30% chance: fire a hardcoded nuke instantly
    if random.random() < 0.30:
        return random.choice(HARDCODED_ROASTS)

    style = random.choice(ROAST_STYLES)
    examples = random.sample(HARDCODED_ROASTS, 3)
    ex_block = "\n".join(f"— {e}" for e in examples)

    prompt = (
        f"You are the most feared roast master in history. You have made celebrities cry on stage, "
        f"ended careers with a single sentence, and turned whole rooms silent with one line. "
        f"Your roasts are legendary because they feel PERSONAL — like you've studied the target "
        f"for years and found the one sentence that exposes everything.\n\n"
        f"Target: {subject}\n"
        f"Style: {style}\n\n"
        f"Here are examples of the MINIMUM brutality I expect:\n"
        f"{ex_block}\n\n"
        f"Now write ONE roast for {subject} that is MORE devastating than any example above. "
        "Rules:\n"
        "— Must feel specific and personal, not generic.\n"
        "— Must be clever AND cruel — the kind that gets screenshotted and shared.\n"
        "— Must sting for days. They should question their life choices after reading it.\n"
        "— Should land like a sniper shot — quiet, precise, absolutely fatal.\n"
        "— No filler words, no warm-up. Pure payload from the first word.\n\n"
        "Output ONLY the roast. One to two sentences max. "
        "No intro, no label, no emoji, no explanation. Go for the jugular."
    )
    try:
        result = ask_ai(prompt).strip().strip('"').strip("'")
        return result if result else random.choice(HARDCODED_ROASTS)
    except Exception:
        return random.choice(HARDCODED_ROASTS)


# ── Banner ─────────────────────────────────────────────────────
def print_banner(ai_name, theme_colors):
    c = theme_colors
    print(f"""
{BOLD}{c['system']}
╔══════════════════════════════════════════╗
║             🤖 AI CLI Assistant          ║
║         Type 'help' to get started       ║
╚══════════════════════════════════════════╝
{RESET}{DIM}AI Assistant:{RESET} {BOLD}{c['ai']}{ai_name}{RESET}
""")


# ── Dynamic help (reads live state) ────────────────────────────
def build_help(theme_colors):
    Y  = theme_colors["user"]
    C  = theme_colors["system"]
    return f"""
{BOLD}{C}g4f CLI — Command Reference{RESET}

{BOLD}General{RESET}
  {Y}help{RESET}                   Show this command list
  {Y}help <command>{RESET}         Get details on a specific command
  {Y}exit / quit{RESET}            Exit the CLI
  {Y}clear{RESET}                  Clear the terminal screen
  {Y}version{RESET}                Show CLI version
  {Y}history{RESET}                Show full chat history
  {Y}clearhistory{RESET}           Wipe the chat history clean
  
{BOLD}Customization{RESET}
  {Y}rename <name>{RESET}          Rename the AI  (e.g. rename Jarvis)
  {Y}randomname{RESET}             Give the AI a random name

  {Y}theme <name>{RESET}           Switch color theme  (e.g. theme ocean)
  {Y}themes{RESET}                 List all available themes

  {Y}color <element> <color>{RESET}  Fine-tune a single color
                           Elements : user · ai · system
                           Colors   : {', '.join(COLOR_MAP)}
                           Example  : color ai blue

  {Y}prompt <style>{RESET}         Change the input prompt style
  {Y}prompts{RESET}                List all prompt styles

  {Y}mood <name>{RESET}            Set AI response mood  (e.g. mood funny)
  {Y}moods{RESET}                  List all available moods

  {Y}timestamp on/off{RESET}       Show/hide time on AI replies
  {Y}banner on/off / banner{RESET} Toggle or re-show the banner

  {Y}resetui{RESET}                Reset all CLI settings to defaults

{BOLD}Utilities{RESET}
  {Y}whoami{RESET}                 Show current CLI settings
  {Y}tips{RESET}                   Show usage tips
  {Y}examples{RESET}               Show example commands
  {Y}echo <text>{RESET}            Print text back to screen
  {Y}roast / roast <name>{RESET}   Get roasted or roast someone 🔥
  {Y}joke {RESET}                  Hear a random joke 😂
  {Y}save txt{RESET}               Save to chat_history.txt
  {Y}save json{RESET}              Save to chat_history.json
  {Y}metrics{RESET}                Show message count stats

{BOLD}Input Rules{RESET}
  • Max {BOLD}1000{RESET} characters per message
  • Min {BOLD}2{RESET} characters required
  • Repeated identical messages are blocked
  • Gibberish detection (repeating chars) warns you
"""


# ── Per-command detailed help ───────────────────────────────────
COMMAND_HELP = {
    "theme":     "Usage: theme <name>\nSwitches the color theme.\nExample: theme ocean\nUse 'themes' to list all options.",
    "color":     "Usage: color <element> <colorname>\nElements: user, ai, system\nColors: " + ", ".join(COLOR_MAP) + "\nExample: color ai blue",
    "prompt":    "Usage: prompt <style>\nChanges the input prompt look.\nStyles: classic, arrow, simple, minimal, bracket\nExample: prompt bracket",
    "rename":    "Usage: rename <name>\nRenames the AI assistant.\nExample: rename Jarvis",
    "mood":      "Usage: mood <name>\nPrefixes your message with a tone instruction.\nExample: mood concise\nUse 'moods' to see all options.",
    "timestamp": "Usage: timestamp on  OR  timestamp off\nShows or hides the time next to AI replies.",
    "whoami":    "Displays your current CLI settings (theme, mood, prompt style, etc.)",
    "resetui":   "Resets all CLI settings back to their defaults.",
    "echo":      "Usage: echo <text>\nPrints the given text back to the terminal.",
}


# ── Input Validation ───────────────────────────────────────────
def validate_input(text, last_input):
    text = text.strip()

    # Empty
    if not text:
        return False, f"{RED}✖  Input cannot be empty.{RESET}"

    # Too short
    if len(text) < 2:
        return False, f"{RED}✖  Input too short (min 2 characters).{RESET}"

    # Too long
    if len(text) > 1000:
        return False, f"{RED}✖  Input too long (max 1000 characters).{RESET}"

    # Spam: same message repeated
    if text.lower() == last_input.lower() and last_input:
        return False, f"{YELLOW}⚠  Same message as last time. Try something new.{RESET}"

    # Gibberish: single char repeated 6+ times (e.g. "aaaaaa", "......")
    if re.fullmatch(r"(.)\1{5,}", text):
        return False, f"{YELLOW}⚠  Looks like gibberish. Please enter a proper message.{RESET}"

    # All digits only
    if text.isdigit():
        return False, f"{YELLOW}⚠  Message is just numbers. Please enter a question or statement.{RESET}"

    return True, ""


# ── Prompt builder ─────────────────────────────────────────────
def build_prompt(prompt_style, theme_colors):
    if prompt_style == "arrow":
        return f"{theme_colors['user']}➜  {RESET}"
    elif prompt_style == "simple":
        return "> "
    elif prompt_style == "minimal":
        return "  "
    elif prompt_style == "bracket":
        return f"{theme_colors['user']}[you]{RESET} "
    else:  # classic
        return f"{BOLD}{theme_colors['user']}You:{RESET} "


class ChatHistory:
    def __init__(self):
        self.history = []
        self.total_messages = 0

    def add(self, role, content):
        msg = {
            "role": role,
            "content": content,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.append(msg)
        self.total_messages += 1

    def show(self):
        if not self.history:
            print("No chat history.\n")
            return
        
        print("\n--- Chat History ---")
        for m in self.history:
            print(f"[{m['time']}] {m['role'].upper()}: {m['content']}")
        print()

    def save_txt(self, file="chat_history.txt"):
        with open(file, "w", encoding="utf-8") as f:
            for m in self.history:
                f.write(f"[{m['time']}] {m['role']}: {m['content']}\n")
        print(f"Saved to {file}\n")

    def save_json(self, file="chat_history.json"):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4)
        print(f"Saved to {file}\n")

    def metrics(self):
        user = len([m for m in self.history if m["role"] == "user"])
        ai   = len([m for m in self.history if m["role"] == "ai"])
        print("\n--- Metrics ---")
        print(f"Total messages: {self.total_messages}")
        print(f"User messages : {user}")
        print(f"AI messages   : {ai}\n")

    def clear(self):
        self.history = []
        self.total_messages = 0
        print("History cleared.\n")


# ── Main CLI ───────────────────────────────────────────────────
def main():
    chat = ChatHistory()

    # ── Session state ─────────────────────────────────────────
    ai_name        = "AI"
    theme          = "default"
    prompt_style   = "classic"
    banner_enabled = True
    mood           = "default"
    timestamp_on   = False
    last_input     = ""

    theme_colors = THEMES[theme].copy()   # mutable copy (supports `color` cmd)

    if banner_enabled:
        print_banner(ai_name, theme_colors)

    while True:

        prompt_text = build_prompt(prompt_style, theme_colors)

        try:
            sys.stdout.write(prompt_text)
            sys.stdout.flush()
            raw = input("").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        cmd = raw.lower()

        # ── Exit ──────────────────────────────────────────────
        if cmd in ("exit", "quit"):
            sys_msg(theme_colors["system"], "Goodbye! 👋")
            break

        # ── Help ──────────────────────────────────────────────
        elif cmd == "help":
            print(build_help(theme_colors))
            continue

        elif cmd.startswith("help "):
            topic = raw[5:].strip().lower()
            if topic in COMMAND_HELP:
                divider(theme_colors["system"])
                print(f"\n{BOLD}{theme_colors['system']}{topic}{RESET}\n")
                print(COMMAND_HELP[topic])
                divider(theme_colors["system"])
                print()
            else:
                sys_msg(RED, f"✖  No detailed help for '{topic}'. Try 'help' for full list.")
            continue

        # ── Version ───────────────────────────────────────────
        elif cmd == "version":
            sys_msg(theme_colors["system"], f"g4f CLI  v{VERSION}")
            continue

        # ── Clear ─────────────────────────────────────────────
        elif cmd == "clear":
            os.system("cls" if os.name == "nt" else "clear")
            continue

        # ── Rename AI ─────────────────────────────────────────
        elif cmd == "rename":
            sys_msg(YELLOW, "Usage: rename <name>   e.g. rename Jarvis")
            continue

        elif cmd.startswith("rename "):
            ai_name = raw[7:].strip() or "AI"
            sys_msg(theme_colors["system"], f"✔  AI renamed to '{ai_name}'")
            continue

        # ── Random name ───────────────────────────────────────
        elif cmd == "randomname":
            ai_name = random.choice(AI_NAMES)
            sys_msg(theme_colors["system"], f"✔  AI renamed to '{ai_name}'")
            continue

        # ── Themes list ───────────────────────────────────────
        elif cmd == "themes":
            sys_msg(BOLD, "Available themes:")
            for t, cols in THEMES.items():
                marker = " ◀ active" if t == theme else ""
                print(f"  {cols['ai']}●{RESET}  {t}{DIM}{marker}{RESET}")
            print()
            continue

        # ── Theme change ──────────────────────────────────────
        elif cmd.startswith("theme "):
            new_theme = raw.split()[1].lower()
            if new_theme not in THEMES:
                sys_msg(RED, f"✖  Unknown theme '{new_theme}'.")
                sys_msg(DIM, "   Use 'themes' to see options.")
            else:
                theme = new_theme
                theme_colors = THEMES[theme].copy()
                sys_msg(theme_colors["system"], f"✔  Theme switched to '{theme}'")
            continue

        # ── Fine-grained color customization ──────────────────
        elif cmd == "colors":
            sys_msg(BOLD, "Available colors:")
            for name, code in COLOR_MAP.items():
                print(f"  {code}■  {name}{RESET}")
            print()
            continue

        elif cmd.startswith("color "):
            parts = raw.split()
            if len(parts) != 3:
                sys_msg(YELLOW, "Usage: color <element> <color>")
                sys_msg(DIM,    "       Elements: user · ai · system")
                sys_msg(DIM,    "       Example : color ai blue")
            else:
                element, color_name = parts[1].lower(), parts[2].lower()
                if element not in ("user", "ai", "system"):
                    sys_msg(RED, f"✖  Unknown element '{element}'. Use: user, ai, system")
                elif color_name not in COLOR_MAP:
                    sys_msg(RED, f"✖  Unknown color '{color_name}'.")
                    sys_msg(DIM, f"   Available: {', '.join(COLOR_MAP)}")
                else:
                    theme_colors[element] = COLOR_MAP[color_name]
                    sys_msg(theme_colors["system"], f"✔  '{element}' color set to {COLOR_MAP[color_name]}{color_name}{RESET}")
            continue

        # ── Prompt styles ─────────────────────────────────────
        elif cmd == "prompts":
            sys_msg(BOLD, "Available prompt styles:")
            for p in PROMPT_STYLES:
                marker = " ◀ active" if p == prompt_style else ""
                print(f"  {theme_colors['user']}•{RESET}  {p}{DIM}{marker}{RESET}")
            print()
            continue

        elif cmd.startswith("prompt "):
            style = raw.split()[1].lower()
            if style not in PROMPT_STYLES:
                sys_msg(RED, f"✖  Unknown style '{style}'.")
                sys_msg(DIM, f"   Available: {', '.join(PROMPT_STYLES)}")
            else:
                prompt_style = style
                sys_msg(theme_colors["system"], f"✔  Prompt style set to '{style}'")
            continue

        # ── Mood ──────────────────────────────────────────────
        elif cmd == "moods":
            sys_msg(BOLD, "Available moods:")
            for m, desc in MOODS.items():
                marker = " ◀ active" if m == mood else ""
                preview = desc[:40] + "…" if len(desc) > 40 else (desc or "(no prefix)")
                print(f"  {theme_colors['ai']}•{RESET}  {m:<10} {DIM}{preview}{RESET}{DIM}{marker}{RESET}")
            print()
            continue

        elif cmd == "mood":
            sys_msg(YELLOW, f"Current mood: {mood}")
            sys_msg(DIM,     "Usage: mood <name>   e.g. mood funny")
            continue

        elif cmd.startswith("mood "):
            new_mood = raw.split()[1].lower()
            if new_mood not in MOODS:
                sys_msg(RED, f"✖  Unknown mood '{new_mood}'.")
                sys_msg(DIM, f"   Use 'moods' to see options.")
            else:
                mood = new_mood
                sys_msg(theme_colors["system"], f"✔  Mood set to '{mood}'")
            continue

        # ── Timestamp ─────────────────────────────────────────
        elif cmd == "timestamp on":
            timestamp_on = True
            sys_msg(theme_colors["system"], "✔  Timestamps enabled")
            continue

        elif cmd == "timestamp off":
            timestamp_on = False
            sys_msg(theme_colors["system"], "✔  Timestamps disabled")
            continue

        elif cmd == "timestamp":
            state = "on" if timestamp_on else "off"
            sys_msg(DIM, f"Timestamps are currently {state}. Use 'timestamp on/off' to toggle.")
            continue

        # ── Banner commands ───────────────────────────────────
        elif cmd == "banner":
            print_banner(ai_name, theme_colors)
            continue

        elif cmd == "banner off":
            banner_enabled = False
            sys_msg(DIM, "Banner disabled")
            continue

        elif cmd == "banner on":
            banner_enabled = True
            print_banner(ai_name, theme_colors)
            continue

        # ── Reset UI ──────────────────────────────────────────
        elif cmd == "resetui":
            ai_name        = "AI"
            theme          = "default"
            theme_colors   = THEMES[theme].copy()
            prompt_style   = "classic"
            banner_enabled = True
            mood           = "default"
            timestamp_on   = False
            last_input     = ""
            sys_msg(theme_colors["system"], "✔  CLI settings reset to defaults")
            continue

        # ── Whoami ────────────────────────────────────────────
        elif cmd == "whoami":
            divider(theme_colors["system"])
            print(f"""
  {DIM}AI Name   {RESET}{BOLD}{theme_colors['ai']}{ai_name}{RESET}
  {DIM}Theme     {RESET}{theme}
  {DIM}Prompt    {RESET}{prompt_style}
  {DIM}Mood      {RESET}{mood}
  {DIM}Timestamp {RESET}{'on' if timestamp_on else 'off'}
  {DIM}Banner    {RESET}{'enabled' if banner_enabled else 'disabled'}
  {DIM}Version   {RESET}v{VERSION}
""")
            divider(theme_colors["system"])
            print()
            continue

        # ── Tips ──────────────────────────────────────────────
        elif cmd == "tips":
            tips = [
                "Use 'themes' to browse all color themes",
                "Use 'color ai green' to fine-tune a single color",
                "Try 'mood concise' for shorter AI answers",
                "Use 'prompt bracket' for a different input look",
                "Type 'help <command>' for details on any command",
                "Use 'timestamp on' to see when each reply arrives",
                "Reset everything with 'resetui'",
            ]
            sys_msg(BOLD, "CLI Tips:")
            for tip in tips:
                print(f"  {theme_colors['system']}•{RESET}  {tip}")
            print()
            continue

        # ── Examples ──────────────────────────────────────────
        elif cmd == "examples":
            examples = [
                ("rename Jarvis",       "Rename AI to Jarvis"),
                ("theme ocean",         "Switch to ocean theme"),
                ("color user orange",   "Make your text orange"),
                ("prompt bracket",      "Use [you] prompt style"),
                ("mood funny",          "Get humorous responses"),
                ("timestamp on",        "Show time on replies"),
                ("help mood",           "Detailed help on mood"),
                ("roast me",            "Get roasted 🔥"),
                ("roast Jarvis",        "Roast someone by name"),
                ("joke",                "Hear a random joke 😂"),
            ]
            sys_msg(BOLD, "Example commands:")
            for ex, desc in examples:
                print(f"  {theme_colors['user']}{ex:<26}{RESET} {DIM}{desc}{RESET}")
            print()
            continue

        # ── Echo ──────────────────────────────────────────────
        elif cmd.startswith("echo "):
            print(raw[5:])
            continue

        # ── Roast (AI-powered) ────────────────────────────────
        elif cmd in ("roast", "roast me") or cmd.startswith("roast "):
            if cmd.startswith("roast ") and cmd not in ("roast me",):
                target = raw[6:].strip()
            else:
                target = "you"
            sys_msg(DIM, "Cooking up a roast...\n")
            roast = get_ai_roast(target)
            divider(RED)
            print(f"{BOLD}{RED}🔥 [{target}]{RESET} {roast}\n")
            continue

        # ── Joke (AI-powered) ─────────────────────────────────
        elif cmd in ("joke", "jokes"):
            sys_msg(DIM, "Fetching a joke...\n")
            setup, punchline = get_ai_joke()
            divider(theme_colors["system"])
            print(f"{BOLD}{theme_colors['system']}😂 {setup}{RESET}")
            print(f"   {punchline}\n")
            continue

        # ── History Commands ──────────────────────────────────
        elif cmd == "history":
            chat.show()
            continue

        elif cmd == "save txt":
            chat.save_txt()
            continue

        elif cmd == "save json":
            chat.save_json()
            continue

        elif cmd == "metrics":
            chat.metrics()
            continue

        elif cmd == "clearhistory":
            chat.clear()
            continue

        # ── Unknown single-word commands ──────────────────────
        elif cmd in ("color", "prompt", "theme", "mood", "timestamp"):
            pass

        # ── AI Handling ─────────────────────────────────────
        valid, err = validate_input(raw, last_input)
        if not valid:
            print(err)
            continue

        last_input = raw
        chat.add("user", raw)
        
        query = MOODS[mood] + raw

        sys_msg(DIM, "AI is thinking...\n")

        try:
            response = ask_ai(query)
        except Exception as e:
            response = f"{RED}Error: {e}{RESET}"

        time_str = ""
        if timestamp_on:
            time_str = f"{DIM}[{datetime.now().strftime('%H:%M:%S')}] {RESET}"

        print(f"{time_str}{BOLD}{theme_colors['ai']}{ai_name}:{RESET} {response}\n")
        chat.add("ai", response)




if __name__ == "__main__":
    main()