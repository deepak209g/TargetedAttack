import email_data
from lib import ThreadedTimer as tt
import filters
import pythoncom
import client
import Tkinter
import tkMessageBox
import threading

susp_emails = {}

PEER_THRESH = 1

def showwarning():
    tkMessageBox()
    tkMessageBox.showwarning("Attention", "Your organization is possibly under a targeted attack")


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




if __name__ == '__main__':
    client.main()
    rt = tt.RepeatedTimer(5, main)