import random
import time
import smtplib
import imaplib
import email
import os
from os import environ
from email.message import EmailMessage

# Account Information
IMAP_HOST = environ['IMAP_HOST']
BOT_USERNAME = environ['BOT_USERNAME']
BOT_PASSWORD = environ['BOT_PASSWORD']

def get_sushi():
    # Read in the menu from the rolls.txt file
    with open('rolls.txt', 'r') as reader:
        menu = reader.readline()

    # Read in the last order from the last_order.txt file
    with open('ordered.txt', 'r+') as reader:
        ordered = reader.readline()
        reader.truncate()


    # Make a list of the rolls and remove the ones that were ordered last time
    rolls_list = menu.split(",")
    ordered_list = ordered.split(",")

    # Need a new list to hold the options to avoid the issue of removing from the first list
    # that we encountered earlier
    options = []
    for item in rolls_list:
        for order in ordered_list:
            if order != item:
                options.append(item)

    # Get the 6 rolls to order today, using set to avoid repeats
    to_order = set()

    # Go while the length of the set is not 6
    while len(to_order) != 6:
        to_order.add(random.choice(options))

    # message to be sent as an email 
    message = ''

    message += 'Today, you should order these 6 rolls\n'
    print('Today, you should order these 6 rolls\n')

    for i, roll in enumerate(to_order):
        message += f"{i + 1}. {roll}\n"
        print(message)

    # Write the latest order to the order file 
    with open('ordered.txt', 'w') as writer:
        for item in to_order:
            writer.write(item + ",")
        print('Finished Writing Order')

    return message

def email_alert(to, subject, body):
    
    # Composing the Email
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to
    msg['from'] = BOT_USERNAME

    # Sending the Email 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(BOT_USERNAME, BOT_PASSWORD)
    server.send_message(msg)

    # Quit the end connection 
    server.quit()

def get_inbox():
    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(BOT_USERNAME, BOT_PASSWORD)
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            # print("{}: {}".format(header, email_message[header]))
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
            elif part.get_content_type() == "text/html":
                html_body = part.get_payload(decode=True)
                email_data['html_body'] = html_body.decode()
        my_message.append(email_data)
    return my_message


if __name__ == '__main__':
    
    # my_inbox = get_inbox()
    # print(my_inbox[0]["from"])

    while True:
        print('Checking inbox...')
        my_inbox = get_inbox()

        if my_inbox:
            print('Found New Message')
            for message in my_inbox:
                if 'Hit Me' in message["html_body"]:
                    msg = get_sushi()
                    try:
                        email_alert(message["from"], 'New Sushi Order', msg)
                        print('Sent Email')
                    except:
                        print('Something Went Wrong')
                else:
                    print('Not an Order')
            time.sleep(10)
        else:
            print('No Message')
            time.sleep(10)
            
