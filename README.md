
# Eyres Staff Software

A staff management web application built with Django, designed to securely register and manage users, with administrator approval and email-based notifications via SendGrid.

---

## 🚀 Features

- **Custom User Registration**:
  - Users can sign up with full name, username, and email.
  - Users are initially marked as *inactive* and cannot log in until approved.

- **Pending Approval Page**:
  - After registration, users are redirected to a custom **"Account Pending Approval"** page.
  - This page includes a **"Request Activation"** button.

- **Admin Notification via Email (SendGrid)**:
  - When a user clicks the "Request Activation" button, an email is sent to the admin(s) requesting approval.
  - Emails are sent using the **SendGrid API**.
  - Admin receives the user's details in the email (name, email, username).

- **Environment-Based Configuration**:
  - `.env` file stores sensitive info (like `SENDGRID_API_KEY`, admin email list, etc.).
  - Uses `python-dotenv` to securely load environment variables.

- **Email Sandbox Mode Warning (Resolved)**:
  - SendGrid was initially in sandbox mode; this has been resolved.
  - Emails now send from user's registered email as the `From` address.

---

## 📦 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/your-username/eyres-staff-software.git
   cd eyres-staff-software
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up `.env` file**:
   Create a `.env` file in the project root with the following:
   ```env
   SENDGRID_API_KEY=your_sendgrid_api_key
   DEFAULT_FROM_EMAIL=no-reply@yourdomain.com
   ADMIN_EMAILS=admin1@example.com,admin2@example.com
   ```

5. **Run migrations and start server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## 🛠️ Admin Approval

To approve a user:
- Log in to the Django admin dashboard at `/admin`.
- Find the user under **Accounts > Custom Users**.
- Set `is_active = True` and save.

---

## 📝 Requirements

- Python 3.8+
- Django 5.2.6
- SendGrid
- python-dotenv

---

## 📄 License

This project is for internal organizational use at **Eyres**.

---
