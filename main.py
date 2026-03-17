import os
import sys
import random
import re
from datetime import datetime

# ── Version ────────────────────────────────────────────────────
VERSION = "1.2.0"

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

# ── Roast Lines ────────────────────────────────────────────────
ROASTS = [
    "You're the human equivalent of a 404 error.",
    "I've seen better code in a kindergarten scratch project.",
    "You bring everyone so much joy... when you leave the room.",
    "Your Wi-Fi password is probably 'password123', isn't it.",
    "You're not stupid, you just have bad luck thinking.",
    "I'd roast you harder but my terms of service have limits.",
    "You're like a software update — nobody asked for you.",
    "Even your Google searches must be embarrassing.",
    "You're the reason the AI needs a safety filter.",
    "I've seen better arguments in a YouTube comment section.",
    "You could get lost in a straight hallway.",
    "Your code probably has more bugs than a rainforest.",
    "If brains were code, yours would be written in Notepad.",
    "You're the type to reply 'you too' when the waiter says enjoy your meal.",
    "I'm not saying you're slow, but turtles overtake you in a debate.",
]

# ── Jokes ───────────────────────────────────────────────────────
JOKES = [
    ("Why do programmers prefer dark mode?", "Because light attracts bugs."),
    ("Why did the developer go broke?", "Because he used up all his cache."),
    ("How do you comfort a JavaScript bug?", "You console it."),
    ("Why did the Python programmer wear glasses?", "Because he couldn't C#."),
    ("What's a computer's favorite snack?", "Microchips."),
    ("Why was the database administrator unhappy?", "Because he had too many tables to handle."),
    ("What do you call a programmer from Finland?", "Nerdic."),
    ("Why did the boolean break up with the integer?", "Because it just wasn't True anymore."),
    ("What did the router say to the doctor?", "It hurts when IP."),
    ("Why do Java developers wear glasses?", "Because they don't C++."),
    ("What's an astronaut's favorite key?", "The space bar."),
    ("Why did the computer get cold?", "It left its Windows open."),
    ("How many programmers does it take to change a light bulb?", "None — that's a hardware problem."),
    ("What do you call 8 hobbits?", "A hobbyte."),
    ("Why did the function break up with the loop?", "Too many iterations."),
]

# ── Mood map (prefixed to user query before ask_ai) ────────────
MOODS = {
    "default":  "",
    "concise":  "Reply in as few words as possible. ",
    "formal":   "Reply in a formal, professional tone. ",
    "friendly": "Reply in a warm, friendly, casual tone. ",
    "funny":    "Reply with humor and wit. ",
    "teacher":  "Explain like I am a beginner. Use simple language and examples. ",
    "expert":   "Assume I am an expert. Be technical and precise. ",
}


# ── Helpers ────────────────────────────────────────────────────

def sys_msg(color, text):
    """Print a colored system message."""
    print(f"{color}{text}{RESET}")

def divider(color=DIM):
    print(f"{color}{'─' * 44}{RESET}")


# ── Banner ─────────────────────────────────────────────────────
def print_banner(ai_name, theme_colors):
    c = theme_colors
    print(f"""
{BOLD}{c['system']}
╔══════════════════════════════════════════╗
║             g4f CLI  v{VERSION}              ║
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


# ── Main CLI ───────────────────────────────────────────────────
def main():

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

        # ── Roast ─────────────────────────────────────────────
        elif cmd in ("roast", "roast me") or cmd.startswith("roast "):
            if cmd.startswith("roast ") and cmd not in ("roast me",):
                target = raw[6:].strip()
            else:
                target = "you"
            roast = random.choice(ROASTS)
            divider(RED)
            print(f"{BOLD}{RED}🔥 [{target}]{RESET} {roast}\n")
            continue

        # ── Joke ──────────────────────────────────────────────
        elif cmd in ("joke", "jokes"):
            setup, punchline = random.choice(JOKES)
            divider(theme_colors["system"])
            print(f"{BOLD}{theme_colors['system']}😂 {setup}{RESET}")
            print(f"   {punchline}\n")
            continue


        # ── Unknown single-word commands ──────────────────────
        elif cmd in ("color", "prompt", "theme", "mood", "timestamp"):
            pass

        # ─────────────────────────────────────────────────────
        # Anything else → validate input and (in a full implementation) send to AI
        # ─────────────────────────────────────────────────────
        valid, err = validate_input(raw, last_input)
        if not valid:
            print(err)
            continue

        last_input = raw


if __name__ == "__main__":
    main()