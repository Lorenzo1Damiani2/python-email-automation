import functions_framework
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime


@functions_framework.http
def hello_http(request):
  
  try:
      df = pd.read_csv('data_with_dates.csv', delimiter='\t')
  except pd.errors.ParserError as e:
      return f"Error reading CSV file: {e}", 400

  df["date"] = pd.to_datetime(df["date"])

  # Prepare email content
  # Extract the word of the day and its meaning
  today = datetime.today().date()
  word_of_the_day_row = df[df['date'].dt.date == today]

  if not word_of_the_day_row.empty:
      word_of_the_day = word_of_the_day_row['catalan'].values[0]
      meaning = word_of_the_day_row['english'].values[0]
  else:
      word_of_the_day = None
      meaning = None

  # Display the variables
  print(f"Word of the Day (Catalan): {word_of_the_day}")
  print(f"Meaning (English): {meaning}")

  email_content = f"Word of the Day: {word_of_the_day}\nMeaning: {meaning}"

  # Email settings
  sender_email = "lorenzodamiani06@gmail.com"
  receiver_email = "osullivanjack16@gmail.com"
  password = "*****"

  msg = MIMEText(email_content)
  msg['Subject'] = f"Word of the Day: {word_of_the_day}"
  msg['From'] = sender_email
  msg['To'] = receiver_email

  # Send the email
  try:
      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
          server.login(sender_email, password)
          server.sendmail(sender_email, receiver_email, msg.as_string())
      print("Email sent successfully!")
  except Exception as e:
      print(f"Failed to send email: {e}")

  return "Done!!"
