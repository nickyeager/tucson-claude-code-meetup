# Session 2: Context Engineering — Blueprints Beat Prompts

---

## Slide 1

# Building AI Agents with Claude Code

### Session 2: Context Engineering — Blueprints Beat Prompts

*From one-off prompts to reusable systems*

**Nick Yeager** — AI Solutions Architect / nickcyeager.com

Tucson Claude Code Meetup | `github.com/ai-trailblazers/tucson-claude-code-meetup`

---

## Slide 2: Recap — Where We Left Off

You have:
- A git repo with `CLAUDE.md` defining your agent's personality and schemas
- `/plan-event` that generates structured JSON event plans
- An LLM provider connected — Claude Code Max (default), Anthropic API, or ngrok
- Sample venue and speaker data in `data/`

**Today:** You'll build the comms and scheduling system using a **completely different approach**.

---

## Slide 3: Today's Goal

**Session 2 Milestone:**
A pipeline where `/plan-event` feeds into `/build-schedule` and `/draft-announcement`

You'll learn:
- **Context engineering** vs. prompt engineering
- **INITIAL.md** — feature requests that actually work
- **PRPs** — implementation blueprints with validation gates
- **Composable slash commands** that feed into each other
- **The examples/ folder trick** — show, don't describe

---

## Slide 4: The Core Problem

### Why do AI agents fail?

Most agent failures aren't **model** failures.

They're **context** failures.

The AI was smart enough. It just didn't have the right information.

- Wrong output format? It didn't know the schema.
- Missed a constraint? Nobody told it.
- Generic tone? No examples to match against.

**The model isn't the bottleneck. Your context is.**

---

## Slide 5: You've Already Seen This Problem

# You've Already Seen This Problem

### "Design Slop" — what AI output looks like without context

A recent analysis of 500 Show HN sites found **67% used 2+ identical AI design patterns**:

| Pattern | What It Looks Like |
|---|---|
| Inter font, centered hero | Every site has the same headline layout |
| "VibeCode Purple" palette | Same gradient, same dark mode, same grey text |
| shadcn/ui cards with icon tops | Identical feature grids, numbered steps |
| Uppercase badges above headings | `✨ INTRODUCING` on every landing page |
| Glassmorphism + gradient shadows | Same blurry card effect, everywhere |

**These sites aren't bad.** They're just *identical*.

The AI wasn't broken — it had **no examples, no brand, no constraints**. So it fell back to the most common patterns in its training data.

**This is exactly what happens to agent output.**
No context = generic event plans, generic emails, generic schedules.

> Source: Adrian Krebs, ["Design Slop"](https://www.adriankrebs.ch/blog/design-slop/) — scoring AI design markers across Show HN submissions

---

## Slide 6: Prompt Engineering vs. Context Engineering

| | Prompt Engineering | Context Engineering |
|---|---|---|
| **Approach** | Clever wording | Complete system |
| **Analogy** | Sticky note on a desk | Full screenplay with stage directions |
| **What you give** | "Write a good email" | Schema + examples + rules + audience data + tone guide |
| **Strategy** | Hopes the AI guesses right | Gives the AI everything it needs |
| **Failure mode** | "Why didn't it know X?" | "I forgot to include X" |
| **Scalability** | Breaks at complexity | Scales with structure |

**Key insight:** Context engineering makes the problem *your* responsibility, not the model's.

---

## Slide 7: LIVE DEMO — The Difference

**Same task, two approaches:**

**Prompt 1 (prompt engineering):**
```
Write an announcement email for a RAG meetup
```

**Prompt 2 (context engineering):**
```
Read the event plan at events/building-rag-pipelines.json,
read data/speakers.json for speaker bios, and read
examples/sample-event-plan.json for the expected format.

Write an announcement email targeting intermediate Python
developers. Keep it under 200 words, include the date,
venue, and speaker highlights.
```

Watch the quality difference.

---

## Slide 8: The Context Engineering Stack

```
Layer                  Purpose
─────────────────────  ──────────────────────────────────
CLAUDE.md              Always-on rules (personality, schemas, constraints)
examples/              Reference outputs the AI mimics
data/                  Real information to work with
INITIAL.md             Feature spec (what to build)
PRPs/                  Implementation blueprint (how to build it)
.claude/commands/      Reusable workflows (composable tools)
```

Each layer adds context. **More context = better results.**

Think of it as building a briefing packet, not writing a prompt.

---

## Slide 9: INITIAL.md — The Feature Request

A structured feature request with four sections:

```markdown
## FEATURE:
What to build — be specific about inputs, outputs, behavior

## EXAMPLES:
Files to learn from — point to actual files in your repo

## DOCUMENTATION:
APIs, schemas, constraints — the rules it must follow

## OTHER CONSIDERATIONS:
Gotchas, edge cases, integration points — what could go wrong
```

This replaces vague Slack messages with an engineering spec.

> **Template:** See `templates/INITIAL.md` for the blank template and `templates/INITIAL_EXAMPLE.md` for a filled-out example.

---

## Slide 10: Good vs. Bad Feature Requests

**Bad:**
```
Build a scheduling system for meetups
```

**Good:**
```
Build a scheduling system that reads event plan JSON from
/plan-event output, fits talks into time slots using speaker
availability from data/speakers.json, adds breaks every
90 min, and outputs both markdown and JSON.
```

| Bad | Good |
|---|---|
| No data sources | Points to specific files |
| No constraints | Break intervals, availability |
| No output format | Markdown + JSON |
| Ambiguous scope | Reads from, outputs to |

**Specific > Vague. Always.**

---

## Slide 11: PRPs — Implementation Blueprints

**PRP = Product Requirements Prompt**

Like a PRD, but designed for AI coding assistants:

- **Complete context** — everything the AI needs to know, in one file
- **Step-by-step implementation plan** — ordered tasks with dependencies
- **Validation gates** — tests and checks that must pass before moving on
- **Error handling patterns** — what to do when things go wrong

Generated from your INITIAL.md by `/generate-prp`.

> **Note:** `/generate-prp` and `/execute-prp` are custom slash commands, not built-in Claude Code features. Ready-made versions are in `templates/.claude/commands/` — copy them into your project's `.claude/commands/` directory.

You write the WHAT. The PRP figures out the HOW.

---

## Slide 12: The PRP Workflow

```
INITIAL.md  -->  /generate-prp  -->  PRPs/meetup-comms.md  -->  /execute-prp  -->  Working code
    ^                                        ^
    |                                        |
 You write this                   Claude researches your
 (the WHAT)                       codebase and builds this
                                  (the HOW)
```

**The workflow:**
1. You describe the feature in INITIAL.md
2. `/generate-prp` reads your codebase, analyzes patterns, generates a blueprint
3. You review the PRP (catch misunderstandings early!)
4. `/execute-prp` follows the blueprint step by step
5. Working, tested code comes out

---

## Slide 13: LIVE DEMO — /generate-prp

**Run:** `/generate-prp INITIAL.md`

Watch Claude:
1. Read the feature request
2. Analyze existing code (`CLAUDE.md`, commands, data files)
3. Research patterns from `examples/`
4. Generate a comprehensive blueprint

**Open `PRPs/meetup-comms.md` and review:**
- Does it understand the data flow (event plan -> schedule, event plan -> emails)?
- Did it pick up the speaker availability constraint?
- Are there validation steps?
- Did it reference the right files?

---

## Slide 14: LIVE DEMO — /execute-prp

**Run:** `/execute-prp PRPs/meetup-comms.md`

Watch Claude:
1. Read the full PRP
2. Create `.claude/commands/build-schedule.md`
3. Create `.claude/commands/draft-announcement.md`
4. Create `.claude/commands/draft-speaker-outreach.md`
5. Validate against the event plan schema

**Key observation:** Claude isn't guessing. It's following a blueprint you reviewed first.

---

## Slide 15: The Examples/ Folder Trick

**More examples = dramatically better output.**

```
examples/
  sample-event-plan.json     "Make output look like this"
  sample-announcement.md     "Match this tone and format"
  sample-schedule.md         "Follow this structure"
```

The AI pattern-matches against your examples.

- Want a specific JSON schema? Show a sample file.
- Want a particular email tone? Include a real example.
- Want consistent formatting? Provide a template.

**Show it. Don't describe it.**

Remember the design slop sites? They all look the same because the AI had **zero examples** to differentiate against. Your `examples/` folder is the fix.

---

## Slide 16: Composable Slash Commands

Commands that feed into each other:

```
/plan-event "RAG pipelines"
    --> outputs events/rag-pipelines.json

/build-schedule events/rag-pipelines.json
    --> outputs schedules/rag-pipelines.md + .json

/draft-announcement events/rag-pipelines.json
    --> outputs comms/rag-pipelines-announcement.md
```

Each command reads **structured data** from the previous one.

**This is why JSON schemas matter.**
- Predictable format = reliable piping
- Schema in CLAUDE.md = every command knows the contract
- Structured > freeform for agent-to-agent communication

---

## Slide 17: $ARGUMENTS in Slash Commands

```markdown
---
name: build-schedule
description: Build a schedule from an event plan
argument-hint: [event-plan.json]
allowed-tools: Read, Write
---

Build a schedule for the event plan at: $ARGUMENTS

## Steps:
1. Read $ARGUMENTS and data/speakers.json
2. Fit talks into time slots, breaks every 90 min
3. Output markdown + JSON to schedules/
```

**Usage:** `/build-schedule events/rag-pipelines.json`  →  `$ARGUMENTS` becomes `events/rag-pipelines.json`

> **Modern style:** YAML frontmatter (`name`, `description`, `argument-hint`, `allowed-tools`) is the current convention. Plain-markdown commands still work. Skills (`.claude/skills/<name>/SKILL.md`) are the same idea with extra capabilities — Session 3.

---

## Slide 18: Tips & Gotchas

| | Tip |
|---|---|
| Don't | Skip INITIAL.md and go straight to coding |
| **Do** | **Review the PRP before executing — catch misunderstandings early** |
| Don't | Write vague EXAMPLES sections — point to specific files |
| **Do** | **Include OTHER CONSIDERATIONS — that's where edge cases live** |
| Don't | Expect perfection on the first PRP — iterate |
| **Do** | **Add more examples to improve output quality over time** |

**The biggest mistake:** Skipping the review step. A bad PRP executed perfectly still gives you bad code.

---

## Slide 19: BUILD TIME

### Exercise: Build the Comms & Scheduling System via PRP

See `sessions/session-2/EXERCISE.md` for step-by-step instructions.

**Goal:** A pipeline where:
```
/plan-event --> /build-schedule --> /draft-announcement
```

**Steps:**
1. Write your INITIAL.md (15 min)
2. Run `/generate-prp` and review (10 min)
3. Run `/execute-prp` and test (15 min)

**Time:** ~40 minutes

Raise your hand if you get stuck on INITIAL.md — that's the hardest part.

---

## Slide 20: Checkpoint

You should have:

- INITIAL.md with complete feature request
- Generated PRP in `PRPs/`
- `/build-schedule` command working
- `/draft-announcement` command working
- `/draft-speaker-outreach` command working
- All commands consuming JSON from previous steps

**Quick test:** Run the full pipeline end-to-end:
```
/plan-event "Your Topic" --> /build-schedule --> /draft-announcement
```

---

## Slide 21: What's Next — Session 3

### Subagents & Hooks: Specialists Beat Generalists

Right now, one agent does everything. Next session:

- **Subagents** — split into specialists (schedule optimizer, comms reviewer, quality checker)
- **Hooks** — automate quality checks that run on every command
- **The difference** between one person doing everything and a team of experts

*Your MeetupBot will go from a solo performer to a coordinated team.*

---

## Slide 22: Session 2 Recap

### Three things to remember:

1. **Context engineering > prompt engineering**
   Complete blueprints beat clever wording. Give the AI everything it needs.

2. **INITIAL.md -> PRP -> Execute**
   Describe WHAT you want, generate HOW to build it, execute automatically.

3. **Composable commands via structured JSON**
   JSON schemas enable data flow between agent capabilities. Structure scales.

