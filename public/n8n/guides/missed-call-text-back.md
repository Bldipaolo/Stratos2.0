# n8n Guide: Missed-Call Text-Back

## Use when
A business misses calls during treatments, jobs, court, lunch, weekends, or after hours.

## Business promise
Recover leads at the moment they are still interested instead of waiting for staff to call back manually.

## Workflow map
1. **Phone webhook:** Phone provider sends missed-call payload.
2. **Classify urgency:** Route emergency/high-value/service category if available.
3. **Immediate SMS:** “Sorry we missed you — what can we help with?”
4. **Team notification:** Alert owner/front desk with caller, source, and recommended action.
5. **Log opportunity:** Add row to CRM/Sheet with status `missed_call_recovered`.
6. **Owner digest:** Daily summary of recovered/missed/unanswered opportunities.

## Required client inputs
- Phone provider with webhook support or missed-call export
- SMS provider credentials in n8n only
- Approved reply language
- Business hours
- Emergency escalation rules
- Destination log system

## QA checklist
- Trigger with internal test number only.
- Verify no SMS loops occur if the customer replies repeatedly.
- Verify emergency wording is safe and does not guarantee immediate service.
- Verify team alert includes callback number and timestamp.
- Verify duplicate missed calls within 10 minutes do not spam the prospect.

## Sales line
“The first company to respond clearly usually wins. This gives your front desk a second chance every time they miss a call.”
