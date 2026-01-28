# 🗺️ Navigation Guide - Unstop Internships Portal

Welcome! Here's where to find everything:

## 🚀 Getting Started

| Document | Purpose | When to Use |
|----------|---------|-------------|
| **[README.md](README.md)** | Main overview | Start here! Learn what this is |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Deploy to GitHub | Ready to go live? |
| **[quickstart.bat](quickstart.bat)** | Local setup script | Test on your computer |

## 📖 Understanding the Project

| Document | Purpose |
|----------|---------|
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | Technical architecture & design decisions |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | How to contribute & code style |

## 🏗️ Core Source Code

### Backend (Python)
```
src/
├── scraper.py       ← Main scraper (fetches & saves)
├── database.py      ← SQLite operations (NEW!)
├── api_client.py    ← HTTP requests to Unstop
├── config.py        ← Configuration loader
├── utils.py         ← Helper functions
└── models.py        ← Type definitions
```

### Frontend (Web)
```
docs/
├── index.html       ← Landing page structure
├── styles.css       ← Beautiful styling
├── app.js           ← Search, filter, render logic
└── data/
    └── internships.json  ← Data consumed by site
```

### Automation
```
.github/
└── workflows/
    └── scrape-deploy.yml  ← Daily cron & deploy
```

## 🎯 Common Tasks

### I want to...

**...understand how it works**
→ Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

**...run it locally**
→ Run `quickstart.bat` or follow README.md

**...deploy to GitHub**
→ Follow [DEPLOYMENT.md](DEPLOYMENT.md)

**...change the design**
→ Edit `docs/styles.css` (colors, fonts, layout)

**...modify scraper logic**
→ Edit `src/scraper.py` or `src/database.py`

**...add new features**
→ Read [CONTRIBUTING.md](CONTRIBUTING.md) first

**...change scrape schedule**
→ Edit `.github/workflows/scrape-deploy.yml` (cron line)

**...customize filters**
→ Edit `docs/app.js` (applyFilters function)

**...report a bug**
→ Open GitHub Issue with details

## 📁 File Reference

### Configuration
- `.env` - Your local settings (API_BASE_URL)
- `.env.example` - Template for .env
- `requirements.txt` - Python dependencies

### Data Storage
- `data/internships.db` - SQLite database (duplicates prevented)
- `data/internships/*.json` - Daily backups
- `docs/data/internships.json` - Public JSON for website

### Testing & Utilities
- `test_scraper.py` - Test suite
- `quickstart.bat` - Easy setup script (Windows)

### Documentation
- `README.md` - Main documentation
- `DEPLOYMENT.md` - GitHub deployment guide
- `PROJECT_SUMMARY.md` - Technical overview
- `CONTRIBUTING.md` - Contribution guide
- `INDEX.md` - This file!

## 🔑 Key Concepts

### How Duplicate Prevention Works
```
API → Scraper → Database (check unstop_id) → Add if new OR Skip if exists
```
The `unstop_id` field has a UNIQUE constraint in SQLite.

### How Daily Updates Work
```
9 AM UTC → GitHub Actions triggers
         → Runs scraper
         → Commits new data
         → Deploys to GitHub Pages
         → Site updates automatically
```

### How the Frontend Works
```
User visits → Fetch internships.json
           → Parse & render cards
           → User searches/filters
           → Filter client-side (no server needed)
```

## 🎨 Customization Quick Reference

### Change Brand Colors
**File:** `docs/styles.css`
```css
:root {
    --primary: #667eea;      /* Change this */
    --secondary: #764ba2;    /* And this */
}
```

### Change Site Title
**File:** `docs/index.html`
```html
<title>Your Custom Title</title>
<h1>Your Brand Name</h1>
```

### Change Scrape Time
**File:** `.github/workflows/scrape-deploy.yml`
```yaml
schedule:
  - cron: '0 9 * * *'  # 9 AM UTC - Change this
```

### Change Lookback Period
**File:** `.env`
```
HOURS_LOOKBACK=168  # 7 days (increase for more history)
```

## 🆘 Troubleshooting

### Issue: Scraper not running
**Check:**
1. API_BASE_URL is set in GitHub secrets
2. Workflow is enabled (Actions tab)
3. View logs in Actions → Latest run

### Issue: No data showing on site
**Check:**
1. `docs/data/internships.json` exists
2. JSON is valid (not empty or malformed)
3. Browser console for errors (F12)

### Issue: Duplicates appearing
**Check:**
1. Database constraint is working (run test_scraper.py)
2. unstop_id field is populated correctly
3. Check database directly: `sqlite3 data/internships.db`

### Issue: Site not updating
**Check:**
1. GitHub Pages is enabled (Settings → Pages)
2. gh-pages branch exists
3. Wait 2-3 minutes for CDN
4. Hard refresh (Ctrl+F5)

## 📞 Get Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Features:** Open a GitHub Issue with "Feature Request" label

## 🌟 Quick Links

- [Live Demo](https://yourusername.github.io/unstop-scraper/) (replace with your URL)
- [GitHub Repository](https://github.com/yourusername/unstop-scraper) (replace with your URL)
- [Unstop](https://unstop.com/)

---

**Happy Building! 🚀**

Still confused? Start with [README.md](README.md)!
