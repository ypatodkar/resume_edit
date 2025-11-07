# 🔄 Recover Lost Code - Quick Guide

## What Happened?

If you lost code, here are ways to recover it:

## Method 1: Check Reflog (Most Common)

```bash
# See all recent actions
git reflog

# Find the commit/action before you lost code
# Then restore to that point:
git checkout <commit-hash>
# Or
git reset --hard <commit-hash>
```

## Method 2: Recover from Stash

```bash
# List all stashes
git stash list

# Apply a stash
git stash apply stash@{0}

# Or pop (apply and remove)
git stash pop stash@{0}
```

## Method 3: Recover Uncommitted Changes

If you had uncommitted changes that were lost:

```bash
# Check for dangling commits
git fsck --lost-found

# Look for lost commits
git log --all --reflog --oneline
```

## Method 4: Check IDE/Editor Recovery

- **VS Code**: Check `.vscode/` or local history
- **IntelliJ/WebStorm**: Local History feature
- **Sublime**: Check unsaved files

## Method 5: Restore from Backup Branch

If you created a backup:

```bash
# List all branches (including remote)
git branch -a

# Checkout backup branch
git checkout backup-branch
```

## Quick Recovery Commands

```bash
# 1. See what you lost
git reflog

# 2. Go back to before the loss
git reset --hard HEAD@{N}  # N = number of actions ago

# 3. Or checkout specific commit
git checkout <commit-hash>

# 4. Create new branch from recovered code
git checkout -b recovered-code
```

## Prevention

Always commit or stash before risky operations:

```bash
# Before reset/checkout
git stash save "backup before reset"
# Or
git commit -am "WIP: backup"
```

