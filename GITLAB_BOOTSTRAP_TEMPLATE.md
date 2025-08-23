---
name: Django Onam Project Bootstrap
about: Complete project setup for Onam Celebration & Treasure Hunt Django application
title: 'Bootstrap Django Onam Celebration & Treasure Hunt App'
labels: ['enhancement', 'bootstrap', 'django', 'onam']
assignees: ''
---

## 🌸 Project Bootstrap Request: Onam Celebration & Treasure Hunt Django App

### Project Overview
Create a complete Django application celebrating Onam festival with an interactive SMS-based treasure hunt game, user authentication via Swedish phone numbers, and beautiful cultural content.

### 📋 Requirements Checklist

#### 🏗️ Core Infrastructure
- [ ] Django 4.2+ project setup with Python 3.11+
- [ ] PostgreSQL database (production) / SQLite (development)
- [ ] Docker containerization with docker-compose
- [ ] GitLab CI/CD pipeline configuration
- [ ] Environment-based settings (development/staging/production)
- [ ] Celery for background tasks with Redis broker
- [ ] Static files handling with WhiteNoise

#### 🎨 Frontend & UI
- [ ] Bootstrap 5 responsive design
- [ ] Kerala-themed color scheme (gold, green, white)
- [ ] Mobile-first responsive layout
- [ ] Custom CSS animations for Onam elements
- [ ] Font Awesome icons integration
- [ ] Progressive Web App (PWA) features

#### 🏠 Homepage Features
- [ ] Beautiful Onam celebration landing page
- [ ] Pookalam (flower carpet) gallery section
- [ ] Traditional Sadhya (feast) information
- [ ] Kerala cultural elements (Pulikali, Kathakali, etc.)
- [ ] King Mahabali legend storytelling
- [ ] Interactive game preview section
- [ ] Responsive navigation with user status

#### 👥 User Authentication System
- [ ] Custom User model with Swedish phone numbers (+46 format)
- [ ] Phone number validation and formatting
- [ ] SMS OTP verification (Twilio/MessageBird integration)
- [ ] Registration form with phone verification
- [ ] Login/logout functionality
- [ ] Password reset via SMS
- [ ] User profile management
- [ ] Phone number change with re-verification

#### 📱 SMS Integration
- [ ] Twilio SDK integration for SMS services
- [ ] MessageBird as alternative SMS provider
- [ ] OTP generation and validation
- [ ] Rate limiting for SMS sending (10/hour default)
- [ ] SMS templates for different message types
- [ ] Webhook endpoints for SMS delivery status
- [ ] Console backend for development/testing
- [ ] SMS delivery tracking and logs

#### 🎯 Treasure Hunt Game
- [ ] Multi-level game progression system
- [ ] SMS-based clue delivery mechanism
- [ ] Progress tracking per user
- [ ] Answer validation and scoring
- [ ] Leaderboard with rankings
- [ ] Game state management
- [ ] Clue difficulty levels
- [ ] Hint system for stuck players
- [ ] Game completion rewards
- [ ] Admin interface for game management

#### 🛡️ Security & Performance
- [ ] Django security best practices
- [ ] CSRF protection and secure headers
- [ ] Rate limiting for critical endpoints
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection
- [ ] Secure session management
- [ ] Environment variables for sensitive data
- [ ] HTTPS enforcement in production

#### 🧪 Testing & Quality
- [ ] Unit tests for all models and views
- [ ] Integration tests for SMS workflows
- [ ] Game logic testing
- [ ] Authentication flow testing
- [ ] API endpoint testing
- [ ] Code coverage reporting (>80%)
- [ ] Pytest configuration
- [ ] Factory Boy for test data
- [ ] Mock SMS services for testing

#### 📊 Monitoring & Logging
- [ ] Comprehensive logging configuration
- [ ] Error tracking with Sentry (optional)
- [ ] Health check endpoints
- [ ] Performance monitoring
- [ ] Database query optimization
- [ ] Cache implementation with Redis
- [ ] Metrics collection for game analytics

#### 🌐 API & Integration
- [ ] RESTful API with Django REST Framework
- [ ] JWT authentication for API
- [ ] API documentation with Swagger/OpenAPI
- [ ] Webhook endpoints for SMS providers
- [ ] Game status API endpoints
- [ ] User management API
- [ ] Leaderboard API with pagination
- [ ] Game analytics API

### 📁 Expected Project Structure
```
onam_project/
├── .github/workflows/          # GitHub Actions (if needed)
├── .gitlab/                    # GitLab templates
├── apps/
│   ├── accounts/               # User management & phone verification
│   │   ├── migrations/
│   │   ├── templates/accounts/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── signals.py
│   │   ├── tasks.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── tests/
│   ├── core/                   # Homepage and common utilities
│   │   ├── templates/core/
│   │   ├── management/commands/
│   │   ├── templatetags/
│   │   └── ...
│   ├── games/                  # Treasure hunt logic
│   │   ├── templates/games/
│   │   ├── models.py           # Game, Level, UserProgress
│   │   ├── game_engine.py      # Game logic
│   │   └── ...
│   └── sms/                    # SMS service integration
│       ├── backends/           # Twilio, MessageBird backends
│       ├── models.py           # SMS logs, templates
│       └── ...
├── fixtures/                   # Sample data
├── logs/                      # Application logs
├── media/                     # User uploads
├── static/                    # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                 # Global templates
├── tests/                     # Project-wide tests
├── onam_project/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
├── .env.example
├── .gitignore
├── .gitlab-ci.yml
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── pyproject.toml
├── requirements.txt
└── setup.sh
```

### 🔧 Environment Variables Required
```bash
# Core Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/onam_db

# SMS Configuration
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token  
TWILIO_PHONE_NUMBER=+46701234567

# Alternative SMS
MESSAGEBIRD_ACCESS_KEY=your_messagebird_key
MESSAGEBIRD_ORIGINATOR=OnamApp

# Email (backup for password reset)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery & Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Game Configuration
TREASURE_HUNT_LEVELS=5
SMS_RATE_LIMIT_PER_HOUR=10
OTP_EXPIRY_MINUTES=5

# Security
CORS_ALLOWED_ORIGINS=http://localhost:3000
SECURE_SSL_REDIRECT=True

# Monitoring (Optional)
SENTRY_DSN=your_sentry_dsn
```

### 🎮 Game Flow Requirements
1. **User Registration**: Swedish phone (+46) → SMS OTP verification
2. **Game Start**: First clue sent via SMS after successful login
3. **Clue Progression**: User submits answer → validation → next clue via SMS
4. **Scoring System**: Points based on speed and accuracy
5. **Leaderboard**: Real-time rankings with user achievements
6. **Game Completion**: Final treasure location + celebration message

### 📱 SMS Message Templates
- **OTP Verification**: "Your Onam app verification code: {code}. Valid for 5 minutes."
- **Game Clue**: "Onam Clue #{level}: {clue_text}. Reply with your answer at {app_url}"
- **Correct Answer**: "🎉 Correct! You've unlocked level {next_level}. New clue coming soon!"
- **Wrong Answer**: "Not quite right. Hint: {hint}. Try again at {app_url}"
- **Game Complete**: "🌸 Congratulations! You've completed the Onam treasure hunt! Check your rank: {leaderboard_url}"

### 🎨 Kerala Cultural Elements to Include
- **Pookalam**: Flower carpet designs and significance
- **Sadhya**: Traditional feast with 20+ dishes description
- **Pulikali**: Tiger dance performances
- **Kathakali**: Classical dance drama
- **Thiruvathira**: Traditional dance
- **Vallamkali**: Snake boat races
- **King Mahabali**: Legend and significance
- **Onam Songs**: Traditional verses and meanings

### 🚀 Deployment Requirements
- [ ] Docker containers for web, db, redis, celery
- [ ] GitLab CI/CD with automated testing
- [ ] Staging and production environments
- [ ] Database migrations automation
- [ ] Static files collection and serving
- [ ] Health checks and monitoring
- [ ] Backup and recovery procedures
- [ ] SSL certificate configuration

### 📋 Admin Interface Requirements
- [ ] User management with phone verification status
- [ ] Game level management and clue editing
- [ ] SMS log viewing and analytics
- [ ] Leaderboard management
- [ ] System health dashboard
- [ ] Configuration management
- [ ] Bulk user operations
- [ ] Game statistics and reports

### 🎯 Success Criteria
- [ ] Users can register with Swedish phone numbers
- [ ] SMS OTP verification works reliably
- [ ] Game clues are delivered via SMS
- [ ] Answer submission and validation works
- [ ] Leaderboard updates in real-time
- [ ] Mobile-responsive design works on all devices
- [ ] All tests pass with >80% coverage
- [ ] Performance: Page load times < 2 seconds
- [ ] Security: Passes Django security checklist
- [ ] Deployment: Successful CI/CD pipeline

### 🌟 Additional Features (Nice to Have)
- [ ] Multi-language support (English, Swedish, Malayalam)
- [ ] Social media sharing of achievements
- [ ] Photo upload for Pookalam contests
- [ ] Push notifications for mobile
- [ ] Offline game progress caching
- [ ] Team-based treasure hunts
- [ ] Seasonal event variations
- [ ] Integration with Kerala tourism
- [ ] Recipe sharing for Onam dishes
- [ ] Virtual Pookalam creator tool

### 📞 Support & Documentation
- [ ] Comprehensive README with setup instructions
- [ ] API documentation with examples
- [ ] Deployment guide for different platforms
- [ ] Troubleshooting guide
- [ ] Contributing guidelines
- [ ] Code of conduct
- [ ] Security policy
- [ ] Privacy policy for SMS data

---

## 🌸 Cultural Authenticity Note
Please ensure all Onam-related content is culturally accurate and respectful. Consult Kerala cultural sources and include proper Malayalam terminology where appropriate. The app should celebrate the rich heritage of Kerala while being accessible to a Swedish audience.

**ഓണാശംസകൾ! (Happy Onam!)**

---

**Priority**: High  
**Estimated Effort**: 2-3 weeks  
**Target Audience**: Swedish residents interested in Kerala culture  
**Primary Language**: English (with cultural terms in Malayalam)
