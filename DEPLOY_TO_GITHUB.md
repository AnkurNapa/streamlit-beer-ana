# 🚀 Deploy Master Brewer to GitHub

Complete step-by-step guide to push this project to GitHub and share it.

---

## Quick Summary

**What you get:**
- ✅ Your code on GitHub (safe backup)
- ✅ Easy sharing with others
- ✅ Free hosting via Streamlit Cloud
- ✅ Version control for future changes

**Time needed:** 5 minutes

---

## Step 1: Create GitHub Account (if needed)

1. Go to https://github.com
2. Sign up for free
3. Verify your email

**Already have an account?** → Skip to Step 2

---

## Step 2: Create Your Repository on GitHub

### Method A: Using Web UI (Easiest)

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `streamlit-beer-ana`
   - **Description:** `Master Brewer - Live Beer Analytics Platform`
   - **Visibility:** Public (so others can see it)
3. Click **Create repository**
4. **Copy the repository URL** (you'll need it in Step 3)

Example URL: `https://github.com/your-username/streamlit-beer-ana.git`

### Method B: Using GitHub CLI (If installed)

```bash
gh repo create streamlit-beer-ana --public
```

---

## Step 3: Push Your Code to GitHub

In the terminal, inside the `streamlit_beer_ana` directory:

```bash
# 1. Configure git (first time only)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 2. Add remote (replace with YOUR URL from Step 2)
git remote add origin https://github.com/YOUR_USERNAME/streamlit-beer-ana.git

# 3. Rename branch to main (if needed)
git branch -M main

# 4. Push your code
git push -u origin main
```

**Expected output:**
```
Enumerating objects: 73, done.
...
To github.com:YOUR_USERNAME/streamlit-beer-ana.git
 * [new branch]      main -> main
✅ Success!
```

---

## Step 4: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/streamlit-beer-ana`
2. You should see:
   - ✅ All your Python files
   - ✅ README and documentation
   - ✅ requirements.txt
   - ✅ .gitignore
   - ✅ Your code history

---

## Step 5: Share Your Repository

### Share the URL

Send this link to anyone:
```
https://github.com/YOUR_USERNAME/streamlit-beer-ana
```

They can:
- View your code
- Clone it
- Run it locally

### Clone & Run (for others)

Anyone can run your app by:

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/streamlit-beer-ana.git
cd streamlit-beer-ana

# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run
export FIRECRAWL_API_KEY="their_api_key"
streamlit run app_streaming.py
```

---

## Step 6: Deploy to Streamlit Cloud (Optional - Free)

Host your app for free on Streamlit Cloud!

### 6a. Go to Streamlit Cloud

1. Visit https://share.streamlit.io/
2. Click **Sign in with GitHub**
3. Authorize Streamlit to access your repos

### 6b. Deploy Your App

1. Click **New app**
2. Select:
   - **Repository:** YOUR_USERNAME/streamlit-beer-ana
   - **Branch:** main
   - **Main file:** app_streaming.py
3. Click **Deploy**

**Status:** 🟡 "Building" → 🟢 "Running" (takes 1-2 min)

### 6c: Add API Key (Required)

1. Go to your app in Streamlit Cloud
2. Click **Settings** (gear icon, top right)
3. Click **Secrets**
4. Paste:
   ```
   FIRECRAWL_API_KEY=your_actual_api_key
   ```
5. Click **Save**
6. Streamlit auto-reboots → **Done!**

### 6d: Share Live App

Your app is now live! Share this URL:

```
https://share.streamlit.io/YOUR_USERNAME/streamlit-beer-ana/app_streaming.py
```

Anyone can use it without installing anything! 🎉

---

## File Structure on GitHub

```
streamlit-beer-ana/
│
├── 📄 README.md                      # Project overview
├── 📄 GETTING_STARTED.md             # Getting started guide
├── 📄 STREAMING_ARCHITECTURE.md      # How it works
├── 📄 GITHUB_SETUP.md                # GitHub guide
│
├── 🐍 app_streaming.py               # Main app (streaming) ⭐
├── 🐍 app_comprehensive.py           # Alternative app (static)
├── 🐍 streaming_loader.py            # Live streaming loader
├── 🐍 data_loader_enhanced.py        # Static loader
│
├── 📋 requirements.txt               # Python dependencies
├── 📋 .gitignore                     # Git ignore rules
├── 📋 .env.example                   # Example config
│
└── 📁 data/                          # Data files (optional)
```

---

## Common Tasks

### Make Changes & Push to GitHub

```bash
# Edit files locally
# Then:

git add .
git commit -m "feat: Add new feature"
git push origin main
```

### Pull Latest Changes

If you cloned elsewhere:

```bash
git pull origin main
```

### Create a Branch (for features)

```bash
# Create branch
git checkout -b feature/my-feature

# Make changes
git add .
git commit -m "feat: My new feature"
git push origin feature/my-feature

# On GitHub: Create Pull Request to merge into main
```

---

## Troubleshooting

### Problem: "fatal: not a git repository"

**Solution:** Make sure you're in the right directory:
```bash
cd /path/to/streamlit-beer-ana
git status
```

### Problem: Permission denied when pushing

**Solution 1: Use GitHub CLI**
```bash
gh auth login
# Follow prompts
git push origin main
```

**Solution 2: Use Personal Access Token**
1. Go to https://github.com/settings/tokens
2. Create new token (check `repo`)
3. Copy token
4. In terminal:
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/streamlit-beer-ana.git
   git push origin main
   ```

### Problem: Streamlit Cloud won't start

**Solution:**
1. Check requirements.txt is valid
2. Check API key is set (Secrets)
3. Check main file exists: `app_streaming.py`
4. View logs in Streamlit Cloud dashboard

---

## What's in Your Repository

### Code Files
- `app_streaming.py` - Live streaming app (recommended)
- `streaming_loader.py` - Streaming loader class
- `data_loader_enhanced.py` - Static loader
- `scraper_enhanced.py` - Data scraper

### Documentation
- `README.md` - Project overview
- `STREAMING_ARCHITECTURE.md` - How streaming works
- `GETTING_STARTED.md` - Getting started
- `QUICK_START.md` - 5-minute setup

### Configuration
- `requirements.txt` - Dependencies
- `.gitignore` - What to ignore
- `.env.example` - Environment template

---

## Summary

| Step | Action | Time |
|------|--------|------|
| 1 | Create GitHub account | 5 min |
| 2 | Create repository | 1 min |
| 3 | Push code | 2 min |
| 4 | Verify on GitHub | 1 min |
| 5 | Share URL | Done! |
| **OPTIONAL:** |
| 6a | Deploy to Streamlit Cloud | 5 min |
| 6b | Add API key | 1 min |
| 6c | Share live app | Done! |

---

## What You Get

✅ **Code on GitHub**
- Safe backup
- Version history
- Easy collaboration

✅ **Shareable URL**
- `https://github.com/YOUR_USERNAME/streamlit-beer-ana`
- Others can clone and run

✅ **Free Hosting (Optional)**
- `https://share.streamlit.io/YOUR_USERNAME/streamlit-beer-ana/app_streaming.py`
- Live app anyone can use

✅ **Easy Updates**
- Make changes locally
- `git push origin main`
- Streamlit Cloud auto-deploys

---

## Next Steps

### Immediate (Required)
```bash
# Push to GitHub
git push -u origin main

# Verify at
https://github.com/YOUR_USERNAME/streamlit-beer-ana
```

### Optional (Recommended)
```bash
# Deploy to Streamlit Cloud
# 1. Go to https://share.streamlit.io/
# 2. Select your repo
# 3. Wait ~2 min for deploy
# 4. Add FIRECRAWL_API_KEY in Secrets
# 5. Share the live URL!
```

---

## Resources

- **GitHub Guides:** https://guides.github.com/
- **Git Tutorial:** https://git-scm.com/docs
- **Streamlit Cloud:** https://share.streamlit.io/
- **Streamlit Docs:** https://docs.streamlit.io/

---

## Example Workflow

```
1. You make changes locally
   ↓
2. git add . && git commit -m "message"
   ↓
3. git push origin main
   ↓
4. GitHub updated automatically
   ↓
5. Streamlit Cloud sees update
   ↓
6. Auto-redeploys your live app (1 min)
   ↓
7. Your URL shows new version instantly
```

---

## Questions?

- **GitHub Issues:** Open an issue on your repo
- **Streamlit Support:** https://discuss.streamlit.io/
- **Firecrawl Help:** https://www.firecrawl.dev/docs

---

**Your Master Brewer app is ready to share!** 🍺

Push to GitHub → Deploy to Cloud → Share with the world! 🌍
