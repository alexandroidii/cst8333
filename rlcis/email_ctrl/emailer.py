# send confirmation emails 
# using smtplib



import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

email = 'cst3333@lange.ca'
password = input('Enter you password ')
send_to_email = 'Robert@lange.ca'
subject = 'This is the subject' # The subject line
message = 'This is my message to test in python'

server = 'ns.lange.ca'
port = 25

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = send_to_email
msg['Subject'] = subject

 # Attach the message to the MIMEMultipart object
msg.attach(MIMEText(message, 'plain'))

server = smtplib.SMTP(server, port)
server.starttls()
server.login(email, password)
text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
server.sendmail(email, send_to_email, text)
server.quit()