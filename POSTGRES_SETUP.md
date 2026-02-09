# PostgreSQL Setup Guide

## 📋 Overview
The application now uses **PostgreSQL** instead of SQLite for user authentication.

## 🔧 Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment variable management

### 2. Configure Database Credentials

**Copy the example file:**
```bash
copy .env.example .env
```

**Edit `.env` file** with your PostgreSQL credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=kandle_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 3. Create PostgreSQL Database

Connect to PostgreSQL and create the database:
```sql
CREATE DATABASE kandle_db;
```

### 4. Run the Application

The app will automatically:
- Create the `users` table
- Add a default admin user: `admin` / `kandle2024`

```bash
streamlit run app.py
```

## 🌐 Cloud PostgreSQL Options

### Option 1: Neon (Recommended - Free Tier)
1. Visit [neon.tech](https://neon.tech)
2. Create free account
3. Create new project
4. Copy connection string to `.env`

### Option 2: Supabase
1. Visit [supabase.com](https://supabase.com)
2. Create new project
3. Get connection details from Settings → Database

### Option 3: ElephantSQL
1. Visit [elephantsql.com](https://www.elephantsql.com)
2. Create free instance
3. Copy connection URL

## 🔐 Security Notes

- ✅ `.env` file is **NOT** committed to git (add to `.gitignore`)
- ✅ Uses connection pooling for better performance
- ✅ Passwords are hashed with SHA-256
- ✅ Environment variables keep credentials secure

## 📊 Database Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Default Login

- **Username:** `admin`
- **Password:** `kandle2024`

Change this after first login!
