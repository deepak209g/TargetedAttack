import File_Utils as fu
import os
import email_data
import search_db


CLEAN = 0
SPAM = 1

mydomain = 'symantec.com'
def filter_mail_from(meta):
    if meta['Sender'] == mydomain:
        return CLEAN
    else:
        return SPAM


def filter_mail_blacklist(meta):
    hostname = meta['Sender']
    row = search_db.search_link_in_blacklist(hostname)
    if row is not None:
        return SPAM
    else:
        return CLEAN

def filter_mail_whitelist(meta):
    hostname = meta['Sender']
    row = search_db.search_link_in_whitelist(hostname)
    if row is not None:
        return CLEAN
    else:
        return SPAM


def filter_email(meta):
    returns = []
    returns.append(filter_mail_from(meta))
    returns.append(filter_mail_blacklist(meta))
    returns.append(filter_mail_whitelist(meta))
    if SPAM in returns:
        return SPAM
    else:
        return CLEAN

# returns only spammy emails
def filter_list(list):
    toret = []
    for item in list:
        f = filter_email(item)
        if f == SPAM:
            toret.append(item)

    return toret


if __name__ == '__main__':
    root = fu.absdir(__file__)
    emails = os.path.join(root, 'Data', 'email')
    _, files = fu.listdir(emails)

    for file in files:
        file = os.path.join(emails, file)
        meta = email_data.get_metadata(file)
        print meta