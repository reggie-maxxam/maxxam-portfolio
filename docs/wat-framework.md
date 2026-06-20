# The WAT Framework

All MAXXAM AI systems are built using the WAT Architecture: **Workflows → Agents → Tools**. This is the operating model that separates AI reasoning from deterministic execution — the separation that makes automation systems reliable at scale.

---

## Why This Matters

When AI tries to handle every step directly, accuracy compounds downward. At 90% accuracy per step, five sequential steps produce a 59% success rate. By offloading execution to deterministic scripts and workflows, the AI stays focused on orchestration and decision-making where it excels.

---

## The Three Layers

### Layer 1: Workflows (The Instructions)

Markdown SOPs that define:
- **Objective** — what the system is trying to accomplish
- **Inputs** — what data or triggers are required
- **Tool sequence** — which scripts or n8n nodes to call and in what order
- **Expected outputs** — what success looks like
- **Edge cases** — how to handle failures, timeouts, unexpected data

These are written in plain language — the same way you'd brief a skilled contractor. They evolve as the system learns.

### Layer 2: Agents (The Decision-Maker)

The AI reasoning layer. Reads the relevant workflow, runs tools in the correct sequence, handles failures gracefully, and asks clarifying questions when needed.

The agent's job is to connect intent to execution without trying to do everything directly.

**Example:** Need to pull data from a website? The agent reads `workflows/scrape_website.md`, identifies the required inputs, then executes `tools/scrape_single_site.py`. It doesn't attempt the scrape directly.

### Layer 3: Tools (The Execution)

The deterministic execution layer — Python scripts, n8n workflows, API calls. These do the actual work:
- Data transformation
- API calls (Twilio, Gmail, Cal.com, Google Sheets)
- File operations
- Database queries

Tools are consistent, testable, and fast. Credentials live in `.env` — never hardcoded.

---

## How It Applies to n8n

In the context of n8n automation:

| WAT Layer | n8n Equivalent |
|-----------|----------------|
| Workflow | The documented SOP for what the automation should do |
| Agent | The AI node or decision logic in the workflow |
| Tool | Individual n8n nodes (Twilio, Gmail, Sheets, HTTP Request) |

The agent (AI) decides *what* to do. The tool (node) does it deterministically.

---

## The Self-Improvement Loop

Every failure is a chance to make the system stronger:

1. Identify what broke
2. Fix the tool (n8n node, Python script)
3. Verify the fix works
4. Update the workflow SOP with what was learned
5. Move on with a more robust system

This loop is how the framework improves over time. Rate limits, timing quirks, API behavior changes — they all get captured in the workflow documentation so the same mistake doesn't happen twice.

---

## Applied Example: Healthcare Follow-Up System

**Workflow SOP** (`workflows/healthcare-appointment-followup.md`):
- Trigger: New appointment booked via Cal.com
- Step 1: Send confirmation email (Gmail)
- Step 2: Schedule SMS at T-72h, T-24h, T-2h (Twilio)
- Step 3: If confirmed → cancel remaining reminders
- Step 4: If no-show → alert staff + re-engagement SMS
- Edge case: If Twilio fails → log error + fallback email

**Tools used:**
- Cal.com webhook (trigger)
- Gmail API node (email)
- Twilio node (SMS)
- Google Sheets node (logging)
- Set node (config variables)

**Agent decisions:**
- Parse incoming webhook data
- Determine which reminder sequence to trigger
- Handle conditional branches (confirmed / no-show / cancel)

---

*WAT Framework developed by MAXXAM AI. Learn more at [www.maxxam.ai](https://www.maxxam.ai)*
