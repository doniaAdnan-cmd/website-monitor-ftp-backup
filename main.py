import os
import shutil
import smtplib
import getpass
import logging
from datetime import datetime
from ftplib import FTP
from email.message import EmailMessage
import requests

# ---------------- PROJECT SETTINGS ----------------
WEBSITE_URL = "http://localhost/mywebsite/index.html"
WEBSITE_FOLDER = r"C:\xampp\htdocs\mywebsite" 
BACKUP_FOLDER = "backups"
FTP_HOST = "127.0.0.1"
FTP_PORT = 2121

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
# --------------------------------------------------

def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/monitor.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def send_email(sender, app_password, subject, body):
    """Send an email from the student's Gmail to the same Gmail account."""
    message = EmailMessage()
    message["From"] = sender
    message["To"] = sender
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(sender, app_password)
        server.send_message(message)

def check_website(sender, app_password):
    """Check whether the local Apache page is available."""
    try:
        response = requests.get(WEBSITE_URL, timeout=5)
        if response.status_code == 200:
            print("Website Status: UP")
            print("HTTP Status Code:", response.status_code)
            logging.info("Website is UP. HTTP %s", response.status_code)
        else:
            reason = f"HTTP status code: {response.status_code}"
            print("Website Status: DOWN")
            print("Reason:", reason)
            logging.warning("Website is DOWN. %s", reason)
            send_email(sender, app_password,
                       "ALERT: Local Website Is Down",
                       f"The local website is not responding.\n\n"
                       f"URL: {WEBSITE_URL}\n"
                       f"Time: {datetime.now()}\n"
                       f"Reason: {reason}")
            print("Gmail alert sent.")
    except requests.RequestException as error:
        print("Website Status: DOWN")
        print("Reason:", error)
        logging.error("Website check failed: %s", error)
        send_email(sender, app_password,
                   "ALERT: Local Website Is Down",
                   f"The local website is not responding.\n\n"
                   f"URL: {WEBSITE_URL}\n"
                   f"Time: {datetime.now()}\n"
                   f"Reason: {error}")
        print("Gmail alert sent.")

def create_and_upload_backup(sender, app_password):
    """Create a ZIP backup, then upload it to the local FTP server."""
    if not os.path.isdir(WEBSITE_FOLDER):
        print("Website folder was not found.")
        return

    os.makedirs(BACKUP_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_base_name = os.path.join(BACKUP_FOLDER, f"backup_{timestamp}")

    # Create local ZIP backup
    zip_path = shutil.make_archive(zip_base_name, "zip", WEBSITE_FOLDER)
    print("Local ZIP backup created:", zip_path)
    logging.info("ZIP backup created: %s", zip_path)

    # Upload ZIP file to local FTP server
    try:
        ftp = FTP()
        ftp.connect(FTP_HOST, FTP_PORT, timeout=10)
        ftp.login()  # Anonymous login for local pyftpdlib test server
        with open(zip_path, "rb") as backup_file:
            ftp.storbinary(f"STOR {os.path.basename(zip_path)}", backup_file)
        ftp.quit()
        print("FTP upload successful.")
        logging.info("FTP upload successful: %s", zip_path)

        send_email(sender, app_password,
                   "BACKUP SUCCESS: FTP Upload Completed",
                   f"Website backup was created and uploaded successfully.\n\n"
                   f"Backup file: {os.path.basename(zip_path)}\n"
                   f"Local backup folder: {BACKUP_FOLDER}\n"
                   f"FTP destination: {FTP_HOST}:{FTP_PORT}\n"
                   f"Time: {datetime.now()}")
        print("Gmail backup confirmation sent.")
    except Exception as error:
        print("FTP upload failed:", error)
        logging.error("FTP upload failed: %s", error)

def main():
    setup_logging()
    print("Local Website Monitor and FTP Backup")
    sender = input("Enter your Gmail address: ").strip()
    app_password = getpass.getpass("Enter Gmail App Password: ")

    while True:
        print("\n1. Check Website Status")
        print("2. Create ZIP Backup and Upload to Local FTP")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            check_website(sender, app_password)
        elif choice == "2":
            create_and_upload_backup(sender, app_password)
        elif choice == "3":
            print("Program closed.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

