import email_data
from lib import ThreadedTimer as tt
import filters
import pythoncom


susp_emails = {}

def main():
    pythoncom.CoInitialize()
    print 'main'
    mails = email_data.fetch_outlook_data()
    spammy_mails = filters.filter_list(mails)
    for mail in spammy_mails:
        key = (mail['Sender'], mail['Date'])
        if key not in susp_emails:
            susp_emails[key] = mail

    # now susp_emails contains list of all suspicious emails
    # for key in susp_emails:
    #     susp_mail = susp_emails[key]
    #     print susp_mail
    #
    print susp_emails



if __name__ == '__main__':
    rt = tt.RepeatedTimer(5, main)