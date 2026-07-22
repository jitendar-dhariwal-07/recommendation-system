# GitHub Setup & Deployment Guide (Windows PowerShell)

This guide walks you through pushing the Recommendation System project to GitHub using PowerShell on Windows.

## 📋 Prerequisites

1. **Git installed**: Download from https://git-scm.com/download/win
2. **GitHub account**: Sign up at https://github.com
3. **GitHub Desktop** (optional): For GUI-based workflow
4. **PowerShell Terminal**: Built into Windows

## 🚀 Step-by-Step GitHub Deployment

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `recommendation-system`
3. Description: "Production-quality recommendation system with multiple algorithms"
4. Choose: **Public** (for portfolio visibility)
5. Do NOT initialize with README (we have our own)
6. Click **Create repository**

**Copy your repository URL** (looks like: `https://github.com/yourusername/recommendation-system.git`)

### Step 2: Initialize Local Repository

Open PowerShell in your project directory:

```powershell
# Navigate to project folder
cd C:\Users\HP\Downloads\recommendation-system

# Initialize git repository
git init

# Verify git initialization
git status
```

### Step 3: Configure Git Identity

```powershell
# Set your GitHub username
git config --global user.name "Your Name"

# Set your GitHub email
git config --global user.email "your.email@gmail.com"

# Verify configuration
git config --global --list
```

### Step 4: Add Files to Staging

```powershell
# Add all project files
git add .

# Verify files are staged
git status

# Expected output should show all files in green
```

### Step 5: Create Initial Commit

```powershell
# Create commit with message
git commit -m "Initial commit: Production-quality recommendation system

- Implemented content-based filtering with 3 similarity metrics
- Added collaborative filtering with k-NN approach
- Created hybrid recommendation algorithm
- Built interactive CLI with multiple datasets (Books, Movies, Courses)
- Comprehensive test suite with 28+ unit tests
- Professional documentation and examples
- Portfolio-ready project structure"
```

### Step 6: Connect to GitHub Repository

```powershell
# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/recommendation-system.git

# Verify remote is added
git remote -v

# Expected output:
# origin  https://github.com/yourusername/recommendation-system.git (fetch)
# origin  https://github.com/yourusername/recommendation-system.git (push)
```

### Step 7: Push to GitHub

```powershell
# For first push, set upstream branch
git branch -M main
git push -u origin main

# You'll be prompted for GitHub credentials
# Use your GitHub username and personal access token (not password)
```

#### If You Get Authentication Error:

**Option A: Using Personal Access Token (Recommended)**

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `workflow`
4. Copy the token
5. Use as password in PowerShell prompt

**Option B: Using SSH Key (Secure)**

```powershell
# Generate SSH key
ssh-keygen -t ed25519 -C "your.email@gmail.com"

# Press Enter for default location
# Enter passphrase (or leave empty)

# Copy public key
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# Go to GitHub → Settings → SSH and GPG keys → New SSH key
# Paste the key and save

# Test SSH connection
ssh -T git@github.com

# You should see: "Hi yourusername! You've successfully authenticated"
```

### Step 8: Verify Upload

```powershell
# Check push was successful
git status

# Expected: "On branch main, Your branch is up to date with 'origin/main'."

# View remote branches
git branch -a

# Expected: "* main" and "remotes/origin/main"
```

## 📝 Common PowerShell Git Commands

### View Commit History

```powershell
# Simple log
git log --oneline

# Detailed log
git log

# Graph view
git log --oneline --graph --all
```

### Make Changes and Push Updates

```powershell
# View changed files
git status

# Add specific file
git add .\filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to GitHub
git push origin main
```

### Undo Changes

```powershell
# Undo changes to a file (before commit)
git restore .\filename.py

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

### Create Branches for Features

```powershell
# Create new branch
git branch feature/new-algorithm

# Switch to branch
git checkout feature/new-algorithm

# Or create and switch in one command
git checkout -b feature/new-algorithm

# Push branch to GitHub
git push origin feature/new-algorithm

# View all branches
git branch -a

# Merge branch back to main
git checkout main
git merge feature/new-algorithm
```

## 🏷️ Adding GitHub Topics (Optional)

These help with discoverability:

1. Go to your GitHub repository
2. Click **Settings** → **About**
3. Add topics: `recommendation-system`, `machine-learning`, `python`, `portfolio`

## 📊 GitHub Actions (Continuous Integration)

### Create Tests Workflow

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: pytest test_recommendation.py -v
```

Commit and push this file to enable automatic test runs.

## 🎯 Portfolio Profile Tips

### Update GitHub Profile

1. Add profile picture
2. Add bio: "Software Engineer | ML Enthusiast | Portfolio Projects"
3. Add website/blog link
4. Pin your recommendation-system repo

### Create GitHub Pages (Optional)

Make your project visible with a website:

1. Go to repository **Settings**
2. Scroll to **GitHub Pages**
3. Choose source: `main` branch
4. Save
5. Your project site: `https://yourusername.github.io/recommendation-system`

### Showcase Your Work

Add badges to README:

```markdown
[![Tests](https://github.com/yourusername/recommendation-system/workflows/Tests/badge.svg)](https://github.com/yourusername/recommendation-system/actions)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

## 📊 Tracking Your Progress

### View GitHub Statistics

PowerShell command to see commit stats:

```powershell
# Count commits by author
git log --oneline | Measure-Object -Line

# See top contributors
git shortlog -sne

# Get repository size
$size = (git count-objects -v | Select-String "size-pack" | ForEach-Object { $_ -split '\s+' } | Select-Object -Index 1)
Write-Host "Repository size: $size KB"
```

## 🔒 Best Practices

### .gitignore Review

Ensure `.gitignore` prevents:

```powershell
# Check what's ignored
git check-ignore -v *

# Clear git cache (if needed)
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
```

### Commit Message Format

Use clear, descriptive messages:

```
feat: Add new similarity metric
fix: Correct Euclidean distance calculation
docs: Update README with examples
test: Add edge case tests
refactor: Improve code organization
```

### Collaborative Development

```powershell
# Before working on new feature
git pull origin main

# Create feature branch
git checkout -b feature/description

# Push regularly
git push origin feature/description

# Create Pull Request on GitHub
# After review, merge to main
```

## 🐛 Troubleshooting

### Issue: "fatal: No commits yet"

```powershell
# Make sure you have committed files
git commit -m "Initial commit"

# Then push
git push -u origin main
```

### Issue: "rejected updates because the tip of your current branch is behind"

```powershell
# Pull latest changes first
git pull origin main

# Then push
git push origin main
```

### Issue: "Detached HEAD state"

```powershell
# Get back to main
git checkout main

# Force sync with remote
git fetch origin
git reset --hard origin/main
```

### Issue: Large file pushing

```powershell
# Check file size
(Get-Item .\large_file.zip).Length / 1MB

# Remove if over 100MB
git rm .\large_file.zip
git commit -m "Remove large file"
git push
```

## ✅ Final Verification

```powershell
# Verify all files uploaded
git ls-files | Measure-Object -Line

# Check repository connection
git remote show origin

# View branches
git branch -a

# See latest commits
git log --oneline -5
```

## 🎉 You're Done!

Your portfolio project is now on GitHub! 

**Next Steps:**
1. Share repository URL with recruiters
2. Add link to your resume/portfolio
3. Keep making commits as you improve the project
4. Pin this repository on your GitHub profile

### Showcase Template

Use this in your GitHub bio or portfolio:

```
📊 Recommendation System
A production-quality recommendation engine with multiple algorithms
- Content-based & collaborative filtering
- 3 similarity metrics (Cosine, Euclidean, Jaccard)
- Hybrid approach for optimal recommendations
- 28+ comprehensive unit tests
- Interactive CLI with sample datasets
🔗 github.com/yourusername/recommendation-system
```

---

**GitHub Profile URL**: https://github.com/yourusername

**Repository URL**: https://github.com/yourusername/recommendation-system

**Your Project is Live!** 🚀
