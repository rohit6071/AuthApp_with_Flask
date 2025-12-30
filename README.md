# AuthApp_with_Flask
Flask JWT Authentication System 🔐

A secure, production-ready user authentication system built with Flask featuring JWT tokens, bcrypt password hashing, and SQLAlchemy ORM with both partial and full user profile updates.

🌟 Features

🔐 Authentication & Security

JWT Token-based Authentication with 1-hour expiration
Bcrypt password hashing for secure storage
HTTP-only cookies for JWT storage
Login decorator for route protection
CSRF protection via SameSite cookies

👤 User Management

User Registration with validation rules
Login/Logout functionality
Partial Updates (PATCH) - Update specific fields
Full Updates (PUT) - Update all fields at once
User isolation - Users can only update their own profiles

🗄️ Database & Backend

SQLAlchemy ORM with SQLite database
Session management with SQLAlchemy sessions
Automatic JWT token refresh on username updates
Form validation with comprehensive rules

🎨 Frontend & UI

Responsive design with modern CSS
Flash messages for user feedback
Font Awesome icons throughout
Clean, intuitive interface
Update forms with clear differentiation

📋 Prerequisites

Python 3.8 or higher
pip (Python package manager)
Git (for version control)

🚀 Installation & Setup

1. Clone the Repository

bash
git clone https://github.com/yourusername/flask-jwt-auth.git
cd flask-jwt-auth

2. Create Virtual Environment

bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

bash
pip install -r requirements.txt

4. Environment Configuration

Create a .env file in the root directory:

env
FLASK_SECRET_KEY="your-flask-secret-key-here"
JWT_SECRET_KEY="your-jwt-secret-key-here"
JWT_ALGORITHM="HS256"

5. Initialize Database

python
python -c "
from models import Base, engine
Base.metadata.create_all(engine)
print('Database initialized successfully!')
"

6. Run the Application

bash
python app.py
The application will be available at http://localhost:5000

📁 Project Structure

text
flask-jwt-auth/
│
├── app.py                    # Main Flask application
├── models.py                 # SQLAlchemy models and database setup
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .gitignore               # Git ignore file
│
├── static/
│   └── css/
│       └── styles.css       # Main stylesheet
│
├── templates/
│   ├── base.html            # Base template with navigation
│   ├── home.html            # Home page with update forms
│   ├── login.html           # Login page
│   └── register.html        # Registration page
│
└── README.md                # This documentation

🔧 API Endpoints

Public Routes (No Authentication Required)

Home Page

Method: GET
Endpoint: /
Description: Landing page with system overview
Access: Public
User Registration

Method: GET (form) / POST (submit)
Endpoint: /register
Description: Create new user account with validation
Access: Public
Validation Rules:

Username: Start with letter, alphanumeric only
Email: Valid format required
Password: Minimum 6 characters, must match confirmation
User Login

Method: GET (form) / POST (submit)
Endpoint: /login
Description: Authenticate user and receive JWT token
Access: Public
Response: Sets HTTP-only JWT cookie on success
Protected Routes (Authentication Required)

User Logout

Method: POST
Endpoint: /logout
Description: Invalidate JWT token and log out user
Access: Authenticated users only
Effect: Clears JWT cookie
Partial User Update

Method: PATCH / POST (with _method=PATCH)
Endpoint: /partial/<username>
Description: Update specific user fields (partial update)
Access: Only the authenticated user matching the username
Features:

Update username, email, or password individually
Fields are optional
Returns updated JWT token if username changes
Full User Update

Method: PUT / POST (with _method=PUT)
Endpoint: /update/<username>
Description: Update all user fields at once (full update)
Access: Only the authenticated user matching the username
Features:

All fields (username, email, password) are required
Complete profile replacement
Returns updated JWT token

📝 Usage Examples

Web Browser Usage 🌐

1. User Registration

Visit: http://localhost:5000/register
Fill the form:

Username: john (starts with letter, alphanumeric)
Email: john@example.com
Password: secure123 (min 6 characters)
Confirm Password: secure123
Click: "Create Account" button
Result: Account created → Redirected to login page
2. User Login

Visit: http://localhost:5000/login
Fill the form:

Username: john
Password: secure123
Click: "Login to Account" button
Result: JWT token stored in cookies → Redirected to home page
3. View Profile (After Login)

Visit: http://localhost:5000
See: Welcome message with your username
View: Account information and update forms
4. Partial Profile Update

On Home Page, fill Partial Update form:

text
Username: (leave blank to keep current)
Email: newemail@example.com
Password: (leave blank to keep current)
Click: "Update Selected Fields" button
Result: Email updated successfully
5. Full Profile Update

On Home Page, fill Full Update form:

text
Username: johndoe
Email: johndoe@example.com
Password: newpassword123
Click: "Update All Fields" button
Result: All profile details updated, JWT token refreshed
6. User Logout

Click: Logout button in navigation bar
Result: JWT token cleared → Redirected to home page as guest

🔐 Security Features

JWT Token Implementation

Tokens expire after 1 hour
Stored in HTTP-only cookies
Automatic validation on protected routes
Token refresh on username changes
Password Security

Bcrypt hashing with salt
Minimum 6 character requirement
Password confirmation on registration
Input Validation

Username rules: alphanumeric, starts with letter
Email format validation
Unique username and email checks
XSS protection through template escaping
🎨 Frontend Features

Responsive Design

Mobile-friendly navigation
Flexible grid layouts
Adaptive form designs
User Interface

Home Page: Welcome message, user info, update forms
Login Page: Clean form with security features display
Register Page: Comprehensive form with rules
Navigation: Dynamic based on login status
Update Forms

Partial Update Form: Update any individual field
Full Update Form: Update all fields at once
Visual feedback: Success/error messages
Form validation: Client-side and server-side

🗄️ Database Schema

sql
CREATE TABLE users_app (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL
);

🚀 Deployment

For Development

bash
python app.py

For Production

bash
# Using Gunicorn (install first: pip install gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Or using Waitress (Windows)
pip install waitress
waitress-serve --port=5000 app:app
📦 Dependencies

Core Dependencies

bcrypt==5.0.0
blinker==1.9.0
click==8.3.1
Flask==3.1.2
Flask-Bcrypt==1.0.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
PyJWT==2.10.1
python-dotenv==1.2.1
SQLAlchemy==2.0.45
typing_extensions==4.15.0
Werkzeug==3.1.4

Development Dependencies

Font Awesome: Icons
CSS3: Modern styling
HTML5: Semantic markup
🔍 Troubleshooting

Common Issues

ModuleNotFoundError: Ensure virtual environment is activated
Database errors: Run database initialization script
JWT errors: Check .env file for secret keys
CSS not loading: Check static file paths
Solutions

bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Reinitialize database
rm database.db
python -c "from models import Base, engine; Base.metadata.create_all(engine)"

# Check environment variables
python -c "import os; print('FLASK_SECRET_KEY' in os.environ)"





