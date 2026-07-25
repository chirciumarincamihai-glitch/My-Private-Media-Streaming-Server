# My Private Media Streaming Server

A private, self-hosted media streaming server, inspired by Jellyfin/Plex, built from scratch as a full-stack learning and portfolio project. It allows a small group of trusted users to securely browse and stream a personal video library from any device, without exposing the server to the public internet.

## Features

- **Video streaming** with HTTP range request support (seek/skip works natively, no custom implementation required)
- **JWT-based authentication** — registration, login, and protected API routes
- **Role-based access control** — accounts are tagged `adult` or `kid`, with content automatically filtered accordingly
- **Automated content ingestion** — a scanning script detects new video files and adds them to the database, skipping duplicates
- **Secure by design** — hashed passwords (never stored in plain text), parameterized SQL queries (SQL injection prevention), and remote access restricted to a private VPN rather than public exposure

## Tech Stack

| Layer      | Technology                              |
|------------|------------------------------------------|
| Backend    | Python, Flask, Flask-JWT-Extended, Flask-CORS |
| Database   | SQLite3                                   |
| Frontend   | React (Vite), JavaScript                  |
| Auth       | JWT (JSON Web Tokens), Werkzeug password hashing |
| Networking | Tailscale (WireGuard-based VPN) for private remote access |

## Architecture

```
[ React Frontend ] <-- fetch (JSON API) --> [ Flask Backend ] <--> [ SQLite Database ]
     (port 5173)                                (port 5000)            (movies.db)
```

The frontend and backend are fully decoupled: Flask serves a JSON API and streams raw video, while React handles all rendering and client-side logic — mirroring a real-world professional application architecture.

## Project Structure

```
Netflix 2.0/
├── backend/
│   ├── P1.py              # Flask app: routes, API, JWT config
│   ├── database.py        # Shared DB access functions (get_movies, get_user, create_user)
│   ├── scan_movies.py     # Standalone script: scans movies/ folder, inserts new entries
│   ├── movies.db          # SQLite database (movies)
│   ├── users.db           # SQLite database (users)
│   └── .env                # Secrets (JWT_SECRET_KEY) — not committed to version control
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main component: movie grid + player
│   │   ├── Login.jsx       # Login / registration form
│   │   └── App.css
│   └── .env                 # VITE_API_URL_SERVER — not committed to version control
└── movies/                  # Video files (sibling of backend/)
```

## Getting Started

### Prerequisites
- Python 3.x
- Node.js + npm
- [Tailscale](https://tailscale.com) (for remote access, optional for local-only use)

### Backend Setup
```bash
cd backend
pip install flask flask-cors flask-jwt-extended python-dotenv --break-system-packages
```

Create a `.env` file inside `backend/`:
```
JWT_SECRET_KEY=your-own-long-random-secret-here
```

Run the server:
```bash
python P1.py
```

### Frontend Setup
```bash
cd frontend
npm install
```

Create a `.env` file inside `frontend/`:
```
VITE_API_URL_SERVER=http://127.0.0.1:5000
```

Run the dev server:
```bash
npm run dev
```

### Adding Movies
Place `.mp4` files in the `movies/` folder, then run:
```bash
cd backend
python scan_movies.py
```
New files are automatically detected and added to the database; duplicates are safely skipped.

### Remote Access (optional)
1. Install Tailscale on the server machine and any client devices, logged into the same account.
2. Start Flask with `app.run(host='0.0.0.0')` (already configured) so it's reachable beyond `localhost`.
3. Start the frontend with `npm run dev -- --host` to expose it on the network.
4. Set `VITE_API_URL_SERVER` in `frontend/.env` to your Tailscale IP (e.g. `http://100.x.x.x:5000`).
5. Access the app from any Tailscale-connected device at `http://100.x.x.x:5173`.

## API Endpoints

| Method | Route         | Auth required | Description |
|--------|---------------|:---:|-------------|
| POST   | `/register`   | No | Create a new user account |
| POST   | `/login`      | No | Authenticate, returns a JWT |
| GET    | `/list`       | Yes | Returns movie metadata (filtered by role) |
| GET    | `/<movie>`    | Yes | Streams the requested video file |

## Key Design Decisions

- **SQLite over flat files** — persistent, structured storage with real querying, replacing an early prototype that used an in-memory Python dictionary.
- **Parameterized SQL queries** — all user input is passed as query parameters, never concatenated into SQL strings, preventing SQL injection.
- **Password hashing, not encryption** — passwords are hashed with Werkzeug's security utilities; the plain password is never stored or recoverable.
- **JWT over server-side sessions** — stateless authentication that scales cleanly with a separate frontend/backend architecture.
- **Tailscale VPN over public exposure** — the server is never directly reachable from the public internet; only devices authenticated on the private Tailscale network can connect.
- **Auto-incrementing primary keys** — `id` columns (not `name`) are used as unique identifiers, so records can be renamed without breaking references.

## Roadmap / Future Improvements

- [ ] Real movie thumbnails (currently placeholder)
- [ ] Logout functionality
- [ ] Configurable token expiration
- [ ] HTTPS for internal traffic
- [ ] Watch progress tracking
- [ ] Search and filter by genre/collection

## License

Personal project — not licensed for redistribution.
