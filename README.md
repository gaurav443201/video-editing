# Video Editing Service App (MVP)

This is a working **MVP** for your service-based platform that connects **Customers** and **Editors** with an **Admin** controlling assignments and payments.

## What’s included
- ✅ FastAPI backend (JWT auth, roles: customer/editor/admin)
- ✅ SQLite database via SQLAlchemy
- ✅ Project workflow (create → assign → edit → sample → approve → final)
- ✅ File uploads for media & samples (local storage)
- ✅ Payment placeholders (UPI/PhonePe ref via transaction_id), commission logic
- ✅ Minimal static frontend to test core flows

## Run backend (Python 3.10+)
```bash
cd backend
python -m venv .venv
# Linux/Mac: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### Seed admin
Use the `/auth/signup` endpoint with role `admin` to create your admin user (first time).

## Minimal Frontend
Serve `frontend/static/` with any static server (or open `index.html` and set API URL).
You can also test everything via FastAPI Swagger UI.

## Notes
- This is an MVP. Replace payment placeholders with a real gateway (Razorpay/PhonePe/Stripe).
- For production: use S3/Cloud storage, HTTPS, proper CORS, rate limiting, background tasks, and a real RDBMS.
