# 🚀 Deployment Guide for GitHub Pages

## Prerequisites
- GitHub account
- Repository with this code

## Step 1: Push to GitHub

```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "🚀 Initial commit: Unstop Internships Portal"

# Add remote (replace with your username)
git remote add origin https://github.com/yourusername/unstop-scraper.git

# Push to main branch
git push -u origin main
```

## Step 2: Configure Repository Secrets

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add the following secret:

### Required Secret
- **Name:** `API_BASE_URL`
- **Value:** `https://unstop.com/api/public/opportunity/search-new?opportunity=internships`

### Optional Variables (click on "Variables" tab)
- `HOURS_LOOKBACK`: `168` (scrape last 7 days)
- `API_PER_PAGE`: `20`
- `REQUEST_DELAY_SECONDS`: `2`

## Step 3: Enable GitHub Pages

1. Go to **Settings** → **Pages**
2. Under **Source**, select:
   - **Deploy from a branch**
3. Under **Branch**, select:
   - Branch: **gh-pages**
   - Folder: **/ (root)**
4. Click **Save**

## Step 4: Run First Scrape

1. Go to **Actions** tab
2. Click on **Daily Scraper & Deploy** workflow
3. Click **Run workflow** → **Run workflow**
4. Wait for the workflow to complete (2-3 minutes)
5. Check the logs to ensure it succeeded

## Step 5: Access Your Site

Your site will be live at:
```
https://yourusername.github.io/unstop-scraper/
```

Replace `yourusername` with your actual GitHub username.

## Step 6: Verify Everything Works

1. Visit your site URL
2. Check if internships are displayed
3. Test search and filters
4. Verify mobile responsiveness

## Troubleshooting

### Workflow Failed

**Check:**
- `API_BASE_URL` secret is set correctly
- API endpoint is accessible (test in browser/Postman)
- Review workflow logs in Actions tab

### No Data Showing

**Check:**
- `docs/data/internships.json` exists in `gh-pages` branch
- JSON file is not empty
- Browser console for JavaScript errors (F12)

### 404 Error on Site

**Check:**
- GitHub Pages is enabled
- `gh-pages` branch exists
- Wait 2-3 minutes for CDN to update
- Try accessing with `/index.html` explicitly

### Database Not Persisting

**Note:** SQLite database is stored in the repository. Ensure:
- `data/internships.db` is being committed
- Git LFS is not interfering (should be < 100MB)

## Customization After Deployment

### Change Site Title/Branding

Edit `docs/index.html`:
```html
<title>Your Custom Title</title>
<h1>Your Brand Name</h1>
```

### Change Colors

Edit `docs/styles.css`:
```css
:root {
    --primary: #your-color;
    --secondary: #your-color;
}
```

### Update Cron Schedule

Edit `.github/workflows/scrape-deploy.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # Change this
```

Then commit and push:
```bash
git add .github/workflows/scrape-deploy.yml
git commit -m "Update scrape schedule"
git push
```

## Monitoring

### Check Last Run

Go to **Actions** tab to see:
- Last scrape time
- Success/failure status
- Number of internships added
- Logs and artifacts

### Email Notifications

GitHub automatically sends emails for workflow failures.

## Advanced: Custom Domain

1. Buy a domain (e.g., internships.yourdomain.com)
2. Add DNS records:
   ```
   CNAME internships yourusername.github.io
   ```
3. In repository settings → Pages → Custom domain:
   - Enter: `internships.yourdomain.com`
   - Enable **Enforce HTTPS**

## Cost

**Total: $0/month** 🎉
- GitHub Actions: 2,000 minutes/month free
- GitHub Pages: Unlimited hosting
- SQLite: No cloud database costs

## Support

Having issues? [Open an issue](https://github.com/yourusername/unstop-scraper/issues) on GitHub!
