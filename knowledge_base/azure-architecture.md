# Azure Architecture

## Purpose

SwitchToSolar uses Microsoft Azure infrastructure to host the public website, backend API, database, storage, payments, email services, and production routing.

The architecture is designed around separate frontend and backend services, Azure Front Door routing, Azure SQL for structured data, and secure backend-controlled access to platform resources.

This document describes the production architecture for retrieval and AI Ops knowledge answering.

## Public Domain Routing

SwitchToSolar uses the public domain:

- `https://switchtosolar.in` as the canonical domain
- `https://www.switchtosolar.in` as the redirected www domain

The domain is managed through Namecheap DNS.

DNS records route public traffic to Azure Front Door.

Typical DNS configuration:

- apex domain `switchtosolar.in` uses an ALIAS record pointing to the Azure Front Door endpoint
- `www.switchtosolar.in` uses a CNAME record pointing to the Azure Front Door endpoint
- TXT records may be used for domain validation and email authentication

## Azure Front Door

Azure Front Door is the public entry point for SwitchToSolar traffic.

Azure Front Door responsibilities include:

- accepting public HTTPS traffic
- managing custom domains
- handling TLS certificates
- redirecting `www.switchtosolar.in` to `switchtosolar.in`
- routing API requests to the backend origin
- routing all other requests to the frontend origin

The production Front Door setup uses path-based routing.

Routing behavior:

- `/api/*` routes to the backend API origin group
- `/*` routes to the frontend origin group

This allows the public website and API to share the same domain while still running on separate Azure App Services.

## Canonical Host Redirect

The canonical public domain is:

`https://switchtosolar.in`

The `www` domain redirects to the apex domain.

Redirect behavior:

- `https://www.switchtosolar.in` redirects to `https://switchtosolar.in`
- redirect type is 301
- path and query string should be preserved

This keeps SEO and user access consistent.

## Frontend App Service

The frontend is hosted on Azure App Service for Linux.

The frontend application is built with Next.js.

Frontend responsibilities include:

- public website rendering
- solar plan user interface
- solar report display
- installer discovery pages
- AI Advisor interface
- AI Explainer interface
- admin dashboard interface
- partner dashboard interface

The frontend origin is routed through Azure Front Door for public access.

The frontend should call backend APIs through the same public domain using `/api/*` routes.

The frontend should not directly connect to the database, payment provider, email provider, or internal AI services.

## Backend App Service

The backend is hosted on Azure App Service for Linux.

The backend application is built with Node.js and Express.

Backend responsibilities include:

- API routing
- authentication and authorization
- admin and partner session handling
- CSRF protection for admin write operations
- solar report generation
- deterministic solar calculation logic
- lead workflows
- installer workflows
- payment workflows
- webhook verification
- email sending
- database access
- protected AI workflow orchestration

The backend origin is routed through Azure Front Door for `/api/*` traffic.

## Azure SQL Database

SwitchToSolar uses Azure SQL Database as the main structured database.

Azure SQL may store data related to:

- users
- leads
- installers
- cities
- solar reports
- partner dashboard records
- admin workflow records
- payments or transaction records
- AI request logs and feedback where applicable

The backend owns database access.

The frontend should not directly access Azure SQL.

## Azure Blob Storage

SwitchToSolar uses Azure Blob Storage for media or file storage needs.

Blob storage can support platform assets such as uploaded media, documents, installer-related files, or other object storage requirements.

The backend should control access to blob storage when sensitive or private files are involved.

## Payment Integration

SwitchToSolar uses Razorpay for payments and webhook handling.

The backend is responsible for:

- creating payment-related server-side records
- verifying Razorpay webhooks
- validating payment status
- updating platform payment state
- protecting payment-related secrets

Payment keys and webhook secrets should stay server-side.

## Email Integration

SwitchToSolar uses Resend for transactional emails.

Transactional email use cases may include:

- user notifications
- admin notifications
- lead workflow notifications
- installer or partner communication
- platform operational messages

Email API keys should stay server-side and should not be exposed to frontend code.

## Authentication and Security

SwitchToSolar uses backend-controlled authentication for admin and partner workflows.

Security concepts include:

- session cookies
- JWT stored in cookies
- role-based access for admin and partner users
- secure cookies in production
- SameSite cookie policy
- CSRF protection for admin write operations
- restricted CORS origins
- protected backend routes

Production cookies should be configured securely.

Common cookie principles:

- `Secure=true` in production
- `SameSite=Lax`
- domain scoped to `.switchtosolar.in` when shared across subdomains is required
- path scoped appropriately
- sensitive tokens not exposed to JavaScript when possible

## CORS and Allowed Origins

Backend CORS should allow trusted production origins only.

Typical allowed origins include:

- `https://switchtosolar.in`
- `https://www.switchtosolar.in`

CORS should not be open to arbitrary origins in production.

## Service Communication Flow

Typical production request flow:

1. User opens `https://switchtosolar.in`.
2. Namecheap DNS points the request to Azure Front Door.
3. Azure Front Door accepts HTTPS traffic.
4. Front Door routes frontend page requests to the frontend App Service.
5. Front Door routes `/api/*` requests to the backend App Service.
6. Backend handles business logic, authentication, database access, payments, email, or AI workflow orchestration.
7. Backend returns the response through Front Door to the browser.

## API Routing Flow

API requests follow this path:

`Browser -> Azure Front Door -> /api/* route -> Backend App Service -> Azure SQL / Blob / Razorpay / Resend / AI services`

This keeps API execution controlled by the backend.

## Frontend Routing Flow

Frontend page requests follow this path:

`Browser -> Azure Front Door -> /* route -> Frontend App Service -> Next.js application`

The frontend renders the user interface and calls backend APIs through the public domain.

## AI Ops Relationship

The AI Ops API is a separate FastAPI service used for retrieval-grounded AI and operational AI workflows.

AI Ops responsibilities may include:

- knowledge base ingestion
- chunking
- embedding generation
- PostgreSQL + pgvector semantic retrieval
- intent routing
- prompt construction
- LLM execution
- operational AI tooling
- query logging
- AI observability

In a production architecture, frontend clients should not directly call internal AI Ops services.

A safer architecture routes admin AI requests through the backend first.

Expected AI Ops access pattern:

`Admin UI -> Backend protected API -> FastAPI AI Ops service -> Retrieval / Operations -> Response`

This keeps AI Ops behind backend governance.

## Environment Separation

SwitchToSolar uses environment-based configuration.

Common environments include:

- local development
- staging
- production

Environment separation helps prevent test settings, staging data, and production secrets from being mixed together.

Important configuration should be controlled through environment variables.

## Secrets and Configuration

Sensitive values should not be committed to GitHub.

Sensitive values include:

- database credentials
- API keys
- JWT secrets
- session secrets
- payment provider secrets
- email provider API keys
- internal service URLs
- webhook secrets

A `.env.example` file can document required configuration using safe placeholder values.

The real `.env` file should be ignored by Git.

## Security Principles

The Azure architecture follows these principles:

- use HTTPS for public traffic
- route public traffic through Azure Front Door
- keep frontend and backend as separate services
- route API traffic through `/api/*`
- keep secrets out of source code
- keep database access backend-controlled
- protect admin and partner routes
- use CSRF protection for admin write actions
- restrict CORS to trusted domains
- avoid exposing internal service URLs to public clients
- route AI workflows through governed backend APIs

## Important Notes

Azure Front Door acts as the public traffic gateway.

The frontend and backend run as separate Azure App Services.

Azure SQL stores structured platform data.

Azure Blob Storage supports object storage needs.

Razorpay handles payments and webhooks.

Resend handles transactional email.

The backend is the main governance layer for database access, authentication, payments, email, and protected AI workflows.

## Example Questions This Document Can Answer

- How is SwitchToSolar hosted?
- What is the role of Azure Front Door?
- How does switchtosolar.in route traffic?
- What happens to `/api/*` requests?
- What happens to frontend page requests?
- What is the canonical domain?
- Why does www redirect to the apex domain?
- What does the frontend App Service do?
- What does the backend App Service do?
- What database does SwitchToSolar use?
- What is Azure Blob Storage used for?
- How does Razorpay fit into the architecture?
- How does Resend fit into the architecture?
- How does authentication work at a high level?
- Why should the frontend not access the database directly?
- Should the frontend call AI Ops directly?
- How does AI Ops connect to the platform?
- Where should secrets be stored?
- Why is `.env.example` useful?
- What are the main Azure security principles?
