# Workflow Library

Ready-to-import n8n workflow templates. All credentials and client-specific values have been replaced with placeholders — look for `YOUR_*_HERE` or `PLACEHOLDER` strings and replace them before importing.

---

## How to Import

1. Open your n8n instance
2. Go to **Workflows** → **Import from file**
3. Select the `.json` file
4. Update all placeholder values in the **Config** or **Set Variables** node
5. Connect your credentials in the node settings
6. Test with a manual trigger before activating

---

## Healthcare

### WF-1.1 — Smart Waitlist System
**File:** `healthcare/WF-1.1-Smart-Waitlist-System.json`

Automated waitlist management that fills cancelled appointment slots without manual staff intervention.

**What it does:**
- Monitors a Google Sheet waitlist on a schedule trigger
- When a cancellation or open slot is detected, sends SMS notifications to waitlisted clients
- Routes first respondent to booking link
- Updates sheet to mark slot as filled

**Placeholders to replace:**
| Variable | Description |
|----------|-------------|
| `YOUR_GOOGLE_SHEET_URL_HERE` | URL of your waitlist Google Sheet |
| `+1XXXXXXXXXX` | Your Twilio sender number |
| `YOUR_BOOKING_URL_HERE` | Cal.com or scheduling link |
| `YOUR_SHEET_NAME_HERE` | Name of the waitlist tab |

**Credentials needed:** Google Sheets OAuth · Twilio

---

## Marketing

### MAXXAM AI Readiness Quiz Funnel
**File:** `marketing/MAXXAM-AI-Readiness-Quiz-Funnel.json`

Lead scoring and routing workflow for quiz-based funnel. Receives quiz submissions, scores and tags leads by tier (hot/warm/cool/cold), logs to Google Sheets, and triggers tiered email sequences.

**What it does:**
1. Receives quiz submission via webhook
2. Parses and normalizes payload
3. Scores lead and assigns routing tags (industry, revenue, timeline, readiness tier)
4. Routes to appropriate email sequence
5. Logs to Google Sheets
6. Sends branded results email with booking link
7. Alerts owner for hot leads (advanced tier)

**Placeholders to replace:**
| Variable | Description |
|----------|-------------|
| `YOUR_SHEET_ID_HERE` | Google Sheet ID for lead logging |
| `YOUR_SENDER_EMAIL` | Verified Gmail or SMTP sender |
| `YOUR_BOOKING_URL` | Discovery call booking link |
| `YOUR_OWNER_EMAIL` | Email to receive hot lead alerts |

**Credentials needed:** Google Sheets OAuth · Gmail (or SMTP) · Webhook URL configured in your quiz form

---

## Adding More Workflows

These are the first two published workflows. Additional templates will be added for:
- [ ] Outbound prospect outreach sequence
- [ ] LinkedIn content scheduler
- [ ] Weekly performance report (email)
- [ ] Newsletter signup + welcome sequence

---

*All workflows built with n8n v1.x. Import and test in a staging environment before production use.*
