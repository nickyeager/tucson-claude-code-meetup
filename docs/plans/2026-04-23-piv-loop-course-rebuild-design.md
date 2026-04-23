# PIV Loop Course Rebuild — Design Document

**Date:** 2026-04-23
**Status:** Validated
**Deadline:** 2026-04-25 (Session 1 teaches Saturday)

---

## Overview

Full rebuild of the 4-session Tucson Claude Code Meetup course from the PRP workflow (`INITIAL.md` → `/generate-prp` → `/execute-prp`) to the PIV Loop (Plan / Implement / Validate), aligned with Cole Medin's 2026 workshop methodology and Anthropic's current Best Practices documentation.

### Why

PRP plumbing (custom `/generate-prp`, `/execute-prp`, `PRPs/` folder) is dated. Anthropic and Cole have both moved to a primitive-based workflow (Plan Mode, Skills, subagents, hooks, context reset). The course must teach the current best practice.

### Key Decisions

1. Full rebuild on PIV Loop (not light-touch, not hybrid).
2. Keep 4-session, ~60-min structure. Map PIV onto the existing arc.
3. Scrub PRP entirely. Delete `/generate-prp`, `/execute-prp`, `PRPs/`, `INITIAL.md`. No "legacy comparison" sidebar.
4. MeetupBot domain stays. PIV is workflow, not domain.
5. Context reset between Plan (S2) and Execute (S3) is non-negotiable.
6. RSVP web page is the feature that spans S2→S3, with an agent-browser skill targeting it in S4.

---

## 4-Session Arc

| # | Theme | PIV Phase | Key Activities |
|---|-------|-----------|----------------|
| 1 | Foundation: Context Tier | Pre-PIV setup | `/init`, CLAUDE.md, Plan Mode (Shift+Tab), `/prime` |
| 2 | Plan Phase | P | `/create-prd` → `/plan-feature` → plan in `.agents/plans/` for RSVP feature |
| 3 | Implement + Validate | I+V | Context reset → fresh session → `/execute` → validation pyramid → `/commit` → working RSVP app |
| 4 | Productize: Agents | Beyond loop | `agent-browser` skill against RSVP app, specialist subagents, hooks, System Evolution mindset |

Single feature (RSVP web page) spans S2→S3. Agent built in S4 targets that feature.

---

## Session Details

### Session 1 — Foundation: Context Tier (~60 min)

**Goal:** Context engineering IS the skill. Before you ever ask Claude to write code, you set up the layers that make it effective.

1. **Intro & Why Context Matters (10 min)** — Frame the course: "You're not learning prompts, you're learning to build a system." PIV Loop diagram. Brief MeetupBot orientation.

2. **Exercise 1: `/init` and CLAUDE.md (15 min)** — Clone starter repo, run `/init`, examine generated CLAUDE.md. Walk through each section. Students edit CLAUDE.md (add a project convention) to prove it's not read-only magic.

3. **Exercise 2: Plan Mode & `/prime` (20 min)** — Toggle Plan Mode (Shift+Tab), explore the codebase read-only. Run `/prime` to watch Claude build a mental model. Teaching moment: Plan Mode is scouting — no code written, but Claude maps the territory.

4. **Exercise 3: Context Tiers in Action (10 min)** — Demo showing how CLAUDE.md, `/prime`, and Plan Mode stack. Ask Claude a question with and without CLAUDE.md to see answer quality difference.

5. **Wrap & Preview (5 min)** — "You now have a context-rich workspace. Next session, we plan a real feature."

### Session 2 — Plan Phase (~60 min)

**Goal:** Experience the "P" in PIV. Write a PRD, run `/plan-feature`, produce a detailed implementation plan — zero lines of code written.

1. **Recap & Setup (5 min)** — Review context tiers. Verify workspace intact. Introduce today's feature: RSVP web page for MeetupBot.

2. **Exercise 1: Write the PRD with `/create-prd` (15 min)** — Describe RSVP feature conversationally, use `/create-prd`. PRD is a human artifact — you own the requirements. Review and edit (add a requirement, remove YAGNI).

3. **Exercise 2: `/plan-feature` Deep Dive (25 min)** — Run `/plan-feature` against the PRD. Walk through the 5 phases: user story extraction, codebase intelligence, external research, strategic thinking, plan emission. Plan lands in `.agents/plans/rsvp-feature.md`. Open and read: context references with `file:line`, patterns to follow, step-by-step tasks with IMPLEMENT/PATTERN/VALIDATE fields, validation pyramid, confidence score.

4. **Exercise 3: Evaluate the Plan (10 min)** — Apply the "No Prior Knowledge Test": could someone unfamiliar implement from this plan alone? Identify one gap, ask Claude to revise. Teaching moment: iteration on the plan is cheap, iteration on code is expensive.

5. **Wrap & The Golden Nugget (5 min)** — "Your plan is done. Close this session. Next week: fresh session, execute. The context reset is the point."

### Session 3 — Implement + Validate (~60 min)

**Goal:** Experience the context reset and "I+V" in PIV. Fresh session, plan-driven execution, validate at every level.

1. **The Context Reset (10 min)** — Start a brand new Claude Code session. No chat history from S2. Explain why: the plan must contain everything — if it doesn't, the plan was bad, not the agent. Run `/execute` pointed at `.agents/plans/rsvp-feature.md`.

2. **Exercise 1: Watch `/execute` Work (15 min)** — Observe Claude walking the plan task-by-task. Point out: it reads IMPLEMENT, checks PATTERN for style, runs VALIDATE after each step. Files appear — Express routes, SQLite schema, HTML templates, test files. Key insight: `/execute` is intentionally small and dumb (~2KB). All intelligence was front-loaded into the plan.

3. **Exercise 2: The Validation Pyramid (20 min)** — Walk all 5 levels:
   - Level 1 — Syntax: Does it compile/start? `npm start`, check for errors.
   - Level 2 — Unit tests: Run the test suite generated during execution.
   - Level 3 — Integration: Hit the RSVP endpoint with curl, check the database.
   - Level 4 — Manual: Open the browser, fill out the RSVP form, see the confirmation.
   - Level 5 — CLI sanity: Check routes, review SQLite data, verify email logic.

4. **Exercise 3: `/commit` (5 min)** — Run `/commit` for atomic conventional commits. Review generated messages.

5. **Wrap & Preview (10 min)** — "You have a working RSVP app built entirely through PIV. Next session: we build an agent that uses it."

### Session 4 — Productize: Agents (~60 min)

**Goal:** Go beyond the loop. Build a browser-automation skill, wire up specialist subagents, learn hooks — turn the RSVP app into a system that evolves.

1. **Recap & Frame (5 min)** — "You've used PIV to build a feature. Now you build the tools that make PIV better." Three pillars: Skills, Subagents, Hooks.

2. **Exercise 1: Build an `agent-browser` Skill (20 min)** — Create `.claude/skills/agent-browser.md` that teaches Claude to use Chrome DevTools MCP to interact with the RSVP app. Navigate to RSVP page, fill form with test data, submit, verify confirmation. Teaching moment: a skill is a reusable instruction set — once written, any future session can invoke it.

3. **Exercise 2: Specialist Subagents (15 min)** — Create a subagent in `.claude/agents/` — e.g., `qa-tester.md` that runs the validation pyramid automatically, or `db-auditor.md` that checks SQLite schema integrity. Invoke it, see how subagents scope context and run in isolation. Key insight: subagents are disposable specialists.

4. **Exercise 3: Hooks (10 min)** — Wire up a hook in `settings.json` — e.g., pre-commit linting or post-session summary logging. Show the 26+ event types. Teaching moment: hooks are how the system runs itself.

5. **System Evolution & Wrap (10 min)** — Tie it together: CLAUDE.md is your foundation, skills are your playbook, subagents are your team, hooks are your automation. Each PIV cycle makes the system smarter. "You're not coding with AI — you're building a system that codes." Retrospective, Q&A, next steps.

---

## File-Level Change Map

### REWRITE (existing files, new content)

- `sessions/session-1/SLIDES.md`
- `sessions/session-1/SCRIPT.md`
- `sessions/session-1/EXERCISE.md`
- `sessions/session-2/SLIDES.md`
- `sessions/session-2/SCRIPT.md`
- `sessions/session-2/EXERCISE.md`
- `sessions/session-3/SLIDES.md`
- `sessions/session-3/SCRIPT.md`
- `sessions/session-3/EXERCISE.md`
- `sessions/session-4/SLIDES.md`
- `sessions/session-4/SCRIPT.md`
- `sessions/session-4/EXERCISE.md`
- `sessions/INSTRUCTOR-PREP.md`
- `README.md`
- `STUDENT-GUIDE.md`

### DELETE

- `templates/.claude/commands/generate-prp.md`
- `templates/.claude/commands/execute-prp.md`
- Any `PRPs/` directories or `INITIAL.md` templates

### CREATE (new files)

- `templates/.claude/commands/plan-feature.md` — Cole's plan-feature adapted for MeetupBot
- `templates/.claude/commands/execute.md` — Small/dumb execute command
- `templates/.claude/commands/create-prd.md` — PRD generation command
- `templates/.claude/commands/prime.md` — Codebase priming command
- `templates/.claude/skills/agent-browser.md` — Browser automation skill for RSVP
- `templates/.claude/agents/qa-tester.md` — Validation pyramid subagent
- `solutions/session-1/` — Post-S1 snapshot (CLAUDE.md populated)
- `solutions/session-2/` — Post-S2 snapshot (PRD + plan)
- `solutions/session-3/` — Post-S3 snapshot (working RSVP app)
- `solutions/session-4/` — Post-S4 snapshot (skills, subagents, hooks)

---

## Source Attribution

### From Cole Medin's PIV Loop (`coleam00/ai-coding-summit-workshop-2`)

- `/plan-feature` structure: 5-phase methodology, plan template with IMPLEMENT/PATTERN/VALIDATE fields, confidence score, "No Prior Knowledge Test"
- `/execute` as intentionally small (~2KB)
- Validation pyramid (5 levels)
- Context reset between Plan and Execute as core principle

### From Anthropic Best Practices

- `/init` and CLAUDE.md as foundation
- Plan Mode (Shift+Tab) for exploration
- "Interview → SPEC.md → fresh session" pattern (taught as PRD → plan → context reset)
- Skills as `.claude/skills/` with SKILL.md format
- Subagents as `.claude/agents/`
- Hooks with 26+ event types

### Original to This Course

- MeetupBot domain and RSVP feature as teaching vehicle
- 4-session progressive arc (context → plan → implement → productize)
- `agent-browser` skill targeting student's own RSVP app as S4 capstone
- "System Evolution" as the takeaway mindset

## Runtime Dependencies (RSVP Feature)

- Node.js + Express (web server)
- SQLite via `better-sqlite3` (no DB server needed)
- Basic HTML templates (no React — keeps it simple for 60 min)
- Chrome DevTools MCP for `agent-browser` in S4
