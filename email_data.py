# import eml_parser
# from mailparser import MailParser
import os
import File_Utils as fu
import datetime
from flanker import mime
import json

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

if __name__ == '__main__':
    root = fu.absdir(__file__)
    emails = os.path.join(root, 'Data', 'email')
    _, files = fu.listdir(emails)

    for file in files:
        file = os.path.join(emails, file)
        print file
        print parser.body
        print '\n\n'
