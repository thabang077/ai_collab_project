from ai_module import ask_ai
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
║             AI CLI Assistant              ║
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
    print("AI CLI Assistant")
    print("Type 'exit' to quit.\n")
 
    while True:
        user_input = input("You: ").strip()
 
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
 
        if not user_input:
            continue
 
        print("AI is thinking...\n")
 
        response = ask_ai(user_input)
 
        print("🤖 AI:", response)
        print()
 
if __name__ == "__main__":
    main()

    