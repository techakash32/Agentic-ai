#!/usr/bin/env python3
"""
Daily Random Notes Generator using Groq's LLM API (llama-3.3-70b-versatile).
Generates 0–5 random notes each day and saves them to a dated file.
"""

import os
import random
import datetime
import json
import sys
from groq import Groq  # pip install groq

# -------------------- Configuration --------------------
# Use environment variable for API key (set in GitHub Secrets)
API_KEY = os.environ.get("GROQ_API_KEY")
if not API_KEY:
    sys.exit("Error: GROQ_API_KEY environment variable not set.")

# Groq's fastest and most versatile model
MODEL = "llama-3.3-70b-versatile"  # or "mixtral-8x7b-32768", "gemma2-9b-it"

# Prompt for generating a single note
PROMPT = "Write a short, random thought, observation, or piece of advice. Keep it under 30 words."

# Folder where notes will be stored (will be created if missing)
NOTES_DIR = "notes"

# ------------------------------------------------------

def generate_note(client, prompt):
    """Call the Groq LLM and return the generated note text."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=60,       # Groq handles this well
            temperature=0.9,     # Slightly creative
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating note: {e}")
        return None

def save_notes(notes, date_str):
    """Save the list of notes to a dated file in the notes directory."""
    os.makedirs(NOTES_DIR, exist_ok=True)
    filename = os.path.join(NOTES_DIR, f"notes_{date_str}.json")
    with open(filename, "w") as f:
        json.dump(notes, f, indent=2)
    print(f"Saved {len(notes)} notes to {filename}")

def main():
    # Randomly decide how many notes to generate (0 to 5)
    num_notes = random.randint(0, 5)
    print(f"Generating {num_notes} note(s) for today.")

    if num_notes == 0:
        print("No notes generated today.")
        # Still save an empty file to mark the day
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        save_notes([], date_str)
        return

    # Initialize the Groq client
    client = Groq(api_key=API_KEY)

    # Generate the notes
    notes = []
    for i in range(num_notes):
        note = generate_note(client, PROMPT)
        if note:
            notes.append(note)
        else:
            print(f"Failed to generate note {i+1}, skipping.")

    # Save notes with today's date
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    save_notes(notes, date_str)

if __name__ == "__main__":
    main()