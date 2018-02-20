import os
import File_Utils as fu
import datetime
from flanker import mime
from flanker.addresslib import address
import email.utils
import time
import win32com.client, mailbox, email.utils
import pythoncom


pythoncom.CoInitialize()
def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


def __get_time_from_epoch(str):
    tup = email.utils.parsedate(str)
    toret = time.mktime(tup)
    return toret


# collects metadata from .eml file and returns a dictionary of filled with that data
def get_metadata(file):
    msg = mime.from_string(open(file).read())
    # print msg.headers.items()
    toret = {}
    for item in msg.headers.items():
        key = item[0]
        value = item[1]
        # Collecting attributes here

        # Collection information about the sender
        if key == 'From':
            addr = address.parse(value)
            toret[key] = addr.address
            toret[key + '_hostname'] = addr.hostname
            toret[key + '_mailbox'] = addr.mailbox

        # Collecting the subject
        elif key == 'Subject':
            toret[key] = value
        elif key == 'Date':
            toret[key] = __get_time_from_epoch(value)

    # getting the body of the email
    parts = []
    if 'multipart/alternative' == msg.content_type:
        # message is multipart
        for part in msg.parts:
            # print 'Content-Type: {} Body: {}'.format(part, part.body)
            parts.append(part.body)
    elif 'text/plain' in msg.content_type:
        pass
        # plain message
        # print msg.body
        parts.append(msg.body)

    text = '\n'.join(parts)
    toret['Body'] = text.strip()
    return toret


def fetch_outlook_data():
    outlook_client = win32com.client.Dispatch("Outlook.Application").GetNameSpace('MAPI')
    inbox = outlook_client.GetDefaultFolder(6)
    messages = inbox.Items
    toret = []

    for mail in messages:
        if mail.Unread:
            data = {}
            # mail is unread
            data['Subject'] = mail.Subject
            sender = ''
            if mail.Class == 43:
                if mail.SenderEmailType == "EX":
                    sender = mail.Sender.GetExchangeUser().PrimarySmtpAddress
                else:
                    sender = mail.SenderEmailAddress
            data['Sender'] = sender
            data['Body'] = mail.Body
            data['Date'] = mail.CreationTime
            toret.append(data)


    return toret


if __name__ == '__main__':
    root = fu.absdir(__file__)
    emails = os.path.join(root, 'Data', 'email')
    _, files = fu.listdir(emails)

    # for file in files:
    #     file = os.path.join(emails, file)
    #     print file
    #     print get_metadata(file)

    fetch_outlook_data()


