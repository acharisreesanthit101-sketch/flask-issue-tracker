# Civic Desk — Smart Issue Reporter

A full-stack web app for reporting and tracking local civic issues (roads, electricity, water) with automatic AI-based tagging and status tracking.

🔗 **Live demo:** https://flask-issue-tracker.onrender.com
*(Free tier — first load may take ~30-50s if the server's been idle)*

<img width="1920" height="1080" alt="Screenshot 2026-06-21 191115" src="https://github.com/user-attachments/assets/1d33aa6e-7479-46c4-84c0-6995e85e2ac6" />
<img width="1920" height="1080" alt="Screenshot 2026-06-21 191139" src="https://github.com/user-attachments/assets/c651cb88-8681-4561-be79-ed2764a173f6" />


## Features
- Submit issues with name and description
- Automatic tag detection — descriptions are scanned for keywords and auto-categorized as Road, Electricity, Water, or General
- Persistent storage with SQLite — data survives restarts
- Open/Closed status tracking with one-click toggle
- Filter issues by tag and by status
- Delete issues
- Auto-refreshing list (polls every 3 seconds) — no manual reload needed
- Responsive, custom-designed UI (no framework/template used)

## Tech Stack
- **Backend:** Python, Flask, REST API design
- **Database:** SQLite
- **Frontend:** HTML, CSS, vanilla JavaScript (fetch API, DOM manipulation)
- **Deployment:** Render (Gunicorn WSGI server)

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| POST | `/add-issue` | Create a new issue (auto-tagged) |
| GET | `/issues` | Fetch all issues |
| DELETE | `/delete-issue/<id>` | Delete an issue |
| PATCH | `/toggle-status/<id>` | Toggle Open/Closed status |

## How to Run Locally
1. Clone the repo
   git clone https://github.com/acharisreesanthit101-sketch/flask-issue-tracker.git
   cd flask-issue-tracker
