#!/usr/bin/env python3
"""
Daily Agentic AI Notes Generator using Groq.
Generates 0–5 random notes about unique Agentic AI topics each day.
Saves output as a Markdown (.md) file.
"""

import os
import random
import datetime
import sys
from groq import Groq  # pip install groq

# -------------------- Configuration --------------------
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    sys.exit("Error: GROQ_API_KEY environment variable not set.")

# Groq's versatile model
MODEL = "llama-3.3-70b-versatile"

# Agentic AI focused prompt with distinct topic requirement
PROMPT = (
    "Write a short, insightful note (maximum 30 words) about a specific, "
    "distinct facet of Agentic AI. This could include aspects like planning, "
    "memory, tool-use, multi-agent coordination, safety, reasoning, self-reflection, "
    "or emergent behavior. IMPORTANT: Ensure this topic is completely different "
    "from any other note generated today."
)

NOTES_DIR = "notes"
# ------------------------------------------------------

def generate_note(client, prompt, note_index):
    """Call Groq and return a single note. Passes index to vary context slightly."""
    try:
        # Adding the index to the prompt slightly nudges the LLM to vary topics
        full_prompt = f"{prompt} (This is note #{note_index})"
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": full_prompt}],
            max_tokens=60,
            temperature=0.95,  # Higher temp for maximum topic variety
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating note: {e}")
        return None

def save_notes(notes, date_str):
    """Save all notes as a formatted Markdown file in the notes directory."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    filename = os.path.join(NOTES_DIR, f"notes_{date_str}.md")
    
    with open(filename, "w") as f:
        # Header
        f.write(f"# 🤖 Agentic AI Daily Notes - {date_str}\n\n")
        
        if not notes:
            f.write("> No notes generated for today. The agents are resting. 💤\n")
        else:
            f.write(f"> *{len(notes)} random insights generated today.*\n\n---\n\n")
            for idx, note in enumerate(notes, 1):
                f.write(f"## 🧠 Insight {idx}\n\n")
                f.write(f"{note}\n\n")
                # Add a horizontal rule between notes except for the last one
                if idx < len(notes):
                    f.write("---\n\n")
    
    print(f"Saved {len(notes)} notes to {filename}")

def main():
    # Randomly decide how many notes to generate (0 to 5)
    num_notes = random.randint(0, 5)
    print(f"Generating {num_notes} Agentic AI note(s) for today.")

    # Initialize the Groq client
    client = Groq(api_key=API_KEY)

    # Generate the notes
    notes = []
    for i in range(num_notes):
        note = generate_note(client, PROMPT, i + 1)
        if note:
            notes.append(note)
        else:
            print(f"Failed to generate note {i+1}, skipping.")

    # Save notes with today's date
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    save_notes(notes, date_str)

if __name__ == "__main__":
    main()