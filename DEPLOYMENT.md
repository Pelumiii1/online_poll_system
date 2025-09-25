# Deployment Guide

## PostgreSQL Database Configuration

This project is configured to work with both SQLite (development) and PostgreSQL (production) databases.

### Environment Variables

For production deployment, set the following environment variables:

```bash
DATABASE_URL=postgresql://online_poll_system_kk3u_user:CFhhHHoD1URqgQoxHGeny8ruFVMYSLwF@dpg-d35fvj3uibrs73d4gkc0-a/online_poll_system_kk3u
SECRET_KEY=your-production-secret-key-here
RENDER=true
```

**Important**: Generate a secure SECRET_KEY for production. You can use Django's get_random_secret_key() function or an online generator.

### Production Settings

The application automatically detects production environment based on:
- `RENDER=true` environment variable (for Render.com)
- Presence of `DATABASE_URL` environment variable

### Database Migration

After deployment, run the following commands:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### Security Features

When `DEBUG=False`, the following security features are automatically enabled:
- SSL redirect
- HSTS headers
- Secure cookies
- XSS protection
- Content type sniffing protection

### Local Development

For local development, the application uses SQLite by default. No additional configuration needed.

```bash
python manage.py runserver
```

## Deployment Platforms

### Render.com
- Set `DATABASE_URL` environment variable
- Set `RENDER=true` environment variable
- The app will automatically use production settings

### Other Platforms
- Set `DATABASE_URL` environment variable
- Ensure `DEBUG=False` for production
- Configure static files serving