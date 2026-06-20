# Case Study 01 — AI Voice Agent + Lead Intake

**Industry:** Healthcare / Specialty Medical Practice  
**System Type:** AI Messaging & Voice · Automated Lead Response  
**Published:** April 2026

---

## Results

| Metric | Before | After |
|--------|--------|-------|
| Lead response time | Hours | **2 minutes** |
| Inbound leads contacted | Partial | **100%** |
| Staff added | — | **0** |

---

## The Situation

A specialty medical practice was generating inbound leads through paid ads but converting a fraction of them. The problem wasn't the ads — it was response time. When a lead came in, it sat until someone on staff had a moment to follow up. By then, the prospective patient had already moved on.

The practice knew it was leaving appointments on the table but had no bandwidth to fix it manually.

---

## The System

MAXXAM AI built an AI voice agent connected directly to the practice's lead intake. The moment a new lead came in from any source, the system triggered an outbound call within two minutes.

The agent:
- Qualified the lead and answered common intake questions
- Routed confirmed appointments directly into the scheduling system
- Sent a staff notification only when an appointment was booked

No manual follow-up queue. No leads aging in a spreadsheet.

**Stack:** RetellAI · Cal.com · n8n · Twilio · Gmail

---

## Architecture Overview

```
Lead Source (Ads / Web Form)
    ↓
Webhook Trigger (n8n)
    ↓
AI Voice Agent (RetellAI)
    → Qualify → Book → Notify Staff
    ↓
Google Sheets Logger
    ↓
Weekly ROI Report (Email)
```

---

## The Takeaway

Speed is the conversion variable most practices overlook. The quality of a lead doesn't matter if the response comes too late. An AI voice agent doesn't eliminate the human relationship — it ensures the human relationship gets a chance to start.

---

→ [See all case studies](../../README.md#case-studies)  
→ [Book a discovery call](https://tinyurl.com/maxxam-call)
