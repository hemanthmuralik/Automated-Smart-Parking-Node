# Smart Parking Node

This is a refactored starter for the **Automated Smart Parking Node** project.

## What’s included
- Clear folder structure (routes, controllers, services, models, utils, config)
- Environment config via `.env`
- Simple in-memory model for parking slots
- Winston logger
- Basic tests using Jest + Supertest
- Scripts for dev & test
- Dockerfile and CI (example)

## Quick start

1. Copy `.env.example` to `.env` and edit values.
2. Install dependencies:
```bash
npm install
```
3. Run in dev:
```bash
npm run dev
```
4. Run tests:
```bash
npm test
```

## File Overview
- `src/app.js` — Express app and middleware
- `src/server.js` — Entrypoint
- `src/routes/parkingRoutes.js` — API routes
- `src/controllers/parkingController.js` — Route handlers
- `src/services/parkingService.js` — Business logic (abstracted)
- `src/models/slotModel.js` — In-memory model (swapable with DB)
- `src/utils/logger.js` — Winston logger
- `tests/` — Basic API tests

## Notes
This is a starter template. Replace the in-memory model with a real DB (Postgres/Mongo/Redis) for production, add more tests, CI, and monitoring as needed.
