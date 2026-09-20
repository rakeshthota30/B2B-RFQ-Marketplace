# Mini B2B RFQ Marketplace

A simple B2B Request for Quotation marketplace with two roles: Buyer and Supplier.

## Features

### Buyer
- Register/login
- Create RFQs
- Edit RFQs
- Delete/manage RFQs
- View submitted RFQs
- View supplier quotations

### Supplier
- Register/login
- Browse open RFQs
- Search RFQs
- Filter by delivery location
- View RFQ details
- Submit one quotation per RFQ
- View submitted quotations

## Technology Stack

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- PyMySQL
- HTML
- CSS
- JavaScript
- Bootstrap

## Project Structure

```text
rfq_marketplace/
├── app.py
├── config.py
├── extensions.py
├── requirements.txt
├── .env
├── models/
├── routes/
├── templates/
├── static/
└── database/
```

## Local Setup

### 1. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install packages

```bash
pip install -r requirements.txt
```

### 3. Create the database

Open MySQL:

```sql
CREATE DATABASE rfq_marketplace;
```

The application will create its tables automatically on first run.

### 4. Create `.env`

Copy `.env.example` to `.env` and update:

```text
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/rfq_marketplace
```

### 5. Run

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Architecture

Browser -> Flask routes -> SQLAlchemy models -> MySQL

Authentication uses Flask sessions. Passwords are stored as secure hashes using Werkzeug.

## Security

- Password hashing
- Session-based authentication
- Role-based authorization
- Database constraints
- Input validation
- Environment variables for secrets
- Supplier quotation uniqueness per RFQ

## Assumptions / Limitations

- One supplier can submit one quotation for each RFQ.
- No payment system is included.
- No real-time notifications are included.
- No complex auction/bidding mechanism is included.
- Admin functionality is outside the current scope.
- For production deployment, use HTTPS, a strong secret key, secure cookie settings, and a managed database.

## Deployment

The project can be deployed to a Python-compatible service such as Render. Configure the production database connection and environment variables in the hosting provider.

Example production start command:

```bash
gunicorn app:app
```
