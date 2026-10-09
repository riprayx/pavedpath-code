# Migration to PavedPath Code

`github-solution-research` was renamed to **PavedPath Code**.

- Skill name: `pavedpath-code`
- Display name: `PavedPath Code`

Keep only one of the two names active. Some runtimes scan Skill directories recursively and would load both.

## Replace an old installation safely

The commands below use Codex's user Skill directory. Replace `SKILLS` with your runtime's directory, for example `~/.claude/skills` for Claude Code. Nothing is deleted: old copies are moved to a dated backup outside the active Skill root.

```bash
SKILLS=~/.agents/skills
BACKUP=~/skill-backups/$(date +%Y%m%d-%H%M%S)
mkdir -p "$SKILLS" "$BACKUP"

# Move any existing copies out of the active root.
for old in github-solution-research pavedpath-code; do
  [ -e "$SKILLS/$old" ] && mv "$SKILLS/$old" "$BACKUP/"
done

git clone https://github.com/riprayx/pavedpath-code.git "$SKILLS/pavedpath-code"
```

If the backup contains local edits you want to keep, compare them with `diff -ru "$BACKUP/pavedpath-code" "$SKILLS/pavedpath-code"` and copy them over. Delete the backup only once the new installation works.

## Behavior changes in 1.0.0

The Skill no longer requires the GitHub CLI, answers default to a compact shape, and several out-of-scope rules were removed. See the 1.0.0 entry in [CHANGELOG.md](CHANGELOG.md).
