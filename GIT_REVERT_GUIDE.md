# Git: Revert to Previous Commit and Add Changes

## Common Scenarios

### Scenario 1: Undo Last Commit, Keep Changes, Add More

**You want to:**
- Undo the last commit
- Keep the changes in your working directory
- Add more changes

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Or undo last commit, keep changes unstaged
git reset HEAD~1

# Now add your new changes
git add .
git commit -m "New commit message"
```

### Scenario 2: Undo Last Commit, Discard Changes, Start Fresh

**You want to:**
- Completely undo the last commit
- Discard all changes
- Start from previous commit

```bash
# ⚠️ WARNING: This discards all changes!
git reset --hard HEAD~1
```

### Scenario 3: Revert to Specific Commit, Keep Changes

**You want to:**
- Go back to a specific commit
- Keep your current changes

```bash
# See commit history
git log --oneline

# Reset to specific commit (keep changes)
git reset <commit-hash>

# Or reset to specific commit (discard changes)
git reset --hard <commit-hash>
```

### Scenario 4: Create New Branch from Previous Commit

**You want to:**
- Keep current work
- Start from previous commit in new branch

```bash
# Create new branch from previous commit
git checkout -b new-branch HEAD~1

# Or from specific commit
git checkout -b new-branch <commit-hash>
```

## Common Commands

### View History
```bash
# Short format
git log --oneline -10

# Detailed format
git log -5

# With graph
git log --oneline --graph -10
```

### Reset Options

| Command | What It Does |
|---------|-------------|
| `git reset --soft HEAD~1` | Undo commit, keep changes **staged** |
| `git reset HEAD~1` | Undo commit, keep changes **unstaged** |
| `git reset --hard HEAD~1` | Undo commit, **discard all changes** ⚠️ |
| `git reset --soft <hash>` | Reset to commit, keep changes staged |
| `git reset <hash>` | Reset to commit, keep changes unstaged |
| `git reset --hard <hash>` | Reset to commit, discard changes ⚠️ |

### Revert (Safe Alternative)

**Creates a new commit that undoes changes:**

```bash
# Revert last commit (creates new commit)
git revert HEAD

# Revert specific commit
git revert <commit-hash>
```

## Step-by-Step: Most Common Use Case

### Undo Last Commit, Add More Changes

```bash
# 1. See what you're undoing
git log --oneline -5

# 2. Undo last commit, keep changes
git reset HEAD~1

# 3. Check status
git status

# 4. Add your new changes
git add .

# 5. Commit everything together
git commit -m "Updated changes with new additions"
```

## Examples

### Example 1: Undo Last Commit, Keep Working

```bash
# Current state: You have commit "Fix CORS" but want to add more
git log --oneline
# abc123 Fix CORS
# def456 Previous commit

# Undo "Fix CORS" but keep the changes
git reset HEAD~1

# Now make more changes
# ... edit files ...

# Add and commit everything
git add .
git commit -m "Fix CORS and add new features"
```

### Example 2: Go Back 3 Commits

```bash
# See history
git log --oneline
# abc123 Latest
# def456 Middle
# ghi789 Older
# jkl012 Oldest

# Go back 3 commits, keep changes
git reset HEAD~3

# Or go to specific commit
git reset ghi789
```

## ⚠️ Warnings

1. **`--hard` discards all changes** - Use carefully!
2. **If already pushed** - Use `git revert` instead of `reset`
3. **Backup first** - Create a branch before resetting:
   ```bash
   git branch backup-branch
   git reset HEAD~1
   ```

## If You Already Pushed

**Don't use `reset` if you already pushed!** Use `revert` instead:

```bash
# Revert creates a new commit (safe for shared repos)
git revert HEAD

# Then add your new changes
git add .
git commit -m "New changes"
```

## Quick Reference

```bash
# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes unstaged  
git reset HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Go back N commits
git reset HEAD~N

# Go to specific commit
git reset <commit-hash>

# Safe revert (if already pushed)
git revert HEAD
```

## Need Help?

- `git log --oneline` - See commit history
- `git status` - See current state
- `git diff` - See what changed
- `git reflog` - See all actions (can recover!)

