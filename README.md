# Online Poll System

A Django REST API-based online polling system that allows users to create, manage, and participate in polls with secure authentication and authorization.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Poll Management**: Create, read, update, and delete polls
- **Secure Voting**: Authenticated users can vote on polls with proper permissions
- **RESTful API**: Well-structured API endpoints with DRF (Django REST Framework)
- **Database Integration**: PostgreSQL support for production environments
- **API Documentation**: Auto-generated API documentation with drf-spectacular

## Technology Stack

- **Backend**: Django 5.2.6
- **API Framework**: Django REST Framework 3.16.1
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: PostgreSQL (with psycopg2)
- **API Documentation**: drf-spectacular
- **Production Server**: Gunicorn with Whitenoise for static files

## Project Structure

```
online_poll_system/
├── accounts/                 # User authentication app
│   ├── models.py            # Custom user model
│   ├── views.py             # Authentication views
│   ├── serializer.py        # User serializers
│   └── urls.py              # Authentication URLs
├── poll/                    # Poll management app
│   ├── models.py            # Poll and Vote models
│   ├── views.py             # Poll CRUD operations
│   ├── serializer.py        # Poll serializers
│   ├── permissions.py       # Custom permissions
│   └── urls.py              # Poll URLs
├── online_poll_system/      # Main project settings
│   ├── settings.py          # Django settings
│   └── urls.py              # Main URL configuration
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd online_poll_system
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:

   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   DATABASE_URL=postgres://username:password@localhost:5432/poll_db
   ```

5. **Run database migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser** (optional):

   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication

- `POST /accounts/register/` - User registration
- `POST /accounts/login/` - User login (get JWT tokens)
- `POST /accounts/token/refresh/` - Refresh JWT token

### Polls

- `GET /poll/polls/` - List all polls
- `POST /poll/polls/` - Create a new poll (authenticated users)
- `GET /poll/polls/{id}/` - Get specific poll details
- `PUT /poll/polls/{id}/` - Update poll (poll creator only)
- `DELETE /poll/polls/{id}/` - Delete poll (poll creator only)
- `POST /poll/polls/{id}/vote/` - Vote on a poll (authenticated users)

## API Documentation

Once the server is running, you can access the auto-generated API documentation at:

- **Swagger UI**: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://127.0.0.1:8000/api/schema/`

## Usage Example

1. **Register a new user**:

   ```bash
   curl -X POST http://127.0.0.1:8000/accounts/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123"}'
   ```

2. **Login to get JWT token**:

   ```bash
   curl -X POST http://127.0.0.1:8000/accounts/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "testpass123"}'
   ```

3. **Create a poll** (using the access token):
   ```bash
   curl -X POST http://127.0.0.1:8000/poll/polls/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     -d '{"question": "What is your favorite programming language?", "options": ["Python", "JavaScript", "Java"]}'
   ```

## Development

- **Run tests**: `python manage.py test`
- **Create migrations**: `python manage.py makemigrations`
- **Apply migrations**: `python manage.py migrate`
- **Check code**: `python manage.py check`

## Production Deployment

The project is configured for production deployment with:

- Gunicorn WSGI server
- Whitenoise for static file serving
- PostgreSQL database support
- Environment-based configuration

## License

This project is licensed under the MIT License - see the LICENSE file for details.
