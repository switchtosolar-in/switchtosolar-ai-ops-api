# Lead Workflow

## Purpose

The lead workflow manages user interest after a homeowner requests a solar quote or takes an action that indicates interest in installation.

The purpose of the lead system is to track homeowner requests, assign or expose leads to eligible installers, monitor installer response activity, and help admins understand lead aging and follow-up status.

This workflow is important because solar leads lose value if they are not handled quickly.

## Lead Creation

A lead is created when a user submits a solar request or quote request through the SwitchToSolar platform.

A lead may include information such as:

- customer name
- phone number
- email
- city
- state
- monthly electricity bill
- estimated solar requirement
- location or rooftop information
- report token
- preferred contact or quote request details
- submitted timestamp

The lead record becomes the operational unit tracked by admins and installers.

## Lead Lifecycle

A typical lead moves through this lifecycle:

1. User submits a solar request.
2. The platform stores the lead.
3. The lead is assigned or made available to eligible installers.
4. Installer unlocks or accesses the lead based on platform rules.
5. Installer contacts the user.
6. Installer updates the lead status.
7. Admin monitors lead response, aging, and outcome.

## Lead Statuses

Lead statuses help track the current stage of a customer opportunity.

Common lead status values may include:

- new
- unlocked
- in_talks
- installing
- won
- lost

## Meaning of Lead Statuses

New:

The lead has been submitted but has not progressed into active follow-up.

Unlocked:

An installer has accessed or unlocked the lead details.

In Talks:

The installer and customer are communicating.

Installing:

The customer has moved toward installation or installation is in progress.

Won:

The lead successfully converted into a confirmed solar installation opportunity.

Lost:

The opportunity did not convert or is no longer active.

## SLA and Lead Aging

SwitchToSolar tracks lead aging using SLA-style buckets.

SLA buckets help identify how quickly leads are being handled.

Typical SLA buckets:

- HOT: 0–6 hours
- WARM: 6–12 hours
- COLD: 12–24 hours
- DYING: 24–36 hours
- OVERDUE: 36+ hours

The goal is to identify leads that are becoming stale and may need faster follow-up.

## Stale Leads

A stale lead is a lead that has not received timely action.

In operational reporting, stale leads may refer to leads that are still in a new status after a certain number of hours.

Example:

A lead submitted more than 24 hours ago and still marked as new can be treated as stale.

Stale lead tracking helps admins monitor installer responsiveness and platform health.

## Installer Assignment

Leads may be assigned or made available to installers based on platform rules.

Installer eligibility can depend on factors such as:

- active status
- approved status
- city coverage
- service availability
- platform rules
- admin assignment decisions

The lead assignment workflow should prevent inactive, archived, or unapproved installers from receiving inappropriate lead access.

## Lead Unlocking

Installers may unlock or access lead details based on the platform model.

Lead unlocking allows an installer to view customer contact information or lead details needed for follow-up.

Unlocking should be tracked because it helps measure installer activity and response behavior.

## Admin Monitoring

Admins may monitor leads using operational views and summaries.

Useful admin questions include:

- How many new leads were submitted today?
- How many leads are stale?
- How many leads are overdue?
- How many leads are in each status?
- Which leads are waiting too long?
- Which installers are responding quickly?
- How many leads moved from new to in_talks?
- How many leads became won or lost?

## AI Ops Relevance

The AI Ops system can answer operational questions about lead activity using controlled backend tools.

Supported operational questions may include:

- number of new leads in a time window
- stale lead count
- SLA bucket summary
- lead status summary
- report activity connected to leads
- recent operational activity

AI Ops should not generate arbitrary SQL for lead questions.

Operational answers should come from predefined repository functions and controlled database queries.

## Operational Safety Rules

Lead data may contain sensitive customer information.

AI workflows should avoid exposing unnecessary customer details.

Operational AI responses should prefer summaries and counts over raw customer records.

Examples of safer outputs:

- total new leads
- stale lead count
- SLA bucket summary
- lead status distribution
- top activity categories

Examples of riskier outputs:

- full customer phone numbers
- full customer emails
- raw lead notes
- complete address lists
- unrestricted lead record dumps

## Important Notes

The lead workflow connects user interest, installer response, admin visibility, and platform operations.

Fast lead handling improves customer experience and installer value.

SLA tracking helps identify when leads are not being handled quickly enough.

Controlled operational retrieval allows AI Ops to answer lead-related questions without giving the model unrestricted database access.

## Example Questions This Document Can Answer

- What is a lead in SwitchToSolar?
- How is a lead created?
- What is the lead lifecycle?
- What are lead statuses?
- What does new lead mean?
- What does unlocked lead mean?
- What does in_talks mean?
- What does won or lost mean?
- What are SLA buckets?
- What is a stale lead?
- What does overdue lead mean?
- How does installer assignment work?
- Why does lead aging matter?
- How can AI Ops answer lead questions?
- Why should AI Ops avoid exposing raw lead records?
