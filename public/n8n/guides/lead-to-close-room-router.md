# n8n Guide: Lead-to-Close Room Router

## Use when
Stratos needs a repeatable internal sales ops lane for new qualified targets.

## Business promise
Every qualified lead gets a next-best-action packet instead of sitting as a name in a list.

## Workflow map
1. **Trigger:** Manual webhook, sheet row, or future CRM status change.
2. **Score router:** Determine vertical, offer tier, and urgency.
3. **Offer mapper:** Attach Launch, Growth, AI Front Desk, or Retainer recommendation.
4. **Task creation:** Create a task for audit, first touch, and follow-up.
5. **Briefing:** Send Bradley a compact packet with angle, weakness, close-room link, and first message.
6. **Status log:** Persist `new`, `contacted`, `responded`, `meeting`, `won/lost`.

## Required inputs
- Lead source
- Offer ladder rules
- Destination for tasks/briefings
- Link pattern for demos and close rooms
- Manual override process

## QA checklist
- Test one medspa, one dental, one home-services, and one legal lead.
- Confirm recommended package matches the visible pain.
- Confirm no fake client-result claims are generated.
- Confirm output points to existing demo/close-room files.

## Sales line
“This is Stratos operating on itself: every lead becomes an action packet.”
