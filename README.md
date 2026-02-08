# Mass Email Sender Web App

A locally-run, authenticated bulk email sender built with FastAPI, Jinja2, and SMTP. This application allows an authorized user to upload a CSV of recipients, select an email template, customize campaign-level metadata (subject, sender name, footer position), preview the rendered email, and send emails in bulk while logging results to a local SQLite database.

This project is designed to run locally via the terminal and is not intended for deployment at this stage.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Authentication](#authentication)
- [Bulk Email Workflow](#bulk-email-workflow)
- [Email Templates](#email-templates)
  - [Required Template Fields](#required-template-fields)
  - [Preview vs Send Mode](#preview-vs-send-mode)
  - [Adding a New Email Template](#adding-a-new-email-template)
- [CSV Format Requirements](#csv-format-requirements)
- [Logs](#logs)
- [Extending the System](#extending-the-system)
- [Known Limitations](#known-limitations)
- [Author](#author)

---

## Features

- Login-protected dashboard
- Upload CSV recipient lists
- Campaign-based sending (subject, sender, footer position)
- HTML email templates using Jinja2
- Inline image support via CID
- Email preview inside an iframe
- Background email sending (non-blocking)
- SQLite email logs (sent / failed)
- Modular, extensible architecture

---

## Tech Stack

- Python 3.10+
- FastAPI
- Jinja2
- SQLite
- SMTP (Gmail / Outlook / etc.)
- passlib + bcrypt (authentication)
- Starlette sessions

---

## Project Structure

```
MassEmailSenderWebApp/
│
├── app/
│   ├── main.py                      # FastAPI app entry point
│   │
│   ├── auth/
│   │   ├── dependencies.py          # Login guards
│   │   └── auth.py                  # Login/logout routes
│   │
│   ├── routes/
│   │   ├── bulk.py                  # Bulk upload, preview, send
│   │   ├── preview.py               # Email iframe preview
│   │   └── logs.py                  # Email log viewer
│   │
│   ├── emailer/
│   │   ├── send_email.py            # SMTP + template rendering
│   │   └── templates.py             # Email template registry
│   │
│   ├── services/
│   │   └── bulk_sender.py           # Background bulk send task
│   │
│   ├── db/
│   │   └── database.py              # SQLite connection + logging
│   │
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── bulk_preview.html
│   │   ├── send_confirmation.html
│   │   ├── logs.html
│   │   └── emails/
│   │       └── ga_invitation_email.html
│   │
│   └── static/
│       ├── BigHeader.png
│       └── ICPEPLogo.png
│
├── .env                             # SMTP credentials (not committed)
├── requirements.txt
└── README.md
```

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <repo-url>
cd MassEmailSenderWebApp
```

### 2. Create and activate a virtual environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
SECRET_KEY=some-random-secret
```

**Note:** If using Gmail, you must use an App Password, not your regular account password.

---

## Running the Application

Run the server locally from the project root:

```bash
uvicorn app.main:app --reload
```

Then open your browser at:

```
http://127.0.0.1:8000
```

---

## Authentication

- The app is protected by session-based authentication
- All routes except login require authentication
- Credentials are currently stored locally (MVP setup)

---

## Bulk Email Workflow

1. Log in
2. Go to the dashboard
3. Select an email template
4. Enter:
   - Email subject
   - Sender name
   - Footer position/title
5. Upload a CSV file
6. Preview recipients and email content
7. Confirm send
8. Emails are sent in the background
9. Results are logged to SQLite

---

## Email Templates

Email templates are standard Jinja2 HTML files located in:

```
app/templates/emails/
```

### Required Template Fields

Every email template must support the following variables:

- `{{ recipient_name }}`
- `{{ sender_name }}`
- `{{ position }}`
- `{{ preview_mode }}`

If any of these are missing during render, the template may display blank content.

### Preview vs Send Mode

Templates must handle two modes:

```jinja
{% if preview_mode %}
  <img src="/static/BigHeader.png">
{% else %}
  <img src="cid:header_image">
{% endif %}
```

This ensures:

- Browser preview works
- Email clients render inline images correctly

### Adding a New Email Template

1. Create a new HTML file in:

   ```
   app/templates/emails/
   ```

2. Register it in:
   ```python
   # app/emailer/templates.py
   EMAIL_TEMPLATES = {
       "invitation": {
           "label": "Partnership Invitation",
           "file": "ga_invitation_email.html",
       },
   }
   ```

The template will automatically appear in the dashboard dropdown.

---

## CSV Format Requirements

The uploaded CSV must contain at least:

```csv
email,name
test@example.com,John Doe
```

- `email` is required
- `name` is optional (defaults to "Partner")

---

## Logs

Email logs are stored in a local SQLite database and include:

- Recipient email
- Recipient name
- Status (sent / failed)
- Error message (if any)
- Timestamp

Accessible via the Logs page in the UI.

---

## Extending the System

To add a new campaign-level field (example: phone number, department):

You must update all of the following:

1. Dashboard form (`dashboard.html`)
2. `preview_bulk` route (`bulk.py`)
3. Session storage (`campaign` dict)
4. Preview renderer (`preview.py`)
5. Bulk sender (`bulk_sender.py`)
6. Email renderer (`send_email.py`)
7. Email template (Jinja variable)

Missing any step will result in empty values or validation errors.

---

## Known Limitations

- Single-user (MVP)
- In-memory recipient storage
- No job progress tracking
- No retry queue
- No deployment configuration

These are intentional for local use.

---

## Author

**Charles Chang-il Jung**  
Vice President Internal  
Institute of Computer Engineers of the Philippines – Student Edition  
Pamantasan ng Lungsod ng Maynila Chapter

---

## License

This project is intended for educational and organizational use.
