# 🔐 Campus Pulse Authentication System

Complete user authentication and profile management system for Campus Pulse.

## Features

### 🎓 UFL Email Authentication
- **Email Validation**: Only accepts @ufl.edu email addresses
- **Secure Passwords**: Enforced strong password requirements
- **Password Hashing**: SHA-256 encryption for all passwords

### 👤 Student Profiles
- **Profile Information**:
  - Full Name
  - Bio (up to 500 characters)
  - Major
  - Year (Freshman, Sophomore, Junior, Senior, Graduate)
  - Interests (comma-separated tags)

### 🔒 Privacy Controls
- **Profile Visibility Options**:
  - **Public**: Visible to all students in the directory
  - **Private**: Only visible to you

- **Directory Settings**:
  - Show/hide profile in student directory
  - Email notification preferences

### 🔍 Student Discovery
- **Search Features**:
  - Search by name or major
  - Browse public student profiles
  - Student directory with 20+ profiles per page

## How to Use

### Sign Up

1. Navigate to **👤 Profile** in the top navigation
2. Click the **"Sign Up"** tab
3. Fill in required information:
   - **UFL Email** (must be @ufl.edu)
   - **Password** (min 8 chars, 1 uppercase, 1 lowercase, 1 number)
   - **Full Name**
4. Add optional information:
   - Bio
   - Major
   - Year
   - Interests
5. Choose profile visibility:
   - 🌍 **Public** - Visible to all students
   - 🔒 **Private** - Only you can see
6. Agree to Terms of Service
7. Click **"Create Account"**

### Sign In

1. Navigate to **👤 Profile**
2. Click the **"Sign In"** tab
3. Enter your UFL email and password
4. Click **"Sign In"**

### Managing Your Profile

Once signed in, you can:

1. **View Profile** - See your complete profile
2. **Edit Profile** - Update your information:
   - Name, bio, major, year
   - Interests
   - Privacy settings
3. **Find Students** - Search and browse other students

### Privacy Settings

**Public Profile:**
- Visible in student directory
- Other students can find you by search
- Shows name, major, year, bio, interests

**Private Profile:**
- Not visible in student directory
- Cannot be found by other students
- Only you can see your information

## Password Requirements

For security, passwords must:
- Be at least 8 characters long
- Contain at least one uppercase letter (A-Z)
- Contain at least one lowercase letter (a-z)
- Contain at least one number (0-9)

Example valid passwords:
- `Gator2024!`
- `UFL_Student1`
- `GoGators25`

## Database

The authentication system uses **SQLite** for data storage:

- **File**: `campus_pulse_users.db`
- **Tables**:
  - `users` - User accounts and profiles
  - `user_settings` - Privacy and notification settings

### Security Features

✅ **Password Hashing**: All passwords encrypted with SHA-256
✅ **Email Validation**: Only UFL emails accepted
✅ **SQL Injection Protection**: Parameterized queries
✅ **Session Management**: Streamlit session state
✅ **Privacy Controls**: User-controlled visibility

## API Reference

### AuthManager Class

```python
from auth.auth_manager import AuthManager

# Initialize
auth = AuthManager()

# Sign up
success, message = auth.sign_up(
    email="student@ufl.edu",
    password="SecurePass123",
    full_name="John Doe",
    bio="Computer Science student",
    profile_visibility="public"
)

# Sign in
success, user_data, message = auth.sign_in(
    email="student@ufl.edu",
    password="SecurePass123"
)

# Update profile
success, message = auth.update_profile(
    user_id=1,
    updates={
        'bio': 'New bio',
        'major': 'Computer Science',
        'profile_visibility': 'private'
    }
)

# Search students
results = auth.search_students("Computer Science")

# Get public profiles
profiles = auth.get_public_profiles(limit=20)
```

## Data Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| email | TEXT | UFL email (unique) |
| password_hash | TEXT | SHA-256 hashed password |
| full_name | TEXT | Student's full name |
| bio | TEXT | Profile bio |
| profile_visibility | TEXT | 'public' or 'private' |
| major | TEXT | Major/department |
| year | TEXT | Academic year |
| interests | TEXT | Comma-separated interests |
| created_at | TIMESTAMP | Account creation date |
| last_login | TIMESTAMP | Last login timestamp |

### User Settings Table

| Column | Type | Description |
|--------|------|-------------|
| user_id | INTEGER | Foreign key to users |
| email_notifications | BOOLEAN | Email notification preference |
| show_in_directory | BOOLEAN | Show in student directory |
| theme | TEXT | UI theme preference |

## Integration with Campus Pulse

### Personalized Features

When signed in, users get:
- ✅ **Event Creation** - Tagged with creator name
- ✅ **Saved Locations** - Personal location bookmarks
- ✅ **Activity Stats** - Events created, locations saved
- ✅ **Profile Badge** - Name shown in navigation

### Event Attribution

User-created events are marked with:
- ⭐ **"Your Event"** gold badge
- Creator name stored
- Visible only to creator in event list

## Security Best Practices

1. **Never share your password**
2. **Use a unique password** for Campus Pulse
3. **Log out** when using shared computers
4. **Review privacy settings** regularly
5. **Report suspicious activity** immediately

## Troubleshooting

### Can't Sign Up

**Problem**: "Please use a valid UFL email address"
- **Solution**: Make sure email ends with `@ufl.edu`

**Problem**: "Password does not meet requirements"
- **Solution**: Check password has 8+ chars, uppercase, lowercase, and number

### Can't Sign In

**Problem**: "Invalid email or password"
- **Solution**: Double-check email and password
- **Solution**: Make sure caps lock is off

### Profile Not Showing

**Problem**: "I can't find other students"
- **Solution**: Only **public** profiles are visible
- **Solution**: Student must have "Show in directory" enabled

### Database Issues

**Problem**: Database errors on startup
- **Solution**: Database is created automatically on first run
- **Solution**: Check file permissions in app directory

## Privacy Policy

Campus Pulse respects your privacy:

✅ **No data sharing** - Your data stays on the server
✅ **User control** - You control visibility settings
✅ **Secure storage** - Passwords are hashed
✅ **Optional directory** - Choose to be listed or not

## Support

For authentication issues:
1. Check this guide first
2. Review error messages carefully
3. Try logging out and back in
4. Contact support if issues persist

---

**Built with 🔒 for UFL student privacy and security**

🐊 Go Gators! 🐊
