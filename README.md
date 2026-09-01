# 🤖 Agentic AI Daily Notes Generator

This repository automatically generates 0–5 random notes about Agentic AI every day, using **Groq's LLM API**. Each note is saved as a `.md` file with a filename based on its topic (e.g., `multi-agent-planning.md`). The number of commits per day is random (0–5), creating a natural, varied commit history.

## ✨ Features

- **Random daily commits** – 0 to 5 commits per day.
- **Topic-based filenames** – e.g., `tool-calling-strategies.md`.
- **Automated scheduling** – runs at midnight UTC via GitHub Actions.
- **Fresh topics** – each note covers a distinct facet of Agentic AI.

## 🔧 Setup

1. **Fork/clone** this repository.
2. **Get a Groq API key** from [console.groq.com/keys](https://console.groq.com/keys).
3. **Add the key** as a GitHub secret:
   - Go to your repo → **Settings** → **Secrets and variables** → **Actions**.
   - Create a new secret named `GROQ_API_KEY` and paste your key.
4. **Model** – `generate_notes.py` uses `openai/gpt-oss-120b`, Groq's current
   recommended replacement for the deprecated `llama-3.3-70b-versatile`/
   `-specdec` models. If Groq deprecates it later, check
   [console.groq.com/docs/models](https://console.groq.com/docs/models) and
   update the `MODEL` variable.
5. **Commit and push** – the workflow will run automatically at midnight UTC, or you can trigger it manually from the **Actions** tab.

## 📂 Output

All notes are stored in the `notes/` folder. Each file is a Markdown document containing one insight.

## 🛠️ Customisation

- Adjust the prompt in `generate_notes.py` to change the style or domain.
- Change the random range (`random.randint(0, 5)`) to any other range.
- Switch to another LLM provider by modifying the client initialisation.

## ❓ Troubleshooting

- **Model not found (404 / `model_not_found`)** – the model in `MODEL` was
  deprecated. Check [console.groq.com/docs/deprecations](https://console.groq.com/docs/deprecations)
  and update `MODEL` in `generate_notes.py`.
- **API key errors** – verify that the secret is correctly named `GROQ_API_KEY`.
- **No commits** – if the random count is 0, the script exits without committing. This is expected.
- **Commits don't show on your GitHub contribution graph** – the workflow
  now sets `git config user.email` to `${{ github.actor }}@users.noreply.github.com`,
  which GitHub recognizes as belonging to you. If you renamed the workflow
  step or changed this, make sure the email matches an address linked to
  your GitHub account (Settings → Emails).
