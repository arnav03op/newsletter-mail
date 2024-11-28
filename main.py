import datetime 
import smtplib
import pandas as pd
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os


def send_email():
    print("Sending email...") 
    

    contacts = pd.read_csv("contacts.csv")
    
    
    with open("credentials.txt", "r") as f:
        email_password = f.read().strip()
    
    sender_email = "arnavgupta372002@gmail.com"  
    subject = "Monthly Newsletter"

    
    with open("email_template.txt", "r") as f:
        template = f.read()

    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()

    #
    server.starttls()
    #

    server.login(sender_email, email_password)

    
    log_file = open("logs/email_log.txt", "a")

    
    for index, contact in contacts.iterrows():
        name = contact['name']
        receiver_email = contact['email']

        # Personalize - not clear
        message = template.format(name=name)

        
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        # attachment wala part
        attachment_path = "attachments/sample.pdf"  
        try:
            attachment = open(attachment_path, "rb")
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=sample.pdf")
            msg.attach(part)
            attachment.close()
        except FileNotFoundError:
            print(f"Attachment not found: {attachment_path}")

        
        try:
            server.sendmail(sender_email, receiver_email, msg.as_string())
            log_file.write(f"Email sent to {name} ({receiver_email})\n")
            print(f"Email sent to {name} ({receiver_email})")
        except Exception as e:
            log_file.write(f"Failed to send email to {receiver_email}: {e}\n")
            print(f"Failed to send email to {receiver_email}: {e}")
    
    server.quit()
    log_file.close()
    print("All emails sent!")


# alter the date , for testing , but ideally 1st day of month hona chahiye
def send_email_if_first_of_month():
    today = datetime.date.today()
    print(f"Checking date: {today}") 
    if today.day == 29:  
        print("Triggering send_email()...")
        send_email()

# Schedule time accordingly
schedule.every().day.at("03:29").do(send_email_if_first_of_month)


# Run-scheduler 
if __name__ == "__main__":
    print("Email Scheduler Running...")
    while True:
        schedule.run_pending()
        time.sleep(1)


# will add more features in future such as backup and encryption




