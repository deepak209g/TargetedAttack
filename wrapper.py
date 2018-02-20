import email_data
from lib import ThreadedTimer as tt
import filters
# import pythoncom
import client
import Tkinter
import tkMessageBox
import threading
import time
import ctypes
susp_emails = {}

PEER_THRESH = 1

def showwarning():
    MessageBox = ctypes.windll.user32.MessageBoxW
    MessageBox(None, u'Malicious', u'Warning', 0)


def main(timer=10):
    print 'main'
    mails = email_data.fetch_outlook_data()
    spammy_mails = filters.filter_list(mails)
    for mail in spammy_mails:
        key = (mail['Sender'], mail['Date'])
        if key not in susp_emails:
            susp_emails[key] = mail

    # now susp_emails contains list of all suspicious emails

    print susp_emails

    for key in susp_emails:
        susp_mail = susp_emails[key]
        peerlist = client.message_generator(susp_mail['Body'])
        print 'peerlist len; ' + str(peerlist)
        if len(peerlist) >= PEER_THRESH:
            print 'show warning'
            t = threading.Thread(target=showwarning)
            t.start()
            t.join()

    time.sleep(timer)



if __name__ == '__main__':
    client.main(susp_emails)
    # rt = tt.RepeatedTimer(5, main)
    main()
