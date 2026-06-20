"""
redact_workflows.py — MAXXAM AI Workflow Sanitizer

Reads n8n workflow JSON files, redacts Code node jsCode content,
and writes sanitized showcase copies to the target directory.

Usage:
    python tools/redact_workflows.py
"""

import json
import os
import re
import shutil

BASE = "C:/Users/Reginald/Desktop/Synergistechs333/MAXXAM AI"
PORTFOLIO = f"{BASE}/Claude Maxxam Code/projects/maxxam-portfolio-github"
AUTOMATIONS = f"{BASE}/Claude Maxxam Code/projects/dev/backend/microservices/maxxam-automations"
OUTREACH = f"{BASE}/Claude Maxxam Code/projects/maxxam/outreach"
LAFAMILIA = f"{BASE}/LaFamilia Collateral"
MAXXPROMPTS = f"{BASE}/MaxxPrompts"

def make_stub(node_name: str, meta: dict) -> str:
    return (
        "// ── MAXXAM AI — Redacted Implementation ─────────────────────────\n"
        "//\n"
        f"// Purpose: {meta.get('purpose', f'Process data at the {node_name} stage')}\n"
        f"// Inputs:  {meta.get('inputs', 'See upstream node output')}\n"
        f"// Outputs: {meta.get('outputs', 'See downstream node input')}\n"
        "//\n"
        f"// This node implements proprietary MAXXAM AI logic.\n"
        "// Full implementation is available to MAXXAM AI clients.\n"
        "//\n"
        "// → Book a discovery call: https://tinyurl.com/maxxam-call\n"
        "// ────────────────────────────────────────────────────────────────\n"
        "\n"
        "return { json: {} }; // stub — see full implementation\n"
    )

# Per-workflow metadata for Code node stubs (node name → description)
METADATA = {
    "MAXXAM AI Readiness Scorecard - Quiz Funnel": {
        "Parse Quiz Data": {
            "purpose": "Normalize and validate the quiz.html POST payload",
            "inputs":  "Raw webhook body: email, firstName, lastName, phone, overall(%), tier, categoryScores{}, weakestCategory, industry, revenue, timeline, source, completedAt",
            "outputs": "Normalized lead object with standardized field names and defaults"
        },
        "Enrich Lead Data": {
            "purpose": "Score and tag the lead by readiness tier for downstream routing",
            "inputs":  "Normalized lead: overall(%), tier, categoryScores, weakestCategory, industry, revenue, timeline",
            "outputs": "categoryTag(hot/warm/cool/cold), emailSequence, primaryCTA, allTags, industryTag, revenueTag, timelineTag"
        }
    },
    "maxxam-content-generator": {
        "Score Content Quality": {
            "purpose": "Evaluate generated content against engagement quality criteria",
            "inputs":  "Raw draft text, topic, target audience",
            "outputs": "qualityScore(0-100), passThreshold(bool), improvementNotes"
        }
    },
    "maxxam-reddit-scraper": {
        "Filter & Score Posts": {
            "purpose": "Filter subreddit posts by keyword relevance and score by lead intent signals",
            "inputs":  "Raw Reddit API post objects: title, selftext, score, subreddit",
            "outputs": "Qualified posts with relevanceScore, intentScore, subredditTag, extractedKeywords"
        }
    },
    "maxxam-content-performance-report": {
        "Calculate Metrics": {
            "purpose": "Compute engagement metrics and week-over-week performance deltas",
            "inputs":  "Current week sheet rows: impressions, clicks, reactions, comments, reposts",
            "outputs": "engagementRate, ctr, weeklyDelta, topPerformer, lowPerformer, overallTrend"
        }
    },
    "maxxam-newsletter-hub": {
        "Route Subscriber": {
            "purpose": "Classify subscriber by engagement tier and route to appropriate sequence",
            "inputs":  "subscriberData: email, openRate, clickRate, joinDate, lastActivity",
            "outputs": "engagementTier, sequenceName, nextSendDate, suppressionFlag"
        }
    },
    "maxxam-newsletter-signup": {
        "Process Signup": {
            "purpose": "Validate, deduplicate, and enrich new subscriber record",
            "inputs":  "Webhook body: email, firstName, source, utmParams",
            "outputs": "cleanEmail, displayName, subscriberTag, welcomeSequence, sheetRow"
        }
    },
    "MAXXAM-Prospect-Outreach": {
        "Personalize Email": {
            "purpose": "Generate personalized email copy from prospect data fields",
            "inputs":  "prospect: firstName, company, industry, painPoint, source",
            "outputs": "subject, body, ctaText, sendDelay(hours), sequenceStep"
        }
    },
    "MAXXAM-Voice-Outreach": {
        "Build Call Script": {
            "purpose": "Construct dynamic call script variables for the RetellAI voice agent",
            "inputs":  "prospect: firstName, company, industry, priorTouch, timezone",
            "outputs": "agentVariables{}, callSchedule, priorityScore, fallbackSMS"
        }
    },
    "PE-01_Central_Activity_Logger": {
        "Parse Activity Event": {
            "purpose": "Normalize incoming webhook event to standardized activity log schema",
            "inputs":  "Raw webhook: eventType, source, timestamp, payload{}",
            "outputs": "activityId, category, normalizedPayload, benchmarkTag, sheetRow"
        }
    },
    "PE-01_Central_Activity_Logger_v1.1": {
        "Parse Activity Event": {
            "purpose": "Normalize incoming webhook event to standardized activity log schema",
            "inputs":  "Raw webhook: eventType, source, timestamp, payload{}",
            "outputs": "activityId, category, normalizedPayload, benchmarkTag, sheetRow"
        },
        "Handle Error": {
            "purpose": "Classify and route errors for retry or escalation",
            "inputs":  "error: message, code, sourceNode, retryCount",
            "outputs": "errorCategory, retryEligible, escalationEmail, logEntry"
        }
    },
    "airbnb-burnout-detector": {
        "Score Burnout Risk": {
            "purpose": "Calculate burnout risk score from host response patterns",
            "inputs":  "chatHistory: messages[], responseLatency, sentimentSignals",
            "outputs": "burnoutScore(0-100), riskTier(low/medium/high/critical), triggerFactors[], recommendation"
        }
    },
    "airbnb-burnout-detectorv3": {
        "Score Burnout Risk": {
            "purpose": "Calculate burnout risk score from host response patterns",
            "inputs":  "chatHistory: messages[], responseLatency, sentimentSignals",
            "outputs": "burnoutScore(0-100), riskTier, triggerFactors[], recommendation"
        }
    },
    "airbnb-burnout-detectorv4": {
        "Score Burnout Risk": {
            "purpose": "Calculate burnout risk score from host response patterns",
            "inputs":  "testPayload or chatHistory: messages[], responseLatency",
            "outputs": "burnoutScore(0-100), riskTier, recommendation"
        }
    },
    "sales automation": {
        "Parse Lead Data": {
            "purpose": "Extract and normalize lead fields from web scrape or CRM payload",
            "inputs":  "Raw lead data: name, company, linkedinUrl, email, industry",
            "outputs": "normalizedLead, qualificationScore, crmFields, outreachSequence"
        }
    },
    "sales automationv2": {
        "Parse Lead Data": {
            "purpose": "Extract and normalize lead fields from web scrape or CRM payload",
            "inputs":  "Raw lead data: name, company, linkedinUrl, email, industry, driveAssetUrl",
            "outputs": "normalizedLead, qualificationScore, crmFields, outreachSequence, assetLink"
        }
    }
}

def redact_workflow(source_path: str, dest_path: str, workflow_key: str = None) -> bool:
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except Exception as e:
        print(f"  ✗ Failed to read {source_path}: {e}")
        return False

    wf_name = workflow.get('name', workflow_key or '')
    node_meta = METADATA.get(wf_name, METADATA.get(workflow_key, {}))

    redacted_count = 0
    for node in workflow.get('nodes', []):
        if node.get('type') == 'n8n-nodes-base.code':
            node_name = node.get('name', 'Code')
            meta = node_meta.get(node_name, {})
            stub = make_stub(node_name, meta)
            if 'parameters' not in node:
                node['parameters'] = {}
            node['parameters']['jsCode'] = stub
            node['parameters'].pop('mode', None)
            redacted_count += 1

    # Standardize credential placeholders
    wf_str = json.dumps(workflow, indent=2)
    wf_str = re.sub(r'PASTE_\w+_HERE', lambda m: '{{ ' + m.group(0).replace('PASTE_','').replace('_HERE','') + ' }}', wf_str)
    wf_str = re.sub(r'"YOUR_[^"]+?"', lambda m: '"{{ ' + m.group(0).strip('"').replace('YOUR_','') + ' }}"', wf_str)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(wf_str)

    print(f"  [OK] {os.path.basename(dest_path)} ({redacted_count} Code nodes redacted)")
    return True

def copy_free(source_path: str, dest_name: str):
    dest_path = f"{PORTFOLIO}/workflows/free/{dest_name}"
    shutil.copy2(source_path, dest_path)
    print(f"  [OK] free/{dest_name}")

if __name__ == '__main__':
    print("\n=== STEP 1: Fix IP leak — redact Quiz Funnel already in repo ===")
    redact_workflow(
        f"{PORTFOLIO}/workflows/marketing/MAXXAM-AI-Readiness-Quiz-Funnel.json",
        f"{PORTFOLIO}/workflows/showcase/healthcare/MAXXAM-AI-Quiz-Funnel-SHOWCASE.json",
        "MAXXAM AI Readiness Scorecard - Quiz Funnel"
    )

    print("\n=== STEP 2: Internal / MAXXAM Operations showcases ===")
    redact_workflow(f"{AUTOMATIONS}/maxxam-content-generator.json",
                    f"{PORTFOLIO}/workflows/showcase/content/maxxam-content-generator-SHOWCASE.json",
                    "maxxam-content-generator")
    redact_workflow(f"{AUTOMATIONS}/maxxam-content-performance-report.json",
                    f"{PORTFOLIO}/workflows/showcase/operations/maxxam-content-performance-report-SHOWCASE.json",
                    "maxxam-content-performance-report")
    redact_workflow(f"{AUTOMATIONS}/maxxam-newsletter-hub.json",
                    f"{PORTFOLIO}/workflows/showcase/content/maxxam-newsletter-hub-SHOWCASE.json",
                    "maxxam-newsletter-hub")
    redact_workflow(f"{AUTOMATIONS}/maxxam-newsletter-signup.json",
                    f"{PORTFOLIO}/workflows/showcase/content/maxxam-newsletter-signup-SHOWCASE.json",
                    "maxxam-newsletter-signup")
    redact_workflow(f"{AUTOMATIONS}/maxxam-reddit-scraper.json",
                    f"{PORTFOLIO}/workflows/showcase/content/maxxam-reddit-scraper-SHOWCASE.json",
                    "maxxam-reddit-scraper")
    redact_workflow(f"{AUTOMATIONS}/telegram-image-poster.json",
                    f"{PORTFOLIO}/workflows/showcase/content/telegram-image-poster-SHOWCASE.json",
                    "telegram-image-poster")

    print("\n=== STEP 3: Outreach showcases ===")
    redact_workflow(f"{OUTREACH}/MAXXAM-Prospect-Outreach.json",
                    f"{PORTFOLIO}/workflows/showcase/sales-outreach/MAXXAM-Prospect-Outreach-SHOWCASE.json",
                    "MAXXAM-Prospect-Outreach")
    redact_workflow(f"{OUTREACH}/MAXXAM-Voice-Outreach.json",
                    f"{PORTFOLIO}/workflows/showcase/sales-outreach/MAXXAM-Voice-Outreach-SHOWCASE.json",
                    "MAXXAM-Voice-Outreach")

    print("\n=== STEP 4: LaFamilia / Operations showcases ===")
    redact_workflow(f"{LAFAMILIA}/PE-01_Central_Activity_Logger_v1.1.json",
                    f"{PORTFOLIO}/workflows/showcase/operations/PE-01-Central-Activity-Logger-SHOWCASE.json",
                    "PE-01_Central_Activity_Logger_v1.1")

    print("\n=== STEP 5: Sales / CRM showcases ===")
    redact_workflow(f"{MAXXPROMPTS}/sales automationv2.json",
                    f"{PORTFOLIO}/workflows/showcase/sales-outreach/sales-automation-SHOWCASE.json",
                    "sales automationv2")

    print("\n=== STEP 6: AI Agent showcase ===")
    redact_workflow(f"{MAXXPROMPTS}/my_ai_army2.json",
                    f"{PORTFOLIO}/workflows/showcase/ai-agent/my-ai-army-SHOWCASE.json",
                    "my_ai_army2")

    print("\n=== STEP 7: Real estate / Airbnb showcase ===")
    redact_workflow(f"{MAXXPROMPTS}/airbnb-burnout-detectorv4.json",
                    f"{PORTFOLIO}/workflows/showcase/real-estate/airbnb-burnout-detector-SHOWCASE.json",
                    "airbnb-burnout-detectorv4")

    print("\n=== STEP 8: Free templates (copy, no redaction) ===")
    copy_free(f"{AUTOMATIONS}/WF-1.1 Smart Waitlist System - Base Template.json",
              "WF-1.1-Smart-Waitlist-System.json")
    copy_free(f"{AUTOMATIONS}/maxxam-linkedin-poster.json",
              "maxxam-linkedin-poster.json")
    copy_free(f"{AUTOMATIONS}/maxxam-sheet-writer.json",
              "maxxam-sheet-writer.json")
    copy_free(f"{MAXXPROMPTS}/Airbnb75_55.json",
              "airbnb-padsplit-market-analyzer.json")
    copy_free(f"{MAXXPROMPTS}/pad split _75_55.json",
              "padsplit-75-55-rule.json")

    print("\n=== Done ===")
