# Execute PRP

Execute the implementation plan defined in a PRP file.

**PRP file:** $ARGUMENTS

A PRP is a reviewed blueprint. Your job is to follow it faithfully, run the validation gates, and produce working code — not to redesign the feature.

## Steps

### 1. Load the PRP
Read the file at `$ARGUMENTS` end-to-end. Extract:
- The **Implementation Plan** (ordered work to do)
- The **Validation Gates** (checks that must pass)
- The **Success Criteria** (user-facing outcomes)
- The **Relevant Files** (what to read for grounding)

If the PRP has an "Open Questions" section with unresolved items, **stop and surface them** before writing any code.

### 2. Re-ground in the codebase
Before implementing:
- Re-read `CLAUDE.md`
- Read every file in the PRP's "Relevant Files" section
- Read existing `.claude/commands/*.md` to match the established pattern

### 3. Implement in order
Work through the Implementation Plan **section by section**, in the order written. For each section:
1. Create or edit the file the PRP names
2. Follow the Steps inside that section literally
3. Match the style of existing slash commands in `.claude/commands/`
4. Use `$ARGUMENTS` for any path or value the user passes in
5. After finishing the section, run its Validation Gate checks (see step 4)

Do not skip ahead. Do not reorder. If you discover the PRP is wrong, **stop and report** — do not silently improvise.

### 4. Run validation gates
After each implementation section, verify the gates that apply:
- **File-existence gates** — confirm files were created at the paths specified
- **Pattern gates** — confirm `$ARGUMENTS` is used, schemas match CLAUDE.md, conventions are followed
- **Behavior gates** — when a gate says "running `/x` produces `y`", run a representative test by reading the output you'd produce against a sample input from `events/` or `data/`

If a gate fails, fix the issue before moving on.

### 5. Final integration check
Once all implementation sections are complete:
- Re-read each new file you created
- Walk the full pipeline mentally: does the output of one command satisfy the input contract of the next?
- Confirm naming conventions (kebab-case files, camelCase JSON keys) hold across every new file

### 6. Report
Print a summary:
- Files created (full paths)
- Files modified (full paths)
- Gates passed / failed
- Any deviations from the PRP, with a one-line reason for each
- Suggested next command for the user to test (e.g., `/build-schedule events/your-event.json`)

## IMPORTANT

- **Follow the PRP, don't redesign it.** If the PRP is wrong, surface it — don't silently fix.
- **No new abstractions.** Match the existing slash command style. A slash command is a markdown file with instructions and `$ARGUMENTS` — not code.
- **Respect CLAUDE.md.** Every output format, naming convention, and tone rule there is binding.
- **Fail loudly.** If a validation gate cannot be satisfied, stop and report rather than producing partial output that looks finished.
- **No code outside the PRP's scope.** If the user wants more, that's a new INITIAL.md.
