# AI Explainer Design

## Purpose

The AI Explainer is a focused explanation feature in the SwitchToSolar platform.

Its purpose is to explain individual sections or metrics inside a generated solar report.

The Explainer helps users understand specific report values such as system size, savings, payback period, rooftop feasibility, solar generation, and bill impact.

The AI Explainer is not a general chatbot. It is designed to explain one selected report section at a time.

## Runtime Behavior

The AI Explainer works after a solar report has already been generated.

High-level runtime flow:

1. User views a generated solar report.
2. User clicks an explanation option for a specific report section.
3. The frontend sends the report token and explainer type to the backend.
4. The backend validates the report token.
5. The backend validates the requested explainer type.
6. The backend loads the saved solar report.
7. The backend selects only the report fields relevant to that explainer type.
8. The backend builds a focused prompt.
9. The LLM generates a concise explanation.
10. The explanation is returned to the frontend.
11. Request metadata may be logged for observability.

## Context Used

The AI Explainer uses report-specific context.

The exact context depends on the selected explainer type.

Common context fields may include:

- recommended solar system size
- ideal solar system size
- rooftop capacity or rooftop limitation
- estimated solar generation
- monthly electricity bill
- estimated monthly usage
- monthly savings
- annual savings
- final investment
- subsidy estimate
- payback period
- lifetime savings
- bill after solar
- solar coverage percentage
- rooftop feasibility notes

The Explainer should only use the context needed for the selected explanation.

## Supported Explanation Types

The AI Explainer can support focused explanations such as:

- system size explanation
- rooftop support explanation
- solar coverage explanation
- monthly savings explanation
- annual savings explanation
- payback period explanation
- investment explanation
- solar generation explanation
- bill impact explanation
- rooftop feasibility explanation

Each explanation type should use a controlled prompt and relevant report fields.

## Scope Rules

The AI Explainer should stay focused on the selected report section.

Allowed scope:

- explaining what a report value means
- explaining how to interpret a metric
- explaining why a value may be higher or lower
- explaining the relationship between system size, savings, generation, and payback
- explaining rooftop feasibility in simple language

Out-of-scope behavior:

- answering unrelated user questions
- acting like a general chatbot
- recommending specific installers
- comparing solar brands or vendors
- changing or recalculating official report values
- inventing missing report data
- giving unsupported claims outside the selected explanation context

If the requested explanation cannot be supported from available report context, the system should return a safe and simple explanation instead of inventing details.

## Difference from AI Advisor

The AI Advisor is conversational and handles user questions about the report.

The AI Explainer is focused and explains one selected report section.

Advisor:

- conversational
- user question driven
- can use limited chat history
- answers report-related questions

Explainer:

- section-specific
- explainer type driven
- uses focused context
- explains one metric or concept at a time

This separation keeps each AI workflow simpler and more predictable.

## Design Principles

The AI Explainer follows these design principles:

- focused explanations
- predefined explainer types
- report-grounded context
- simple language
- short and clear answers
- no open-ended chat behavior
- no unsupported calculations
- no installer or brand recommendations
- backend-controlled prompt construction
- observable AI execution

## Important Notes

The AI Explainer should not generate the official solar report values.

The solar report values are produced by deterministic backend logic.

The Explainer explains those values in plain language so users can understand the report more easily.

This separation keeps calculations controlled while using AI to improve clarity and user experience.

## Example Questions This Document Can Answer

- What is the AI Explainer?
- How does the AI Explainer work?
- What report sections can the AI Explainer explain?
- How is AI Explainer different from AI Advisor?
- Does the AI Explainer act like a chatbot?
- What context does the AI Explainer use?
- What should the AI Explainer avoid?
- Does the AI Explainer calculate solar savings?
- Why does the Explainer use predefined explanation types?
- How does the Explainer keep responses focused?
