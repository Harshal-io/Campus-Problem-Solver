# 🎓 Campus Problem Solver

An AI-powered campus complaint resolution system.

## Features
1. **Student Submission Portal**: Submit complaints with optional images.
2. **AI Classification Agent**: Matches complaints to predefined categories.
3. **Automated Routing**: Routes complaints to the appropriate department.
4. **Tracking Dashboard**: Track status with a unique ID.
5. **Admin Dashboard**: Executive dashboard to overview, update status, and export analytics.

## Tech Stack
- Frontend: Streamlit
- Database: SQLite
- AI Classification: Google Gemini API (gemini-1.5-flash)
- Image Handling: Pillow
- Notifications: File logging & optional SMTP

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your API Key: Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` or as an environment variable. Obtain a free key from [Google AI Studio](https://aistudio.google.com/).
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Environment Variables
| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | Your Google Gemini API Key |
| `ADMIN_PASSWORD` | Password for the Admin Dashboard |
| `SMTP_HOST` | Host for email notifications |
| `SMTP_USER` | SMTP User |
| `SMTP_PASS` | SMTP Password |
| `ADMIN_EMAIL` | Admin Email |

## Folder Structure
```
├── app.py                # Main Entry Point
├── pages/                # Streamlit Pages (submit, track, admin)
├── core/                 # Backend logic (classifier, db, router, notifier)
├── data/                 # Database and schema
├── logs/                 # Notification logs
├── uploads/              # Uploaded images
└── .streamlit/           # Streanlit secrets
```

## AI Classification
- **Model**: `gemini-1.5-flash`
- **Fallback**: Keyword based matching if API is unavailable.
- **Categories**:
  - Bathroom & Hygiene -> Housekeeping Department
  - Anti-Ragging & Safety -> Student Affairs / Security Office
  - Mess & Food Quality -> Mess Committee / Warden
  - Academic Issues -> Academic Office / HOD
  - Infrastructure/Maintenance -> Campus Maintenance Cell
  - Other -> General Administration

## Deployment
1. Push to GitHub
2. Connect repo on share.streamlit.io
3. Add secrets (`GEMINI_API_KEY`, `ADMIN_PASSWORD`) in Streamlit Cloud Dashboard settings.

## License
MIT License
