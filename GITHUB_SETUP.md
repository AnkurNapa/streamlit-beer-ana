# 🍺 GitHub Setup & Deployment

Complete guide to push this project to GitHub and use it.

---

## Step 1: Create GitHub Repository

### Option A: GitHub Web UI (Easiest)

1. Go to https://github.com/new
2. Repository name: `streamlit-beer-ana`
3. Description: "Master Brewer - Live Beer Analytics Platform"
4. Choose: **Public** (for easy sharing)
5. Click **Create repository**
6. Copy the repository URL (looks like: `https://github.com/your-username/streamlit-beer-ana.git`)

### Option B: GitHub CLI

```bash
gh repo create streamlit-beer-ana --public --source=. --remote=origin --push
```

---

## Step 2: Add Remote & Push to GitHub

Replace `YOUR_USERNAME` with your GitHub username:

```bash
# Add remote (only if you created via web UI)
git remote add origin https://github.com/YOUR_USERNAME/streamlit-beer-ana.git

# Rename branch to main (if needed)
git branch -M main

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Master Brewer - Live Beer Analytics Platform"

# Push to GitHub
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 42, done.
Counting objects: 100% (42/42), done.
Delta compression using up to 8 threads
Compressing objects: 100% (38/38), done.
Writing objects: 100% (42/42), 245.89 KiB | 1.2 MiB/s
Creating branch tracking information for branch 'main' based on 'origin/main'.
...
To github.com:YOUR_USERNAME/streamlit-beer-ana.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main/main'.
```

✅ **Done!** Your code is now on GitHub.

---

## Step 3: Use Project from GitHub

### For Personal Use

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/streamlit-beer-ana.git
cd streamlit-beer-ana

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install streamlit plotly pandas numpy firecrawl-py python-dotenv

# Set API key
export FIRECRAWL_API_KEY="your_api_key_here"

# Run app
streamlit run app_streaming.py
```

Visit: http://localhost:8501

### For Sharing with Others

Share the GitHub URL:
```
https://github.com/YOUR_USERNAME/streamlit-beer-ana
```

Others can clone and run it:
```bash
git clone https://github.com/YOUR_USERNAME/streamlit-beer-ana.git
cd streamlit-beer-ana
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FIRECRAWL_API_KEY="their_api_key"
streamlit run app_streaming.py
```

---

## Step 4: Deploy to Streamlit Cloud (Optional)

### Free Hosting on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Sign in with your GitHub account
3. Click **New app**
4. Select:
   - Repository: `YOUR_USERNAME/streamlit-beer-ana`
   - Branch: `main`
   - Main file path: `app_streaming.py`
5. Click **Deploy**

### Add Environment Variables

In Streamlit Cloud dashboard:
1. Click your app
2. Settings (gear icon)
3. Add secret: `FIRECRAWL_API_KEY=your_key`
4. Reboot app

**Your app is now live!** Share the URL: `https://share.streamlit.io/YOUR_USERNAME/streamlit-beer-ana/app_streaming.py`

---

## Create requirements.txt

For easier setup:

```bash
pip freeze > requirements.txt
```

This creates a `requirements.txt` file. Then anyone can install with:
```bash
pip install -r requirements.txt
```

---

## File Structure on GitHub

```
streamlit-beer-ana/
├── app_streaming.py              # Main app (streaming)
├── app_comprehensive.py          # Alternative app (static)
├── streaming_loader.py           # Streaming data loader
├── data_loader_enhanced.py       # Static data loader
├── scraper_enhanced.py           # Data scraper
│
├── README.md                      # Project overview
├── STREAMING_ARCHITECTURE.md      # Architecture guide
├── GETTING_STARTED.md            # Getting started
├── GITHUB_SETUP.md               # This file
├── QUICK_START.md                # Quick start
│
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── .env.example                  # Example env vars
│
└── data/                         # Data directory (optional)
    └── beer-analytics-full/      # Scraped data (optional)
```

---

## Push Future Changes

After making changes locally:

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: Add new feature description"

# Push to GitHub
git push origin main
```

---

## Branching (Optional)

For collaborative development:

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: Add new feature"

# Push to GitHub
git push origin feature/new-feature

# On GitHub: Create Pull Request to merge into main
```

---

## .env.example

Create this file so others know what environment variables are needed:

```bash
# Copy to .env and fill in your values
FIRECRAWL_API_KEY=your_api_key_here
```

---

## GitHub Actions (Optional CI/CD)

Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - run: pip install -r requirements.txt
      - run: python -m py_compile *.py
```

---

## Common Tasks

### Update from GitHub

```bash
# Pull latest changes
git pull origin main
```

### Check remote

```bash
# View remote URLs
git remote -v

# Expected output:
# origin  https://github.com/YOUR_USERNAME/streamlit-beer-ana.git (fetch)
# origin  https://github.com/YOUR_USERNAME/streamlit-beer-ana.git (push)
```

### View commits

```bash
# See commit history
git log --oneline -10
```

### See changes

```bash
# Changes not yet staged
git status

# Detailed changes
git diff
```

---

## Troubleshooting

### Problem: "fatal: not a git repository"

**Solution:**
```bash
cd /path/to/streamlit-beer-ana
git status  # Should work now
```

### Problem: "Permission denied" when pushing

**Solution 1: Use Personal Access Token**
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/streamlit-beer-ana.git
git push origin main
```

Get token from: https://github.com/settings/tokens

**Solution 2: Use SSH**
```bash
# Generate SSH key (if not exists)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: https://github.com/settings/ssh/new

# Update remote URL
git remote set-url origin git@github.com:YOUR_USERNAME/streamlit-beer-ana.git
git push origin main
```

### Problem: "Your branch is ahead of 'origin/main'"

**Solution:**
```bash
# Push your commits
git push origin main
```

---

## Summary

✅ **Steps:**
1. Create GitHub repo
2. Push code: `git push -u origin main`
3. Share URL or deploy to Streamlit Cloud

✅ **To use from GitHub:**
```bash
git clone https://github.com/YOUR_USERNAME/streamlit-beer-ana.git
cd streamlit-beer-ana
pip install -r requirements.txt
export FIRECRAWL_API_KEY="key"
streamlit run app_streaming.py
```

✅ **To deploy:**
- Streamlit Cloud: https://share.streamlit.io/
- Heroku/Railway: Requires Procfile
- Any server: Just run streamlit command

---

**GitHub URL:** `https://github.com/YOUR_USERNAME/streamlit-beer-ana`

🚀 Ready to share and deploy!
