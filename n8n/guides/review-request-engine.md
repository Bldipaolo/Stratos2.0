# n8n Guide: Review Request Engine

## Use when
A business has happy customers but inconsistent review growth.

## Business promise
Ask at the right time, route unhappy feedback privately, and turn real customer proof into reusable sales assets.

## Workflow map
1. **Completed milestone trigger:** Appointment completed, job closed, invoice paid, or manual webhook.
2. **Eligibility gate:** Skip if customer opted out, is unhappy, or already reviewed recently.
3. **Review request:** Send SMS/email with direct review link.
4. **Feedback branch:** If rating is low, route to owner before asking for public review.
5. **Reminder delay:** One respectful follow-up if no action.
6. **Proof log:** Save review source/date/context for marketing use.

## Required client inputs
- Review link(s)
- Customer completion trigger source
- Opt-out rules
- Approved message copy
- Private feedback destination
- Proof usage consent process

## QA checklist
- Confirm opt-out and low-rating paths stop public review asks.
- Confirm direct review URL works on mobile.
- Confirm duplicate customers are throttled.
- Confirm proof log captures source/date/context.
- Do not fabricate reviews, ratings, or customer quotes.

## Sales line
“Reviews should not depend on someone remembering to ask. The system asks consistently and protects the brand when feedback is negative.”
