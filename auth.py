import sqlite3
import hashlib
import secrets
from datetime import datetime

DB_PATH = "users.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates the users + reminders tables if they don't already exist,
    and safely adds new columns to `users` if this is an older database.
    Safe to call every time the app starts.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT,
            email TEXT,
            age INTEGER,
            gender TEXT,
            height TEXT,
            weight TEXT,
            blood_group TEXT,
            location TEXT,
            emergency_contact TEXT,
            medical_conditions TEXT,
            allergies TEXT,
            created_at TEXT
        )
    """)

    # ---- Safe migration for existing databases created before this update ----
    existing_columns = [row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()]

    if "medical_conditions" not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN medical_conditions TEXT")

    if "allergies" not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN allergies TEXT")

    conn.commit()

    # ---- Reminders table ----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            title TEXT NOT NULL,
            reminder_type TEXT,
            reminder_date TEXT,
            reminder_time TEXT,
            notes TEXT,
            is_done INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password, salt=None):
    """
    Hashes a password with a salt using SHA-256.
    If no salt is given, a new random one is generated (used at signup).
    """

    if salt is None:
        salt = secrets.token_hex(16)

    pwd_hash = hashlib.sha256((salt + password).encode()).hexdigest()

    return pwd_hash, salt


def create_user(username, password, email=""):
    """
    Creates a new user account. Returns (success, message).
    """

    username = username.strip()

    conn = get_connection()
    cursor = conn.cursor()

    existing = cursor.execute(
        "SELECT id FROM users WHERE username = ?", (username,)
    ).fetchone()

    if existing:
        conn.close()
        return False, "Username already exists. Please choose another."

    pwd_hash, salt = hash_password(password)

    cursor.execute("""
        INSERT INTO users (username, password_hash, salt, email, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (username, pwd_hash, salt, email.strip(), datetime.now().isoformat()))

    conn.commit()
    conn.close()

    return True, "Account created successfully."


def verify_login(username, password):
    """
    Checks username/password combination.
    Returns (success, user_dict_or_None).
    """

    conn = get_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username.strip(),)
    ).fetchone()

    conn.close()

    if user is None:
        return False, None

    pwd_hash, _ = hash_password(password, user["salt"])

    if pwd_hash == user["password_hash"]:
        return True, dict(user)

    return False, None


def get_user_by_username(username):
    """
    Fetches the full profile row for a username as a dict.
    """

    conn = get_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

    conn.close()

    return dict(user) if user else None


def update_profile(username, profile_data):
    """
    Updates the editable profile fields for a user.
    profile_data is a dict with any of: full_name, email, age, gender,
    height, weight, blood_group, location, emergency_contact,
    medical_conditions, allergies.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET full_name = ?,
            email = ?,
            age = ?,
            gender = ?,
            height = ?,
            weight = ?,
            blood_group = ?,
            location = ?,
            emergency_contact = ?,
            medical_conditions = ?,
            allergies = ?
        WHERE username = ?
    """, (
        profile_data.get("full_name", ""),
        profile_data.get("email", ""),
        profile_data.get("age"),
        profile_data.get("gender", ""),
        profile_data.get("height", ""),
        profile_data.get("weight", ""),
        profile_data.get("blood_group", ""),
        profile_data.get("location", ""),
        profile_data.get("emergency_contact", ""),
        profile_data.get("medical_conditions", ""),
        profile_data.get("allergies", ""),
        username
    ))

    conn.commit()
    conn.close()


def change_password(username, old_password, new_password):
    """
    Verifies the old password, then sets a new one.
    Returns (success, message).
    """

    success, user = verify_login(username, old_password)

    if not success:
        return False, "Current password is incorrect."

    conn = get_connection()
    cursor = conn.cursor()

    pwd_hash, salt = hash_password(new_password)

    cursor.execute(
        "UPDATE users SET password_hash = ?, salt = ? WHERE username = ?",
        (pwd_hash, salt, username)
    )

    conn.commit()
    conn.close()

    return True, "Password changed successfully."


def build_profile_context(user):
    """
    Turns a user's profile dict into a short text summary that can be
    injected into AI prompts, so responses can be personalized.
    Returns "" if there isn't enough profile info to matter.
    """

    if not user:
        return ""

    parts = []

    if user.get("age"):
        parts.append(f"Age: {user['age']}")

    if user.get("gender"):
        parts.append(f"Gender: {user['gender']}")

    if user.get("blood_group"):
        parts.append(f"Blood Group: {user['blood_group']}")

    if user.get("height"):
        parts.append(f"Height: {user['height']}")

    if user.get("weight"):
        parts.append(f"Weight: {user['weight']}")

    if user.get("medical_conditions"):
        parts.append(f"Known Medical Conditions: {user['medical_conditions']}")

    if user.get("allergies"):
        parts.append(f"Known Allergies: {user['allergies']}")

    if not parts:
        return ""

    return "Patient Profile (for context only — use to tailor tone/relevance, do not repeat verbatim unless useful):\n" + "\n".join(parts)


# ---------------------------------------------------
# Reminders
# ---------------------------------------------------

def add_reminder(username, title, reminder_type, reminder_date, reminder_time, notes=""):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders (username, title, reminder_type, reminder_date, reminder_time, notes, is_done, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 0, ?)
    """, (
        username,
        title,
        reminder_type,
        str(reminder_date),
        str(reminder_time),
        notes,
        datetime.now().isoformat()
    ))

    conn.commit()
    conn.close()


def get_reminders(username):

    conn = get_connection()
    cursor = conn.cursor()

    rows = cursor.execute(
        "SELECT * FROM reminders WHERE username = ? ORDER BY reminder_date ASC, reminder_time ASC",
        (username,)
    ).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def delete_reminder(reminder_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reminders WHERE id = ?", (reminder_id,))

    conn.commit()
    conn.close()


def toggle_reminder_done(reminder_id, is_done):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE reminders SET is_done = ? WHERE id = ?",
        (1 if is_done else 0, reminder_id)
    )

    conn.commit()
    conn.close()