# 🛠️ BadgeSmith

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

> Automate your way to GitHub achievement badges — transparently and responsibly.

**BadgeSmith** is a collection of Python automation tools for earning GitHub profile badges. Each tool is self-contained, clearly documented, and built to be run on your own repos with your own accounts.

---

## Badges covered

| Badge | Tool | What it does |
|---|---|---|
| 🦈 Pull Shark | `pull_shark.py` | Creates branches, commits, opens PRs, and merges them automatically |
| 🤝 Pair Extraordinaire | `pair_extraordinaire.py` | Creates PRs with `Co-authored-by` commit trailers using two accounts |
| 🧠 Galaxy Brain | `galaxy_brain.py` | Posts Q&A discussion pairs and marks answers as accepted using two accounts |

---

## Badge tiers

### 🦈 Pull Shark
| Tier | PRs merged |
|---|---|
| Default | 2 |
| 🥉 Bronze | 16 |
| 🥈 Silver | 128 |
| 🥇 Gold | 1024 |

### 🤝 Pair Extraordinaire
| Tier | Co-authored PRs merged |
|---|---|
| Default | 1 |
| 🥉 Bronze | 10 |
| 🥈 Silver | 24 |
| 🥇 Gold | 48 |

### 🧠 Galaxy Brain
| Tier | Accepted answers |
|---|---|
| Default | 8 |
| 🥉 Bronze | 16 |
| 🥈 Silver | 32 |

---

## Requirements

- Python 3.8+
- [GitHub CLI (`gh`)](https://cli.github.com/) — required for Pull Shark and Pair Extraordinaire
- `requests` library — required for Galaxy Brain (`pip install requests`)
- A GitHub personal access token with `repo` scope
- For Galaxy Brain and Pair Extraordinaire: a second GitHub account

---

## Setup

### 1. Clone this repo
```bash
git clone https://github.com/03x1/BadgeSmith.git
cd BadgeSmith
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Authenticate the GitHub CLI
```bash
gh auth login
```
Follow the prompts. Select HTTPS and paste your token when asked.

### 4. Create a target repo
Create a public or private repo on GitHub to run the bots against. It needs a `README.md` file. For Galaxy Brain, enable Discussions and add a **Q&A** category under your repo's Settings → Features → Discussions.

### 5. Clone your target repo locally
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

---

## Tools

### 🦈 Pull Shark — `pull_shark.py`

Creates branches, appends a small comment to `README.md`, pushes, opens a PR via the `gh` CLI, merges it, and cleans up — then repeats.

**Requirements:** GitHub token (`repo` scope), `gh` CLI installed and authenticated, a local clone of your target repo.

**Setup:**

Open `pull_shark.py` and fill in the configuration block at the top:

```python
GITHUB_USERNAME = "your-username"
GITHUB_TOKEN    = "ghp_..."
REPO_NAME       = "your-repo-name"
REPO_PATH       = r"C:\path\to\your\repo"   # use raw string on Windows
PR_COUNT        = 100
DELAY_SECONDS   = 15
```

**Run:**
```bash
python pull_shark.py
```

---

### 🤝 Pair Extraordinaire — `pair_extraordinaire.py`

Creates PRs with a `Co-authored-by` trailer in the commit message, verified before each push. Uses your main account to open and merge PRs, with the second account listed as co-author.

**Requirements:** Two GitHub accounts, tokens for both (`repo` scope), `gh` CLI authenticated as your main account.

> **Windows note:** Commit messages are written to a temp file and committed with `git commit -F` to avoid multiline issues on Windows. This is handled automatically.

**Setup:**

Open `pair_extraordinaire.py` and fill in:

```python
MAIN_USERNAME   = "your-main-username"
MAIN_TOKEN      = "ghp_..."
SECOND_USERNAME = "your-second-username"
SECOND_EMAIL    = "second@example.com"
SECOND_TOKEN    = "ghp_..."
REPO_NAME       = "your-repo-name"
REPO_PATH       = r"C:\path\to\your\repo"
PR_COUNT        = 50
DELAY_SECONDS   = 12
```

**Run:**
```bash
python pair_extraordinaire.py
```

---

### 🧠 Galaxy Brain — `galaxy_brain.py`

Uses the GitHub GraphQL API to automate Q&A discussions. The second account posts questions, the main account answers them, and the second account marks the answers as accepted.

**Requirements:** Two GitHub accounts, tokens for both (`repo` + `write:discussion` scope), Discussions enabled on your repo with a **Q&A category**.

> **Rate limiting note:** If you see errors after ~19 rounds, increase `DELAY_SECONDS` to 25 or higher.

**Setup:**

1. Enable Discussions on your repo: **Settings → Features → Discussions ✓**
2. Add a Q&A category: **Discussions → New Category → Question & Answer format**
3. Fill in `galaxy_brain.py`:

```python
MAIN_USERNAME   = "your-main-username"
MAIN_TOKEN      = "ghp_..."
SECOND_USERNAME = "your-second-username"
SECOND_TOKEN    = "ghp_..."
REPO_NAME       = "your-repo-name"
DELAY_SECONDS   = 20
TOTAL_ROUNDS    = 32
```

**Run:**
```bash
python galaxy_brain.py
```

The script includes 35 built-in Q&A pairs and shuffles them on each run. You can add your own pairs to the `QA_PAIRS` list in the script.

---

## Repo structure

```
BadgeSmith/
├── README.md
├── LICENSE
├── requirements.txt
├── pull_shark.py
├── pair_extraordinaire.py
└── galaxy_brain.py
```

---

## Generating a token

1. Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Click **Generate new token**
3. Select scopes:
   - `repo` — required for all tools
   - `write:discussion` — required for Galaxy Brain
4. Copy the token and paste it into the script's config block

> ⚠️ Never commit your token to a public repo. Add your scripts to `.gitignore` if you edit them with real credentials.

---

## Responsible use

These tools automate actions using your own GitHub accounts and your own repositories. They do not:

- Access anyone else's accounts or repos
- Bypass any GitHub security controls
- Violate GitHub's API rate limits (delays are built in)

GitHub's [Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) permit automation on your own repos within API rate limits. That said, badges are ultimately cosmetic — use these tools for fun and learning, not to misrepresent your contributions in a professional context.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `gh: command not found` | Install the [GitHub CLI](https://cli.github.com/) and run `gh auth login` |
| Push fails with 403 | Check your token has `repo` scope and the remote URL is correct |
| Galaxy Brain: can't mark answer | Make sure your repo has a **Q&A** discussion category, not just General |
| Galaxy Brain: errors after ~19 rounds | Increase `DELAY_SECONDS` to 25 or higher |
| Co-authored-by not appearing | The blank line between commit title and trailer is required — this is handled automatically by the script |
| Badge not showing up | Badges can take up to 24 hours to appear on your profile after the threshold is reached |

---

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

You may use, modify, and distribute this software freely — but any distributed version must also be open source under the same license. You cannot sell this as closed-source software.

Copyright (C) 2026 [03x1](https://github.com/03x1)
