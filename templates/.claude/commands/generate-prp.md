---
name: generate-prp
description: Generate a Product Requirements Prompt (PRP) blueprint from an INITIAL.md feature request. Reads the feature request, researches the codebase, and writes a reviewable PRP to PRPs/{slug}.md.
argument-hint: [INITIAL.md]
allowed-tools: Read, Write, Glob, Grep
---

# Generate PRP

Generate a comprehensive Product Requirements Prompt (PRP) from a feature request.

**Feature request file:** $ARGUMENTS

A PRP is an implementation blueprint: complete context, an ordered plan, validation gates, and risks. It is what the AI follows when actually building the feature, so accuracy here saves rework later.

## Steps

### 1. Read the feature request
Read the file at `$ARGUMENTS` (typically `INITIAL.md`). Extract the four sections:
- **FEATURE** — what to build
- **EXAMPLES** — files to learn from
- **DOCUMENTATION** — schemas, constraints, references
- **OTHER CONSIDERATIONS** — gotchas, edge cases

If any section is missing or vague, note it and proceed using best inference — but flag it in the PRP under "Open Questions".

### 2. Research the codebase
Before writing anything, ground yourself in the project:
- Read `CLAUDE.md` for agent personality, schemas, conventions, tone, constraints
- Read every file referenced in the EXAMPLES section
- Read existing slash commands in `.claude/commands/` to learn the pattern new commands should follow
- Read `data/` files referenced (e.g., `data/speakers.json`, `data/venues.json`) to understand real input shapes
- Read any `examples/` files referenced for output style

### 3. Pick a PRP filename
Derive a kebab-case slug from the FEATURE (e.g., "communications and scheduling system" → `meetup-comms`). The PRP will be written to `PRPs/{slug}.md`.

### 4. Generate the PRP
Write `PRPs/{slug}.md` with these sections, in this order:

```markdown
# PRP: {Title}

## Context
2-3 sentence summary: what currently exists, what this PRP adds, how it integrates.

### Relevant Files
Bulleted list of every file the implementation will read or follow patterns from. One line each: `path — what it provides`.

### Key Constraints from CLAUDE.md
Pull out the rules that govern this feature (schemas, naming conventions, tone, timing, validation rules).

## Implementation Plan
For each new file or command, write a sub-section:

### Command/File N: `name`
**File**: full path
**Purpose**: 1-sentence description
**Input**: what `$ARGUMENTS` is, or what the file consumes
**Steps**:
1. Ordered, concrete actions
2. Each step references specific files/data when relevant
3. Validation actions go inline (e.g., "check no speaker is double-booked")
**Output files**: paths the command writes

## Directory Structure (New)
ASCII tree of any new folders/files this PRP introduces.

## Validation Gates
Numbered gates with checkbox lists. Each gate is a verifiable check after implementation:
- Gate 1: Files exist and follow patterns
- Gate 2: Command N produces expected outputs for a known input
- Gate 3: Constraints are enforced (no double-booking, schemas validate, etc.)
- Gate 4: Integration with existing commands works end-to-end

## Success Criteria
Numbered list of user-facing outcomes that prove the feature works. Frame these as "a user can ___".

## Risks & Mitigations
Markdown table: `| Risk | Mitigation |` covering at least:
- Data shape mismatch between commands
- Missing/optional fields in input JSON
- Tone or format drift from CLAUDE.md
- Anything called out in OTHER CONSIDERATIONS

## Open Questions (if any)
Anything the INITIAL.md left ambiguous that the user should clarify before /execute-prp runs.

## Estimated Effort
Per-component complexity estimate (Low / Medium / High) and rough total time.
```

### 5. Confirm
After writing, print:
- The PRP file path (`PRPs/{slug}.md`)
- A 3-bullet summary: what will be built, what files it reads, what files it writes
- Any open questions the user should resolve before running `/execute-prp`

## IMPORTANT

- **Do not write any implementation code.** Generate the PRP only.
- **Do not invent constraints.** Every rule in the PRP must be traceable to CLAUDE.md, an example file, or the INITIAL.md.
- **Reference real files.** Every path mentioned must actually exist in the repo (or be a path the PRP itself instructs creating).
- **The PRP is reviewed by a human before execution.** Optimize for "a teammate can read this and verify intent in 2 minutes", not "this is exhaustive."
