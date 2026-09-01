#!/usr/bin/env python3
"""
Daily Agentic AI Notes Generator with Random Commits (0–5 per day).
Each commit contains exactly one note about a unique Agentic AI topic.
"""

import os
import random
import datetime
import sys
import subprocess
from groq import Groq

# -------------------- Configuration --------------------
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    sys.exit("Error: GROQ_API_KEY environment variable not set.")

MODEL = "llama-3.3-70b-versatile"

# Agentic AI prompt – forces a distinct topic for each note
PROMPT_TEMPLATE = (
    "Write a short, insightful note (maximum 30 words) about a specific, "
    "distinct facet of Agentic AI. This could include planning, memory, "
    "tool-use, multi-agent coordination, safety, reasoning, self-reflection, "
    "or emergent behavior. IMPORTANT: Ensure this topic is completely different "
    "from any other note generated today. (This is note #{index})"
)

NOTES_DIR = "notes"
# ------------------------------------------------------

def generate_note(client, index):
    """Generate one note using Groq."""
    try:
        prompt = PROMPT_TEMPLATE.format(index=index)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
            temperature=0.95,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating note {index}: {e}")
        return None

def create_note_file(note, date_str, index):
    """Write a single note to a unique Markdown file."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(NOTES_DIR, f"agentic_note_{date_str}_{index:03d}.md")
    
    with open(filename, "w") as f:
        f.write(f"# 🤖 Agentic AI Note – {date_str} (#{index})\n\n")
        f.write(f"{note}\n")
    
    return filename

def git_commit_and_push(filepath, date_str, index):
    """Add, commit, and push a single file."""
    try:
        subprocess.run(["git", "add", filepath], check=True)
        commit_msg = f"Agentic AI note #{index} for {date_str}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)
        print(f"✅ Committed and pushed: {filepath}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False

def main():
    # 1. Roll the dice – how many commits today? (0 to 5)
    num_commits = random.randint(0, 5)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"🔢 Today's random commit count: {num_commits}")

    if num_commits == 0:
        print("⏭️  No commits today. Exiting.")
        return

    # 2. Initialize Groq client
    client = Groq(api_key=API_KEY)

    # 3. Generate and commit each note separately
    for i in range(1, num_commits + 1):
        print(f"\n📝 Generating note #{i} ...")
        note = generate_note(client, i)
        if not note:
            print(f"⚠️  Skipping note #{i} due to generation error.")
            continue

        # Write to a unique file
        filepath = create_note_file(note, date_str, i)
        print(f"💾 Created file: {filepath}")

        # Commit and push immediately
        if not git_commit_and_push(filepath, date_str, i):
            print(f"❌ Failed to commit/push note #{i}, stopping early.")
            break

    print("\n🎉 All commits for today are done!")

if __name__ == "__main__":
    main()