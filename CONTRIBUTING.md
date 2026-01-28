# 🤝 Contributing to Unstop Internships Portal

Thank you for considering contributing to this project! This guide will help you get started.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/unstop-scraper.git
   cd unstop-scraper
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Test locally**
   ```bash
   quickstart.bat  # Windows
   # OR
   python test_scraper.py
   ```
6. **Commit and push**
   ```bash
   git add .
   git commit -m "✨ Add: Your feature description"
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## 🎯 Areas for Contribution

### 🐛 Bug Fixes
- Fix parsing errors for edge cases
- Improve error handling
- Fix responsive design issues

### ✨ New Features
Priority features we'd love to see:
- [ ] **Email Notifications** - Alert users of new internships
- [ ] **Telegram Bot** - Push notifications via Telegram
- [ ] **Advanced Filters** - Stipend range, duration, skills
- [ ] **Dark Mode** - Toggle for dark theme
- [ ] **Bookmark Feature** - Save favorites using localStorage
- [ ] **Export to CSV** - Download internships as spreadsheet
- [ ] **Analytics Dashboard** - View trends and statistics

### 🎨 UI/UX Improvements
- Mobile responsiveness enhancements
- Accessibility improvements (ARIA labels, keyboard navigation)
- Loading skeletons instead of spinners
- Improved animations
- Better error states

### 📚 Documentation
- Add screenshots to README
- Create video tutorial
- Translate documentation to other languages
- Add code comments
- Write more comprehensive tests

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to functions
- Keep functions small and focused

```python
def add_internship(self, item: Dict[str, Any]) -> bool:
    """
    Add internship to database if it doesn't exist.
    
    Args:
        item: Internship data from API
        
    Returns:
        True if added, False if duplicate
    """
```

### JavaScript
- Use modern ES6+ syntax
- Prefer `const` over `let`
- Use descriptive variable names
- Add comments for complex logic

```javascript
// Good
const filteredInternships = allInternships.filter(internship => 
    internship.title.toLowerCase().includes(searchTerm)
);

// Avoid
let fi = ai.filter(i => i.t.toLowerCase().includes(st));
```

### CSS
- Use CSS custom properties for theming
- Follow BEM naming convention where applicable
- Mobile-first responsive design
- Comment complex selectors

```css
/* Good */
.internship-card__header {
    display: flex;
    gap: var(--spacing-md);
}

/* Avoid */
.card > div:first-child {
    display: flex;
}
```

## 🧪 Testing

Before submitting a PR:

1. **Run the test suite**
   ```bash
   python test_scraper.py
   ```

2. **Test the scraper**
   ```bash
   python -m src.scraper
   ```

3. **Test the frontend**
   - Open `docs/index.html` in a browser
   - Test all filters and search
   - Check mobile responsiveness
   - Verify console has no errors

4. **Test with different data**
   - Empty results
   - Large datasets (100+ items)
   - Missing fields

## 📋 Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No console errors
- [ ] Mobile responsive
- [ ] Backwards compatible

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Description** - What happened?
2. **Expected Behavior** - What should happen?
3. **Steps to Reproduce**
   ```
   1. Go to '...'
   2. Click on '...'
   3. See error
   ```
4. **Environment**
   - OS: Windows/Mac/Linux
   - Browser: Chrome/Firefox/Safari
   - Python version
5. **Screenshots** - If applicable
6. **Logs** - Error messages or console logs

## 💡 Feature Requests

When requesting features:

1. **Use Case** - Why is this needed?
2. **Proposed Solution** - How should it work?
3. **Alternatives** - Other approaches considered?
4. **Mockups** - Visual representation (optional)

## 🏗️ Architecture Overview

```
Frontend (Static)           Backend (Python)         Storage
─────────────────          ─────────────────        ─────────
   index.html      <───>    scraper.py      <───>   SQLite DB
   styles.css                   ↓                       ↓
   app.js                  database.py             internships
       ↓                        ↓                    table
   Reads JSON            Exports JSON
       ↓                        ↓
internships.json  <──────  JSON export
```

### Key Components

1. **`src/scraper.py`** - Main scraper logic
   - Fetches from Unstop API
   - Paginates through results
   - Filters by date

2. **`src/database.py`** - Database operations
   - SQLite with ORM-like interface
   - Duplicate prevention
   - JSON export for web

3. **`src/api_client.py`** - HTTP requests
   - Handles API communication
   - Retry logic
   - Error handling

4. **`docs/app.js`** - Frontend logic
   - Loads JSON data
   - Implements search/filter
   - Renders cards dynamically

5. **`.github/workflows/scrape-deploy.yml`** - CI/CD
   - Scheduled scraping
   - Automated deployment

## 🎓 Learning Resources

New to these technologies?

- **Python**: [Real Python](https://realpython.com/)
- **SQLite**: [SQLite Tutorial](https://www.sqlitetutorial.net/)
- **JavaScript**: [MDN Web Docs](https://developer.mozilla.org/)
- **GitHub Actions**: [GitHub Docs](https://docs.github.com/en/actions)

## 💬 Communication

- **Issues** - For bugs and features
- **Discussions** - For questions and ideas
- **Pull Requests** - For code contributions

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn

## 🙏 Thank You!

Your contributions make this project better for everyone. Whether it's:
- Reporting a bug
- Suggesting a feature
- Improving documentation
- Writing code

Every contribution is valued! 🌟

---

**Happy Contributing!** 🚀

If you have questions, feel free to open an issue or discussion.
