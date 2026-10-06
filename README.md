# CEE Tender Intelligence v0.1.0

Initial release for monitoring Prozorro and TED procurement notices relevant to Goodram/Wilk Elektronik and KIOXIA.

## Included
- FastAPI application with responsive web UI
- PostgreSQL for Render and SQLite for quick local use
- Prozorro and TED connectors
- SSD, DRAM, Flash and NAND relevance matching
- country/category/score filters
- tender cards, item details, KAM assignment and statuses
- XLSX export with Tenders and Items sheets
- admin panel for KAM/users, roles and keywords
- Ukrainian, Polish and English UI label dictionaries
- Docker, Docker Compose, Render Blueprint and cron synchronization

## Run locally
```bash
cp .env.example .env
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Open `http://localhost:8000` and sign in using values from `.env`.

Docker alternative:
```bash
docker compose up --build
```

## Deploy to Render
1. Push the project files to a GitHub repository.
2. Create a new Render Blueprint from that repository.
3. Enter `ADMIN_EMAIL` and `ADMIN_PASSWORD` when Render requests them.
4. Deploy the Blueprint.

## Operational notes
- External APIs can change. Import failures are saved in SourceRun and shown on the dashboard.
- The product vocabulary is editable in Admin, so it can be expanded without code changes.
- Before production, add CSRF protection, server-side sessions or OIDC/SSO, rate limiting, audit logs and secret rotation.
