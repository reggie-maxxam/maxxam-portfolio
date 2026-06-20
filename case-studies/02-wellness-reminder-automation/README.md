# Case Study 02 — Intake & Reminder Automation

**Industry:** Healthcare / Wellness Practice  
**System Type:** Intake & Scheduling Automation  
**Published:** April 2026

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| No-show rate | Baseline | **-40%** |
| Weekly admin hours (reminders) | 12 hrs | **0** |
| Disconnected tools replaced | 3 | **1 unified flow** |

---

## The Situation

A wellness practice with a full client roster had a no-show problem costing them billable hours every week. Staff were manually sending appointment reminders from three different systems — a scheduling tool, an email platform, and a separate SMS service — none of which talked to each other.

Reminders went out inconsistently. Clients slipped through. Admin time required to manage it all was eating into care delivery capacity.

---

## The System

MAXXAM AI built a single automated intake and reminder workflow connecting the practice's scheduling system to both email and SMS.

**Reminder sequence (conditional):**
1. Confirmation email — immediately on booking
2. Email reminder — 72 hours before appointment
3. SMS reminder — 24 hours before
4. Final SMS — 2 hours before

Conditional logic paused the sequence automatically if a client confirmed or rescheduled.

**Cancellation handling:**
- No-show flag → front desk alert → re-engagement message
- Cancellation → waitlist slot notification (within hours)

**Stack:** Cal.com · Twilio · Gmail API · Google Sheets · n8n

---

## Architecture Overview

```
Appointment Booked (Cal.com)
    ↓
Webhook Trigger (n8n)
    ↓
Confirmation Email (immediate)
    ↓
Schedule: Email 72h → SMS 24h → SMS 2h
    ↓
[if confirmed] → Cancel remaining reminders
[if no-show]  → Staff alert + re-engagement
[if cancel]   → Waitlist slot notification
    ↓
Google Sheets Logger
```

---

## Related Workflow

See [WF-1.1 Smart Waitlist System](../../workflows/healthcare/WF-1.1-Smart-Waitlist-System.json) for the waitlist management component of this system.

---

## The Takeaway

Most no-show problems aren't a client behavior problem — they're a communication timing problem. A structured, automated reminder sequence with conditional logic costs nothing to run after it's built and outperforms any manual reminder process by design.

---

→ [See all case studies](../../README.md#case-studies)  
→ [Book a discovery call](https://tinyurl.com/maxxam-call)
