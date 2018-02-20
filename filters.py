import File_Utils as fu
import os
import email_data


mydomain = 'symantec.com'
def filter_mail_hostname(meta):
    if meta['From_hostname'] == mydomain:
        return False
    else:
        return True


if __name__ == '__main__':
    root = fu.absdir(__file__)
    emails = os.path.join(root, 'Data', 'email')
    _, files = fu.listdir(emails)

    for file in files:
        file = os.path.join(emails, file)
        meta = email_data.get_metadata(file)
        print meta