# PU-Connect (PU-Marketplace) 🎓🛒

PU-Connect is a specialized campus commerce platform designed for university students to buy, sell, and trade items safely within their campus community. It features real-time chat, university email verification, and a modern, interactive dashboard.

## 🚀 Features

- **Secure Authentication**: Traditional email/username login and Google Social Auth integration.
- **Student Verification**: Built with campus safety in mind.
- **Real-time Chat**: Instant messaging between buyers and sellers powered by Django Channels and Redis.
- **Product & Service Listings**: Separate categories for physical goods and student-provided services.
- **Interactive Dashboard**: A centralized hub for managing listings, messages, and profile settings.
- **Responsive Design**: Mobile-first approach with a custom, sleek UI (Dark/Light mode support).

## 🛠️ Tech Stack

- **Backend**: Django 6.0, Django Channels (ASGI)
- **Database**: PostgreSQL
- **Caching/Real-time**: Redis
- **Frontend**: Vanilla CSS (Modern CSS Variables), JavaScript (Async/Await API)
- **Deployment**: Docker, Render-ready

## 🛠️ Local Development Setup

### Prerequisites
- Docker & Docker Compose
- (Optional) Python 3.12+ and Pipenv

### 1. Clone the repository
```bash
git clone <repository-url>
cd PU_MART
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://postgres:postgres_pass@db:5432/pu_mart_db
REDIS_URL=redis://redis:6379
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_PASSWORD=admin_pass
DJANGO_SUPERUSER_EMAIL=admin@example.com
```

### 3. Run with Docker
```bash
docker-compose up --build
```
The app will be available at `http://localhost:8000`.

## 🚢 Production (Render)

This application is configured for deployment on Render using the included `Dockerfile` and `docker/entrypoint.sh`.

### Essential Environment Variables for Production:
| Variable | Description |
| :--- | :--- |
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string (Internal) |
| `SECRET_KEY` | A long, random string for security |
| `DEBUG` | Set to `False` |
| `DJANGO_SUPERUSER_USERNAME` | Auto-creates admin on first deploy |
| `DJANGO_SUPERUSER_PASSWORD` | Password for the auto-created admin |
| `GOOGLE_CLIENT_ID` | Google OAuth2 Client ID |
| `GOOGLE_CLIENT_SECRET` | Google OAuth2 Client Secret |

### ⚠️ Critical Google Console Setting
You **must** add this exact URL to your "Authorized redirect URIs" in the Google Cloud Console:
`https://puconnect-jr7q.onrender.com/accounts/google/login/callback/`

## 📁 Project Structure

- `Auth_app/`: User authentication, login/signup views, and social auth logic.
- `Base_app/`: Static pages (Home, About, Help, Terms).
- `dash_app/`: Main user dashboard and activity management.
- `chat_app/`: Real-time messaging logic (WebSockets).
- `Listings_app/`: Product and service listing management.
- `Profile_app/`: User profile management and automated signals.
- `pu_mp/`: Main project configuration and settings.

## 🤝 Contributing

1. Fork the project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
