import os
import smtplib
import zipfile
import shutil
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Define your email details
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USERNAME = "techsupport@happyecom.com"
SMTP_PASSWORD = "Cuk08671"
filepaths = [
    "Flipkart_Brand_report_MTD.xlsx",
    "Flipkart_Brand_report_YTD.xlsx",
]
# Recipients
toaddr = ["dibyajyoti49dey@gmail.com", "sameera@acumensa.co"]
fromaddr = SMTP_USERNAME
all_recipients = toaddr

def zip_files(file_paths, zip_name):
    """Zip the given list of files into a single zip file."""
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_paths:
            if os.path.exists(file):
                zipf.write(file, os.path.basename(file))
            else:
                print(f"File not found: {file}")

def compress_zip_file(zip_name, compressed_name):
    """Compress the zip file to reduce its size."""
    abs_zip_name = os.path.abspath(zip_name)
    root_dir = os.path.dirname(abs_zip_name)
    base_dir = os.path.basename(abs_zip_name)
    if not os.path.exists(root_dir):
        print(f"Directory not found: {root_dir}")
        return
    shutil.make_archive(compressed_name, 'zip', root_dir=root_dir, base_dir=base_dir)

def attach_zip_file(email_msg, zip_path):
    """Attach a zip file to the given email message."""
    with open(zip_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename={os.path.basename(zip_path)}"
        )
        email_msg.attach(part)

# Create the zip file
zip_name = "flipkart_reports.zip"
zip_files(filepaths, zip_name)

# Compress the zip file
compressed_name = "flipkart_reports_compressed"
compress_zip_file(zip_name, compressed_name)

# Create the MIMEText object to represent your email
print("Constructing email...")
msg = MIMEMultipart()
msg["From"] = fromaddr
msg["To"] = ", ".join(toaddr)
msg["Subject"] = "Order Payment Report"

# Attach the compressed zip file
attach_zip_file(msg, f"{compressed_name}.zip")

print("Sending email...")
# Send the email
server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
server.starttls()
server.login(SMTP_USERNAME, SMTP_PASSWORD)
server.sendmail(fromaddr, all_recipients, msg.as_string())
server.quit()
print("Email sent successfully.")