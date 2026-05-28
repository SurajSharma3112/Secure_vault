PySecureVault

A full-stack, highly secure file encryption vault built with **FastAPI** and MySQL. It allows users to create accounts, securely upload files, and encrypt them using AES-256 encryption. Only authenticated users can decrypt and retrieve their original files.

Developed as a showcase-ready security architecture for **Novum Labs**.

Features

Secure User Authentication: Password hashing using `bcrypt` and secure session management via `itsdangerous`.
Military-Grade Encryption: Files are encrypted using the `cryptography` library (Fernet AES-256) upon upload.
Auto-Destruction of Originals: Original files are immediately deleted from the server once the encrypted `.enc` version is generated.
Modern UI/UX: A responsive, premium Glassmorphism design with intuitive dashboards and interactive hover effects.
Brute-Force Protection: Intelligent account lockout mechanism triggers after 3 consecutive failed login attempts.

🛠️ Tech Stack

Backend: FastAPI, Python
Database: MySQL, `mysql-connector-python`
Frontend: HTML5, CSS3, Jinja2 Templates
Security: `bcrypt`, `cryptography`

installation & Setup

1. Prerequisites
2. Python 3.8+ installed on your system.
  MySQL Server (XAMPP or standalone) running locally.

2. Clone the Repository
```bash
git clone [https://github.com/your-username/PySecureVault.git](https://github.com/your-username/PySecureVault.git)
cd PySecureVault
