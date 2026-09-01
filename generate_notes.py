#!/usr/bin/env python3
"""
Daily Agentic AI Notes Generator using Groq.
Generates 0-5 random notes per day, each saved as [topic].md.
"""

import os
import random
import datetime
import sys
import subprocess
import re
from groq import Groq  # pip install groq

# -------------------- Configuration --------------------
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    sys.exit("Error: GROQ_API_KEY environment variable not set.")

# Active Groq model (llama-3.3-70b-versatile / -specdec are deprecated as of
# June 17 2026, shutdown Aug 16 2026). Groq's official replacement:
# https://console.groq.com/docs/deprecations
MODEL = "openai/gpt-oss-120b"

# Prompt that forces a Topic line and a Note line
PROMPT_TEMPLATE = (
    "Write a short, insightful note (maximum 30 words) about a specific, "
    "distinct facet of Agentic AI (like planning, memory, tool-use, multi-agent "
    "coordination, safety, reasoning, self-reflection, etc.). "
    "IMPORTANT: "
    "1. Ensure this topic is completely different from any other note generated today. "
    "2. Respond with exactly two lines in this format: "
    "   TOPIC: [specific topic title in 2-5 words, e.g., 'LoRA Fine-Tuning for Tool-Use'] "
    "   NOTE: [your 30-word insight about that topic] "
    "(This is note #{index})"
)

NOTES_DIR = "notes"
# ------------------------------------------------------


def sanitize_filename(text):
    """Convert a topic string into a safe filename (lowercase, hyphens)."""
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    slug = re.sub(r'\s+', '-', cleaned)
    return slug.strip('-').lower()


def generate_topic_and_note(client, index):
    """Generate a note using Groq and parse the topic and content."""
    try:
        prompt = PROMPT_TEMPLATE.format(index=index)
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.95,
            reasoning_effort="low",
        )
        raw_text = response.choices[0].message.content.strip()

        lines = raw_text.split('\n')
        topic = None
        note_content = None
        for line in lines:
            line = line.strip()
            if line.lower().startswith("topic:"):
                topic = line[6:].strip()
            elif line.lower().startswith("note:"):
                note_content = line[5:].strip()

        # Fallback if the model didn't follow the exact format
        if not topic or not note_content:
            print(f"⚠️  Model didn't follow format. Raw: {raw_text}")
            words = raw_text.split()
            topic = " ".join(words[:3]) if len(words) >= 3 else "agentic-ai"
            note_content = raw_text

        return topic, note_content
    except Exception as e:
        print(f"Error generating note {index}: {e}")
        return None, None


def create_note_file(topic, note_content, date_str, index):
    """Write a single note to a Markdown file named after the topic."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    slug = sanitize_filename(topic)
    if not slug:
        slug = f"note_{date_str}_{index:03d}"
    filepath = os.path.join(NOTES_DIR, f"{slug}.md")
    # If file already exists (e.g., same topic), append date
    if os.path.exists(filepath):
        filepath = os.path.join(NOTES_DIR, f"{slug}_{date_str}.md")
    with open(filepath, "w") as f:
        f.write(f"# 🤖 {topic}\n\n")
        f.write(f"{note_content}\n\n")
        f.write(f"---\n*Generated on {date_str}*")
    return filepath


def git_commit_and_push(filepath, topic):
    """Add, commit, and push a single file."""
    try:
        subprocess.run(["git", "add", filepath], check=True)
        commit_msg = f"AI Note: {topic[:60]}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)
        print(f"✅ Committed and pushed: {os.path.basename(filepath)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Git operation failed: {e}")
        return False


def main():
    num_commits = random.randint(0, 5)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    print(f"🔢 Today's random commit count: {num_commits}")

    if num_commits == 0:
        print("⏭️  No commits today. Exiting.")
        return

    # Initialize Groq client
    client = Groq(api_key=API_KEY)

    for i in range(1, num_commits + 1):
        print(f"\n📝 Generating note #{i} ...")
        topic, note = generate_topic_and_note(client, i)
        if not topic or not note:
            print(f"⚠️  Skipping note #{i} due to generation error.")
            continue
        print(f"   Topic: {topic}")
        filepath = create_note_file(topic, note, date_str, i)
        print(f"💾 Created file: {filepath}")
        if not git_commit_and_push(filepath, topic):
            print(f"❌ Failed to commit/push note #{i}, stopping early.")
            break

    print("\n🎉 All commits for today are done!")


if __name__ == "__main__":
    main()
