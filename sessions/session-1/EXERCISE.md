# Session 1 Exercise: Set Up Your MeetupBot + Event Planning

## Goal
Create a new repo from scratch, set up Claude Code with a CLAUDE.md, connect to ngrok AI Gateway, and build your first slash command that generates structured event plans.

## Step 1: Install & Authenticate (10 min)

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Create your project from scratch
mkdir meetup-agent && cd meetup-agent

# Initialize a git repo
git init

# Create a README
echo "# MeetupBot" > README.md
echo "An AI-powered agent for organizing AI developer meetups." >> README.md

# First commit
git add README.md
git commit -m "Initial commit"

# Launch Claude Code
claude
```

## Step 2: Create Your CLAUDE.md (15 min)

Ask Claude to help you create a CLAUDE.md for your meetup agent:

```
Create a CLAUDE.md for a meetup planning agent called MeetupBot. This agent helps organize AI developer meetups.

Include rules for:
- Agent personality: friendly, organized, opinionated about good event structure
- Output format: all event data must be structured JSON, not freeform text
- Event plan schema: name, description, format (workshop/talk/panel/hackathon), targetAudience, estimatedAttendees, suggestedDuration, topicTags, prerequisites
- Data locations: venues in data/venues.json, speakers in data/speakers.json, past events in data/past-events/
- Naming conventions: kebab-case for files, camelCase for JSON keys
- Style: concise, actionable recommendations over vague suggestions
```

**Review the CLAUDE.md** — does it capture the rules you'd want for a meetup agent? Edit anything that feels off.

## Step 3: Set Up Project Structure (10 min)

Ask Claude to scaffold the project:

```
Create the project structure for MeetupBot:
- data/ folder with sample venues.json (5 venues with name, capacity, address, amenities, costPerHour)
- data/ folder with sample speakers.json (8 speakers with name, topics, bio, availability)
- data/past-events/ empty folder with a .gitkeep
- examples/sample-event-plan.json showing the expected output format
- config/ngrok-gateway.json with placeholder values for baseUrl and apiKey
- .claude/settings.local.json with permissions for Edit, Read, Write, Glob, Grep, Bash(git *)

Follow the rules in CLAUDE.md.
```

## Step 4: Connect to ngrok AI Gateway (10 min)

Update `config/ngrok-gateway.json` with your actual credentials:

```json
{
  "baseUrl": "https://your-gateway.ngrok.app/v1",
  "apiKey": "your-ngrok-ai-gateway-key",
  "defaultModel": "ngrok/auto",
  "fallbackModel": "gpt-4o-mini"
}
```

> **No ngrok account?** You can use a direct provider URL instead:
> ```json
> {
>   "baseUrl": "https://api.openai.com/v1",
>   "apiKey": "your-openai-key",
>   "defaultModel": "gpt-4o",
>   "fallbackModel": "gpt-4o-mini"
> }
> ```
> The agent works identically — ngrok adds routing and failover on top.

## Step 5: Build /plan-event (10 min)

Create your first slash command. Ask Claude:

```
Create a slash command at .claude/commands/plan-event.md that:
1. Takes a topic as $ARGUMENTS (e.g., "Building RAG pipelines")
2. Reads data/venues.json and data/speakers.json for context
3. Generates a structured event plan as JSON matching the schema in CLAUDE.md
4. Suggests 2-3 speakers from the speakers.json who match the topic
5. Recommends a venue from venues.json based on estimated attendance
6. Writes the plan to a file like events/building-rag-pipelines.json

IMPORTANT: The output must be valid JSON matching the schema defined in CLAUDE.md.
Use the ngrok AI Gateway config from config/ngrok-gateway.json.
```

## Step 6: Test & Commit (5 min)

Test your slash command with different topics:

```
/plan-event Building RAG pipelines
```

```
/plan-event Introduction to AI Agents
```

```
/plan-event Fine-tuning LLMs on a budget
```

Compare the outputs — are they consistent? Does the JSON schema match? Are the venue/speaker suggestions sensible?

Commit your work:
```bash
git add -A
git commit -m "feat: MeetupBot project setup with plan-event command"
```

## Checkpoint ✓

You should now have:
- [ ] Claude Code installed and authenticated
- [ ] A git repo with at least 2 commits
- [ ] CLAUDE.md with meetup agent rules and JSON schemas
- [ ] `data/venues.json` with 5 sample venues
- [ ] `data/speakers.json` with 8 sample speakers
- [ ] `config/ngrok-gateway.json` configured
- [ ] `.claude/commands/plan-event.md` working slash command
- [ ] `examples/sample-event-plan.json` reference output
- [ ] At least one generated event plan in `events/`

## Stuck?

If you're blocked or your output doesn't look right, compare your project against the reference implementation:

```bash
# See what your project should look like after this session
ls -R ../../solution/session-1/

# Compare a specific file
diff your-file.md ../../solution/session-1/equivalent-file.md
```

You can also copy the entire solution to catch up:
```bash
cp -r ../../solution/session-1/* .
cp -r ../../solution/session-1/.claude .
```

## Bonus Challenges

1. Add a `data/topics-calendar.json` with seasonal AI topics (e.g., "NeurIPS recap" in December) and have `/plan-event` suggest timely topics
2. Try the `IMPORTANT` keyword in your CLAUDE.md and see how it changes the agent's behavior
3. Generate 3 event plans and compare — is the JSON schema consistent? If not, tighten your CLAUDE.md rules
