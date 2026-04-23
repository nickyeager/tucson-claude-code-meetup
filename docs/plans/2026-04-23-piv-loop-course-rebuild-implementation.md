# PIV Loop Course Rebuild — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite the entire 4-session Tucson Claude Code Meetup course from PRP workflow to PIV Loop (Plan/Implement/Validate).

**Architecture:** Content-only rewrite. ~30 markdown files across sessions, templates, solutions, and supporting docs. No application code — the RSVP app is built by students during the course, not pre-built by us.

**Tech Stack:** Markdown files, Claude Code commands/skills/agents (`.claude/` directory structure).

**Design doc:** `docs/plans/2026-04-23-piv-loop-course-rebuild-design.md`

**Source material on disk:**
- PIV commands: `~/.claude/commands/core_piv_loop/{plan-feature,execute,prime}.md`
- Existing course: `/private/tmp/tucson-meetup/sessions/`, `templates/`, `solution/`

---

## Batch Strategy

Tasks are grouped into 5 batches. Within each batch, tasks are independent and can run in parallel via subagents.

- **Batch 1:** Delete old PRP files (3 tasks)
- **Batch 2:** Create new template commands, skills, agents (6 tasks)
- **Batch 3:** Rewrite all 4 sessions — SLIDES, SCRIPT, EXERCISE (12 tasks, 4 parallel groups of 3)
- **Batch 4:** Rewrite supporting files (3 tasks)
- **Batch 5:** Rewrite solution snapshots (4 tasks)

**Review checkpoint** after each batch before proceeding.

---

## BATCH 1: Delete Old PRP Files

### Task 1: DELETE `templates/.claude/commands/generate-prp.md`

**Files:**
- Delete: `templates/.claude/commands/generate-prp.md`

**Step 1:** Delete the file.
```bash
rm templates/.claude/commands/generate-prp.md
```

**Step 2:** Verify it's gone.
```bash
ls templates/.claude/commands/  # Should NOT list generate-prp.md
```

### Task 2: DELETE `templates/.claude/commands/execute-prp.md`

**Files:**
- Delete: `templates/.claude/commands/execute-prp.md`

**Step 1:** Delete the file.
```bash
rm templates/.claude/commands/execute-prp.md
```

### Task 3: DELETE old PRP templates and INITIAL.md

**Files:**
- Delete: `templates/PRPs/` directory (contains `templates/prp_base.md`)
- Delete: `templates/INITIAL.md`
- Delete: `templates/INITIAL_EXAMPLE.md`

**Step 1:** Delete all PRP-related template files.
```bash
rm -rf templates/PRPs/
rm -f templates/INITIAL.md templates/INITIAL_EXAMPLE.md
```

**Step 2:** Verify templates directory is clean.
```bash
ls templates/  # Should show: CLAUDE-starter.md, CLAUDE.md, .claude/
```

**Step 3:** Commit batch 1.
```bash
git add -A && git commit -m "chore: remove old PRP templates (generate-prp, execute-prp, INITIAL.md, PRPs/)"
```

---

## BATCH 2: Create New Template Commands, Skills, and Agents

These are the files students will copy into their projects. Adapt from Cole Medin's PIV source files but scope to MeetupBot/RSVP domain.

### Task 4: CREATE `templates/.claude/commands/prime.md`

**Files:**
- Create: `templates/.claude/commands/prime.md`
- Source: `~/.claude/commands/core_piv_loop/prime.md` (adapt for MeetupBot)

**Content:** Adapted version of Cole's prime command. Keep the same structure (analyze project structure, read core docs, identify key files, understand current state, output report) but add MeetupBot-specific hints:
- Look for `data/` directory with venue/speaker JSON
- Look for `CLAUDE.md` conventions
- Note any existing commands in `.claude/commands/`

Keep it generic enough that it works on any project (students will use it beyond this course), but include a comment at the top saying it was adapted from Cole Medin's PIV workflow.

### Task 5: CREATE `templates/.claude/commands/create-prd.md`

**Files:**
- Create: `templates/.claude/commands/create-prd.md`

**Content:** A command that interviews the user about a feature and produces a structured PRD. Structure:

```markdown
---
description: "Create a Product Requirements Document through collaborative interview"
---

# Create PRD

## Feature: $ARGUMENTS

## Process

### Step 1: Interview
Ask the user these questions ONE AT A TIME:
1. What problem does this feature solve?
2. Who is the primary user?
3. What does success look like? (measurable criteria)
4. What are the constraints? (time, tech stack, dependencies)
5. What is explicitly OUT of scope?

### Step 2: Generate PRD
Write a structured PRD to `docs/prd/{kebab-case-name}.md` with sections:
- Problem Statement
- User Story (As a... I want... So that...)
- Requirements (numbered, testable)
- Out of Scope
- Success Criteria
- Technical Constraints

### Step 3: Review
Present the PRD to the user. Ask: "Does this capture what you want to build? Any requirements to add or remove?"

Iterate until the user confirms.
```

### Task 6: CREATE `templates/.claude/commands/plan-feature.md`

**Files:**
- Create: `templates/.claude/commands/plan-feature.md`
- Source: `~/.claude/commands/core_piv_loop/plan-feature.md` (adapt for teaching)

**Content:** This is the crown jewel — Cole's full plan-feature command adapted for the course. Keep ALL 5 phases:
1. Feature Understanding (extract user story)
2. Codebase Intelligence Gathering (project structure, pattern recognition, dependencies, testing patterns, integration points)
3. External Research & Documentation
4. Deep Strategic Thinking
5. Plan Structure Generation

Keep the full plan template output with:
- Context References (with `file:line`)
- Patterns to Follow (with code snippets)
- Step-by-Step Tasks with IMPLEMENT/PATTERN/IMPORTS/GOTCHA/VALIDATE fields
- Validation Pyramid (5 levels: Syntax, Unit, Integration, Manual, CLI)
- Acceptance Criteria
- Confidence Score #/10

Output to `.agents/plans/{kebab-case-name}.md`.

Add a teaching comment at the top: "Adapted from Cole Medin's PIV Loop (github.com/coleam00/ai-coding-summit-workshop-2). This command does NOT write code — it creates a context-rich plan for one-pass implementation."

Keep it close to the original (~12KB). Don't simplify — the complexity IS the teaching point.

### Task 7: CREATE `templates/.claude/commands/execute.md`

**Files:**
- Create: `templates/.claude/commands/execute.md`
- Source: `~/.claude/commands/core_piv_loop/execute.md` (adapt for teaching)

**Content:** Cole's execute command, kept intentionally small (~2KB). This is the counterpoint to plan-feature — all intelligence is in the plan, execute is just a task walker.

Add a teaching comment: "This command is intentionally simple. If execution fails, the fix belongs in the plan, not here."

Keep the same structure: Read plan → Execute tasks in order → Implement testing → Run validation → Final verification → Output report.

### Task 8: CREATE `templates/.claude/skills/agent-browser.md`

**Files:**
- Create directory: `templates/.claude/skills/`
- Create: `templates/.claude/skills/agent-browser.md`

**Content:** A SKILL.md that teaches Claude how to use Chrome DevTools MCP to test a web application. Scoped to the RSVP feature but written generically enough to adapt.

```markdown
---
name: agent-browser
description: "Test web applications using Chrome DevTools MCP — navigate, fill forms, verify content"
---

# Browser Testing Skill

## When to Use
When you need to interact with a web application in the browser — filling forms, clicking buttons, verifying page content, checking for errors.

## Prerequisites
- Chrome DevTools MCP server running
- Target application running locally (default: http://localhost:3000)

## Process

### 1. Navigate
Use the Chrome DevTools MCP to navigate to the target URL.

### 2. Inspect
Take a screenshot or snapshot of the page to understand the current state.

### 3. Interact
Fill form fields, click buttons, submit forms using the MCP tools.

### 4. Verify
After each interaction:
- Take a screenshot to confirm visual state
- Check console for errors
- Verify expected content appears on the page

## Example: Testing an RSVP Form
1. Navigate to http://localhost:3000/rsvp
2. Fill in: name, email, number of guests
3. Click submit
4. Verify: confirmation message appears
5. Navigate to http://localhost:3000/attendees
6. Verify: new attendee appears in the list

## Error Handling
- If page doesn't load: check that the server is running
- If form submission fails: check console for error messages
- If element not found: take a screenshot to see actual page state
```

### Task 9: CREATE `templates/.claude/agents/qa-tester.md`

**Files:**
- Create directory: `templates/.claude/agents/`
- Create: `templates/.claude/agents/qa-tester.md`

**Content:** A specialist subagent that runs the validation pyramid automatically.

```markdown
---
name: qa-tester
description: "Run the 5-level validation pyramid against the current project"
---

# QA Tester Agent

You are a QA specialist. Run the validation pyramid and report results.

## Validation Pyramid

### Level 1: Syntax
- Run the project's start command to check for compilation errors
- Check for syntax errors in all source files

### Level 2: Unit Tests
- Find and run the test suite
- Report pass/fail counts and any failures

### Level 3: Integration Tests
- If integration tests exist, run them
- If not, test key API endpoints with curl

### Level 4: Manual Validation
- If agent-browser skill is available, use it to test the UI
- Otherwise, list the manual testing steps needed

### Level 5: CLI Sanity
- Check database state if applicable
- Verify file structure matches expectations
- Check for common issues (missing env vars, wrong ports, etc.)

## Output
Report results as a table:
| Level | Status | Details |
|-------|--------|---------|
| 1. Syntax | PASS/FAIL | ... |
| 2. Unit Tests | PASS/FAIL | ... |
| 3. Integration | PASS/FAIL | ... |
| 4. Manual | PASS/FAIL/SKIPPED | ... |
| 5. CLI Sanity | PASS/FAIL | ... |
```

**Step (after all Batch 2 tasks):** Commit.
```bash
git add -A && git commit -m "feat: add PIV Loop template commands, skills, and agents

Replaces PRP workflow with:
- /prime — codebase understanding
- /create-prd — collaborative PRD generation
- /plan-feature — comprehensive implementation planning (adapted from Cole Medin)
- /execute — plan-driven task execution
- agent-browser skill — Chrome DevTools MCP testing
- qa-tester agent — automated validation pyramid"
```

---

## BATCH 3: Rewrite All Session Files

Each session has 3 files (SLIDES.md, SCRIPT.md, EXERCISE.md). All 4 sessions can be written in parallel — they reference the design doc for content.

**Format conventions** (preserved from existing files):
- **SLIDES.md:** `## Slide N: Title` sections separated by `---`. Markdown-only, presenter-ready.
- **SCRIPT.md:** Matches slide numbers. Each section has `**Time: N min**`, quoted talk track in `"..."`, `[PAUSE]` and `**Transition:**` cues.
- **EXERCISE.md:** Numbered steps with code blocks. Goal at top. Checkpoints inline.

### Task 10: REWRITE `sessions/session-1/SLIDES.md`

**Files:**
- Rewrite: `sessions/session-1/SLIDES.md`

**Content from design doc — Session 1: Foundation: Context Tier:**

Slides to cover:
1. Title slide: "Building AI Agents with Claude Code / Session 1: Foundation — Context Engineering / Tucson Claude Code Meetup"
2. What We're Building: MeetupBot overview (same domain, but frame through PIV — "4 sessions, one system that evolves")
3. Why Context Engineering: "Context > Prompts. The quality of what Claude builds depends on the context you set up BEFORE you ask it to build."
4. The PIV Loop: Diagram slide — Plan / Implement / Validate. "Today we set up the foundation that makes PIV work."
5. Today's Goal: "By the end of tonight: CLAUDE.md configured, Plan Mode explored, codebase primed. No code written — and that's the point."
6. CLAUDE.md Deep Dive: What it is, what goes in it, why it matters. Show the tiers: project root, `.claude/` directory, user-level.
7. Exercise 1 intro: `/init` and CLAUDE.md
8. Plan Mode: What it does (Shift+Tab), why it exists (scout before you build), what it prevents (premature coding)
9. `/prime`: What it does (builds a mental model), when to use it (start of session, new codebase)
10. Exercise 2 intro: Plan Mode + `/prime`
11. Context Tiers: How CLAUDE.md + `/prime` + Plan Mode stack. The "with vs without" demo.
12. Exercise 3 intro: Context tiers in action
13. Recap + Preview: "You built the foundation. Next session: we use it to plan a real feature."

### Task 11: REWRITE `sessions/session-1/SCRIPT.md`

**Files:**
- Rewrite: `sessions/session-1/SCRIPT.md`

**Content:** Instructor talk track matching the slides above. Follow existing format:
- `## Slide N: Title` with `**Time: N min**`
- Quoted talk track
- `[PAUSE]`, `[DEMO]`, `**Transition:**` cues
- Total: ~25 min instruction, ~30 min exercises, ~5 min wrap

Key talk track beats:
- "You're not learning prompts, you're learning to build a system."
- Show of hands: who's used AI coding tools? Claude Code specifically?
- Explain PIV Loop briefly — we'll go deep in S2-S3, today is the foundation
- CLAUDE.md is not magic — it's a file you edit. Show editing it.
- Plan Mode: "This is how you scout. Notice Claude reads but doesn't write."
- `/prime`: "Watch Claude build a mental model. This is what context engineering looks like."
- Context tiers demo: Ask same question with and without CLAUDE.md. See the difference.
- Close: "We wrote zero code tonight. And that's exactly right. Next session, we plan a real feature."

### Task 12: REWRITE `sessions/session-1/EXERCISE.md`

**Files:**
- Rewrite: `sessions/session-1/EXERCISE.md`

**Content:** Three exercises matching the design doc.

**Exercise 1: `/init` and CLAUDE.md (15 min)**
- Clone starter repo (or `mkdir meetup-agent && cd meetup-agent && git init`)
- Launch Claude Code: `claude`
- Run `/init` — watch it generate CLAUDE.md
- Open CLAUDE.md, read through sections
- Edit CLAUDE.md: add a project convention (e.g., "All event data must be structured JSON")
- Checkpoint: CLAUDE.md exists and has your custom convention

**Exercise 2: Plan Mode & `/prime` (20 min)**
- Toggle Plan Mode: Shift+Tab (or type `plan` in the prompt)
- Ask Claude: "What files are in this project and what do they do?"
- Observe: Claude reads files but writes nothing
- Exit Plan Mode: Shift+Tab again
- Run `/prime` (copy from `templates/.claude/commands/prime.md` first)
- Read the output report — note how Claude mapped the project
- Checkpoint: You can explain what Plan Mode does and why `/prime` matters

**Exercise 3: Context Tiers in Action (10 min)**
- In a fresh session (or after clearing context), ask: "How should I structure a new meetup event?"
- Note the generic answer
- Now with CLAUDE.md loaded, ask the same question
- Compare: the answer should reference your JSON schema convention, MeetupBot context
- Checkpoint: You see a measurable difference in answer quality

### Task 13: REWRITE `sessions/session-2/SLIDES.md`

**Files:**
- Rewrite: `sessions/session-2/SLIDES.md`

**Content from design doc — Session 2: Plan Phase:**

Slides:
1. Title: "Session 2: The Plan Phase / Writing Plans That Agents Can Execute"
2. Recap: Context tiers from S1. Quick check: everyone's CLAUDE.md intact?
3. Today's Feature: "We're building an RSVP web page for MeetupBot. Express + SQLite + HTML."
4. The PIV Loop — Plan Phase: "Today is ALL planning. No code. The plan must be so good that a fresh agent with zero history can execute it."
5. PRDs: What they are, why they matter. "You own the requirements, not Claude."
6. `/create-prd`: How the command works. Interview → structured output.
7. Exercise 1 intro: Write the PRD
8. `/plan-feature` Overview: The 5 phases. "This is the crown jewel of PIV."
9. Phase 1-2: Feature Understanding + Codebase Intelligence
10. Phase 3-4: External Research + Strategic Thinking
11. Phase 5: Plan Structure — show the template (IMPLEMENT/PATTERN/VALIDATE fields)
12. Exercise 2 intro: Run `/plan-feature`
13. The "No Prior Knowledge Test": Could someone unfamiliar implement from this plan alone?
14. Exercise 3 intro: Evaluate the plan
15. The Golden Nugget: "Close this session. The context reset is the point."

### Task 14: REWRITE `sessions/session-2/SCRIPT.md`

**Files:**
- Rewrite: `sessions/session-2/SCRIPT.md`

**Content:** Talk track for S2 slides. Key beats:
- Recap S1 briefly — "Last session we built the foundation. Today we use it."
- Introduce RSVP feature — show what the finished product will look like (screenshot or description)
- PRD exercise: "Describe the feature in your own words. Claude interviews you and structures it."
- `/plan-feature` is the centerpiece — let it run, then pause to walk through the output
- Point out specific plan elements: context references with `file:line`, validation commands, confidence score
- "No Prior Knowledge Test" — have students actually evaluate their plan against this criterion
- Close with the golden nugget: "Now close your session. I mean it. Close it. The plan must stand alone."

### Task 15: REWRITE `sessions/session-2/EXERCISE.md`

**Files:**
- Rewrite: `sessions/session-2/EXERCISE.md`

**Content:** Three exercises.

**Exercise 1: Write the PRD with `/create-prd` (15 min)**
- Copy `templates/.claude/commands/create-prd.md` to your project's `.claude/commands/`
- Run `/create-prd "RSVP web page for meetup events"`
- Answer Claude's interview questions about the feature
- Review the generated PRD in `docs/prd/rsvp-web-page.md`
- Edit: add one requirement, remove one YAGNI item
- Checkpoint: PRD exists with your edits

**Exercise 2: `/plan-feature` Deep Dive (25 min)**
- Copy `templates/.claude/commands/plan-feature.md` to `.claude/commands/`
- Run `/plan-feature "RSVP web page"` (or pass the PRD path)
- Watch the 5 phases execute (instructor will pause to explain each)
- Find the generated plan in `.agents/plans/rsvp-web-page.md`
- Open and read through: context references, patterns, tasks with IMPLEMENT/VALIDATE fields
- Note the confidence score
- Checkpoint: Plan file exists in `.agents/plans/`

**Exercise 3: Evaluate the Plan (10 min)**
- Apply the "No Prior Knowledge Test": read the plan as if you'd never seen this codebase
- Identify one gap (missing dependency? unclear step? missing validation?)
- Ask Claude to revise that section of the plan
- Checkpoint: Plan has been refined based on your feedback

**End of Session:** Close your Claude Code session. Do NOT continue. The context reset happens next session.

### Task 16: REWRITE `sessions/session-3/SLIDES.md`

**Files:**
- Rewrite: `sessions/session-3/SLIDES.md`

**Content from design doc — Session 3: Implement + Validate:**

Slides:
1. Title: "Session 3: Implement + Validate / Context Reset → Execution → Validation"
2. The Context Reset: "Start a fresh session. No history from last week. This is non-negotiable."
3. Why Context Reset Works: The plan contains everything. If it doesn't, the plan was bad.
4. `/execute`: How it works. "Intentionally small and dumb. All intelligence is in the plan."
5. Exercise 1 intro: Watch `/execute` work
6. The Validation Pyramid: 5 levels diagram
7. Level 1-2: Syntax + Unit Tests
8. Level 3-4: Integration + Manual
9. Level 5: CLI Sanity
10. Exercise 2 intro: Walk the pyramid
11. `/commit`: Atomic conventional commits. "The loop closes here."
12. Exercise 3 intro: Commit your work
13. Recap: "You built a working RSVP app. Zero cleverness — just a good plan executed faithfully."
14. Preview S4: "Next session: we build an agent that uses what you built."

### Task 17: REWRITE `sessions/session-3/SCRIPT.md`

**Files:**
- Rewrite: `sessions/session-3/SCRIPT.md`

**Content:** Talk track for S3. Key beats:
- Open with the drama: "Everyone, start a new Claude Code session. Fresh. No history."
- Explain why this feels uncomfortable and why it works
- `/execute` demo: point out Claude reading IMPLEMENT fields, checking PATTERN, running VALIDATE
- Pause during execution to narrate what's happening
- Validation pyramid: walk each level live. Start server, run tests, curl endpoints, open browser
- Level 4 is the payoff — students see their RSVP form in the browser
- `/commit` is quick — show the generated commit messages
- Close: "You didn't write this code. An agent did, from a plan you wrote. That's PIV."

### Task 18: REWRITE `sessions/session-3/EXERCISE.md`

**Files:**
- Rewrite: `sessions/session-3/EXERCISE.md`

**Content:** Three exercises.

**Exercise 1: Context Reset + `/execute` (15 min)**
- Start a brand new Claude Code session: `claude` (fresh terminal, no history)
- Copy `templates/.claude/commands/execute.md` to `.claude/commands/` if not already there
- Run `/execute .agents/plans/rsvp-web-page.md`
- Watch Claude walk the plan task by task
- Observe: files being created (routes, schema, templates, tests)
- Do NOT interrupt — let it complete
- Checkpoint: New files exist in your project (check with `ls`)

**Exercise 2: The Validation Pyramid (20 min)**
- Level 1 — Syntax: `npm start` — does the server start without errors?
- Level 2 — Unit Tests: `npm test` — do the generated tests pass?
- Level 3 — Integration: `curl http://localhost:3000/rsvp` — does the endpoint respond?
- Level 4 — Manual: Open `http://localhost:3000/rsvp` in your browser. Fill out the form. Submit. See the confirmation.
- Level 5 — CLI Sanity: Check the SQLite database (`sqlite3 meetup.db "SELECT * FROM attendees"`), verify the data.
- If any level fails: fix with Claude's help, then re-validate from that level up.
- Checkpoint: All 5 levels pass

**Exercise 3: `/commit` (5 min)**
- Run `/commit`
- Review the generated commit message — is it accurate?
- Checkpoint: Clean git status, meaningful commit message

### Task 19: REWRITE `sessions/session-4/SLIDES.md`

**Files:**
- Rewrite: `sessions/session-4/SLIDES.md`

**Content from design doc — Session 4: Productize: Agents:**

Slides:
1. Title: "Session 4: Productize / Skills, Subagents, and System Evolution"
2. Recap the journey: Context (S1) → Plan (S2) → Implement+Validate (S3) → Now what?
3. Beyond the Loop: "You've used PIV. Now you build the tools that make PIV better."
4. Three Pillars: Skills, Subagents, Hooks
5. Skills: What they are (`.claude/skills/SKILL.md`), reusable instruction sets, progressive disclosure
6. `agent-browser` Skill: Browser automation via Chrome DevTools MCP
7. Exercise 1 intro: Build the skill
8. Subagents: What they are (`.claude/agents/`), disposable specialists, scoped context
9. Exercise 2 intro: Build a specialist subagent
10. Hooks: What they are (`settings.json`), automation triggers, 26+ event types
11. Exercise 3 intro: Wire up a hook
12. System Evolution: CLAUDE.md (foundation) + Skills (playbook) + Subagents (team) + Hooks (automation) = a system that gets smarter with each PIV cycle
13. Course Retrospective: What you built, what transfers to any project
14. Next Steps: Resources, community, advanced topics

### Task 20: REWRITE `sessions/session-4/SCRIPT.md`

**Files:**
- Rewrite: `sessions/session-4/SCRIPT.md`

**Content:** Talk track for S4. Key beats:
- Recap the full journey — "4 weeks ago you typed `/init`. Now you have a working app."
- Frame S4: "Today you stop being a user of PIV and start being a builder of systems."
- Skills: "A skill is a reusable instruction set. Write it once, invoke it forever."
- Agent-browser demo: Watch Claude drive the browser against the RSVP app
- Subagents: "Think of them as disposable specialists. Narrow context, single job."
- Hooks: "This is how the system runs itself. Pre-commit linting, post-session logging."
- System Evolution tie-together: each primitive (CLAUDE.md, skills, subagents, hooks) makes the next PIV cycle better
- Close: "You're not coding with AI. You're building a system that codes."
- Q&A, next steps, community resources

### Task 21: REWRITE `sessions/session-4/EXERCISE.md`

**Files:**
- Rewrite: `sessions/session-4/EXERCISE.md`

**Content:** Three exercises.

**Exercise 1: Build an `agent-browser` Skill (20 min)**
- Create directory: `mkdir -p .claude/skills`
- Copy `templates/.claude/skills/agent-browser.md` to `.claude/skills/`
- Read through the skill — understand each section
- Start your RSVP app: `npm start`
- Ask Claude: "Use the agent-browser skill to test the RSVP form"
- Watch Claude navigate to the RSVP page, fill the form, submit, verify
- If Chrome DevTools MCP is not available: instructor demos, students follow along
- Checkpoint: Claude successfully tested the RSVP form via browser

**Exercise 2: Specialist Subagents (15 min)**
- Create directory: `mkdir -p .claude/agents`
- Copy `templates/.claude/agents/qa-tester.md` to `.claude/agents/`
- Read the agent file — note the validation pyramid structure
- Invoke: Ask Claude to "run the qa-tester agent against the project"
- Observe: Claude spawns a subagent with scoped context
- Read the output report — validation pyramid results in table format
- Checkpoint: QA tester subagent ran and produced a report

**Exercise 3: Hooks (10 min)**
- Open `.claude/settings.json` (create if needed)
- Add a pre-commit hook that runs linting:
```json
{
  "hooks": {
    "pre-commit": {
      "command": "npm run lint --if-present"
    }
  }
}
```
- Make a small change to a file and commit — observe the hook running
- Instructor shows the list of 26+ event types
- Checkpoint: Hook fires on commit

**Wrap-up: System Evolution (10 min)**
- Review your `.claude/` directory — commands, skills, agents, hooks
- Discuss: "Every PIV cycle, you can add a new skill, refine a command, or wire a hook. The system evolves."
- Course retrospective and Q&A

---

## BATCH 4: Rewrite Supporting Files

### Task 22: REWRITE `sessions/INSTRUCTOR-PREP.md`

**Files:**
- Rewrite: `sessions/INSTRUCTOR-PREP.md`

**Content:** Updated for PIV workflow. Sections:

1. **Pre-Teaching Checklist:**
   - Environment: Node.js 18+, Git, Claude Code installed, API key or ngrok
   - Repo: Clone course repo, verify templates (`.claude/commands/` has prime, create-prd, plan-feature, execute), verify skills and agents templates
   - Chrome DevTools MCP: Verify Chrome MCP server works (needed for S4)
   - Terminal: readable font size for projection

2. **Dry Run Protocol (~4-5 hours):**
   - S1 dry run: `/init`, CLAUDE.md, Plan Mode, `/prime` — verify each exercise works
   - S2 dry run: `/create-prd` for RSVP feature, `/plan-feature`, evaluate plan — verify plan lands in `.agents/plans/`
   - S3 dry run: Fresh session, `/execute` the plan, run validation pyramid — verify RSVP app works end-to-end
   - S4 dry run: Agent-browser skill, qa-tester subagent, hook wiring — verify Chrome MCP integration

3. **Common Issues:**
   - `/init` generates different CLAUDE.md depending on Claude Code version — that's fine, it's a starting point
   - `/plan-feature` may take 2-5 minutes — warn students, use the time to explain what's happening
   - Context reset: students WILL try to continue in the same session. Be firm.
   - Chrome DevTools MCP may not work on all machines — have a fallback demo ready

4. **Timing guide per session** (table format matching existing)

### Task 23: REWRITE `README.md`

**Files:**
- Rewrite: `README.md`

**Content:** Course overview rewritten for PIV. Keep the same top-level structure but update all content:

- Title and intro: Same "MeetupBot" framing but mention PIV Loop instead of PRP
- Prerequisites: Keep bootcamp requirements section (GitHub, AI-Trailblazers, consent, Claude Code account). Keep technical setup. Remove ngrok AI Gateway as requirement (make it optional).
- Quick Start: Same `npm install -g @anthropic-ai/claude-code` flow
- Course Structure table: Updated for new session themes (Foundation/Plan/Implement+Validate/Productize)
- Session Folders: Same structure description
- Sample Data: Keep as-is
- Solution/Reference: Update tree to show new structure (`.agents/plans/`, `.claude/skills/`, `.claude/agents/` instead of `PRPs/`, `INITIAL.md`)
- What You'll Learn table: Replace PRP entries with PIV entries (Plan Mode, `/prime`, PRDs, `/plan-feature`, context reset, `/execute`, validation pyramid, skills, subagents, hooks)
- Course Progression: Rewrite S1→S2→S3→S4 narrative for PIV
- Attribution: Update Cole Medin attribution to reference PIV Loop and `ai-coding-summit-workshop-2` repo. Keep Luong Nguyen attribution.
- Resources: Update links, add Anthropic Best Practices doc, Cole's PIV workshop repo

Remove all references to: PRP, `/generate-prp`, `/execute-prp`, `INITIAL.md`, `PRPs/` directory.

### Task 24: REWRITE `STUDENT-GUIDE.md`

**Files:**
- Check if exists: `STUDENT-GUIDE.md` at project root
- If not at root, check `class/README.md` or `sessions/SETUP-GUIDE.md`

**Content:** Updated student-facing guide. Remove all PRP references. Add:
- What is PIV Loop (1 paragraph)
- What you'll need installed
- How each session builds on the last (PIV framing)
- Where to find help (resources, community)

**Step (after Batch 4):** Commit.
```bash
git add -A && git commit -m "docs: rewrite course materials for PIV Loop workflow

- Updated INSTRUCTOR-PREP.md for PIV dry run protocol
- Rewrote README.md: PIV Loop framing, updated attribution
- Updated student guide with PIV overview"
```

---

## BATCH 5: Rewrite Solution Snapshots

Each solution snapshot shows what the student's project should look like after completing that session. Delete old PRP-based solutions and create new PIV-based ones.

### Task 25: REWRITE `solution/session-1/`

**Files:**
- Clear and recreate: `solution/session-1/`

**Content:** Post-S1 snapshot:
```
solution/session-1/
├── CLAUDE.md            # Generated by /init + student's custom convention added
├── README.md            # Basic MeetupBot readme
└── data/
    ├── venues.json      # Keep existing sample data
    ├── speakers.json    # Keep existing sample data
    └── sample-event-plan.json  # Keep existing
```

No `.claude/commands/` yet — those come in S2. The CLAUDE.md should look like a realistic `/init` output with one custom convention added.

### Task 26: REWRITE `solution/session-2/`

**Files:**
- Clear and recreate: `solution/session-2/`

**Content:** Post-S2 snapshot (everything from S1 plus):
```
solution/session-2/
├── CLAUDE.md
├── README.md
├── data/                        # Same as S1
├── .claude/
│   └── commands/
│       ├── prime.md             # Copied from templates
│       ├── create-prd.md        # Copied from templates
│       └── plan-feature.md      # Copied from templates
├── docs/
│   └── prd/
│       └── rsvp-web-page.md     # Generated PRD for RSVP feature
└── .agents/
    └── plans/
        └── rsvp-web-page.md     # Generated plan (realistic example)
```

The PRD and plan files should be realistic examples of what `/create-prd` and `/plan-feature` would produce for the RSVP feature. The plan should follow Cole's template exactly — with context references, IMPLEMENT/PATTERN/VALIDATE fields, validation pyramid, confidence score.

### Task 27: REWRITE `solution/session-3/`

**Files:**
- Clear and recreate: `solution/session-3/`

**Content:** Post-S3 snapshot (everything from S2 plus the executed RSVP app):
```
solution/session-3/
├── CLAUDE.md
├── README.md
├── package.json                 # Express + better-sqlite3 + test deps
├── data/                        # Same as S1
├── .claude/commands/            # Same as S2
├── docs/prd/                    # Same as S2
├── .agents/plans/               # Same as S2
├── src/
│   ├── index.js                 # Express server entry point
│   ├── routes/
│   │   └── rsvp.js              # RSVP routes (GET form, POST submit, GET attendees)
│   ├── db/
│   │   └── schema.js            # SQLite schema + init
│   └── views/
│       ├── rsvp-form.html       # RSVP form page
│       ├── confirmation.html    # Submission confirmation
│       └── attendees.html       # Attendee list
├── tests/
│   ├── rsvp.test.js             # Unit tests for RSVP routes
│   └── db.test.js               # Database tests
└── meetup.db                    # SQLite database (can be .gitignored)
```

This is the most complex solution — it's a working Express app. Write realistic but simple code. No React, no complex bundling. Plain HTML templates served by Express. SQLite via `better-sqlite3`. Tests via a simple test runner (jest or vitest).

### Task 28: REWRITE `solution/session-4/`

**Files:**
- Clear and recreate: `solution/session-4/`

**Content:** Post-S4 snapshot (everything from S3 plus skills, agents, hooks):
```
solution/session-4/
├── (everything from session-3)
├── .claude/
│   ├── commands/                # Same as S2
│   ├── skills/
│   │   └── agent-browser.md     # Browser testing skill
│   ├── agents/
│   │   └── qa-tester.md         # QA validation subagent
│   └── settings.json            # Hooks configuration
```

The `settings.json` should show the pre-commit hook from Exercise 3.

**Step (after Batch 5):** Commit.
```bash
git add -A && git commit -m "feat: add PIV-based solution snapshots for all 4 sessions

- S1: CLAUDE.md + data files (foundation)
- S2: PIV commands + PRD + plan (plan phase)
- S3: Working RSVP Express app (implement + validate)
- S4: Skills, subagents, hooks (productize)"
```

---

## VALIDATION

After all batches complete:

1. **PRP scrub check:** `grep -r "PRP\|generate-prp\|execute-prp\|INITIAL\.md" sessions/ templates/ solution/ README.md` — should return zero results
2. **PIV presence check:** `grep -r "PIV\|plan-feature\|execute\|validation pyramid" sessions/` — should return results in all 4 sessions
3. **File count:** Verify all expected files exist
4. **Dry run:** Walk through S1 exercise steps mentally to verify they make sense
5. **Solution consistency:** Each solution snapshot builds on the previous one

---

## COMPLETION CHECKLIST

- [ ] Batch 1: Old PRP files deleted
- [ ] Batch 2: New template commands, skills, agents created
- [ ] Batch 3: All 12 session files rewritten (4 sessions × 3 files)
- [ ] Batch 4: INSTRUCTOR-PREP, README, STUDENT-GUIDE rewritten
- [ ] Batch 5: All 4 solution snapshots rewritten
- [ ] Validation: PRP scrub clean, PIV present, files exist
- [ ] Final commit and clean git status
