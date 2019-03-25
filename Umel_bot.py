import datetime
import email
import imaplib
import mailbox
import telepot

token = '644158373:AAF8yisw57fukIJBraE7Z1yXaRqUCLLm75E'
bot = telepot.Bot(token)
response = bot.getUpdates()

EMAIL_ACCOUNT = "e-mail"
PASSWORD = "password"
while True:
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(EMAIL_ACCOUNT, PASSWORD)
    mail.list()
    mail.select('inbox')
    result, data = mail.uid('search', None, "UNSEEN") # (ALL/UNSEEN)
    i = len(data[0].split())

    for x in range(i):
        latest_email_uid = data[0].split()[x]
        result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')

        raw_email = email_data[0][1]
        raw_email_string = raw_email
        email_message = email.message_from_string(raw_email_string)

    # Header 
        date_tuple = email.utils.parsedate_tz(email_message['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
        email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
        email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
        subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
    
    # Body 
        for part in email_message.walk():
            body = part.get_payload(decode=False)
            file_name = "email_" + str(x) + ".txt"
            output_file = open(file_name, 'w')
            output_file.write("Date: %s\n\nBody: \n\n%s" %(local_message_date,body))
            output_file.close()
        f = open('email_0.txt', 'r+')
        text = f.read()
        dec_text = text.decode('utf-8')
        print(text)
        f.close()
        bot.sendMessage(-1001238079186, text)
        open('email_0.txt', 'w').close()
