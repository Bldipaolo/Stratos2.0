# n8n Guide: Medspa Consult Capture

## Use when
A medspa has high-ticket treatment interest but weak routing from Instagram/site visits into booked consults.

## Business promise
Turn “I’m interested in Botox/laser/body contouring” into a same-day concierge response, staff alert, and follow-up path.

## Workflow map
1. **Webhook:** Website form, quiz, or landing-page CTA posts lead data to n8n.
2. **Normalize Lead:** Standardize name, phone, email, treatment, urgency, source, notes.
3. **Treatment Router:** Branch by treatment category and urgency.
4. **Staff Alert:** Send Slack/email/SMS to front desk with exact next action.
5. **Lead Log:** Append the opportunity to Google Sheets/Airtable/CRM.
6. **Instant Reply:** Send a warm SMS/email acknowledgment.
7. **Follow-up Delay:** If no booked status appears, send a reminder sequence.

## Required client inputs
- Booking/contact form fields
- Staff notification channel
- Google Sheet/Airtable/CRM destination
- Treatment categories to route
- Approved SMS/email language
- Business hours and escalation rules

## QA checklist
- Submit a dummy consult request from mobile.
- Confirm staff alert arrives within 30 seconds.
- Confirm lead log has name, contact, treatment, urgency, source.
- Confirm prospect acknowledgment sends with no broken merge fields.
- Confirm after-hours copy does not promise live human response.
- Confirm unsubscribe/compliance language for SMS if using real numbers.

## Sales line
“Your site should not just list treatments. It should route consult intent into a premium front-desk path instantly.”
