# Campus Crisis Map

A web app for reporting facilities issues on campus. Students drop a pin, describe the problem, and submit anonymously. Reports show up on a live map with a heatmap so you can see where issues are piling up.

## What it does
- Anonymous reporting with a map pin drop
- Heatmap showing where problems are concentrated
- Status updates: Open, In Progress, Resolved
- Stats bar tracking total reports and resolution rate

## Built with
- Python and Flask for the backend
- SQLite for the database
- Leaflet.js and OpenStreetMap for the map
- Vanilla HTML, CSS, JavaScript for the frontend

## Why I built it
I wanted a way for students to report campus issues without having to figure out which department to email. Centralizing reports also makes it easier to spot patterns, like if the same building keeps having lighting problems.

## Run it locally
```bash
pip3 install flask
python3 app.py
```
Open http://127.0.0.1:5000

## What's next
- Rate limiting to prevent spam
- Admin login so only staff can update statuses
- Email alerts for urgent reports
- Swap SQLite for PostgreSQL before any real deployment
```

Save, then push:
```
git add README.md
git commit -m "Add README"
git push
