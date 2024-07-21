import os
import re

import gspread_dataframe as gd
import gspread as gs

import camelot
import pandas as pd

import imaplib
import email
from email.header import decode_header


GSPREAD_TOKEN = os.environ.get("GSPREAD_TOKEN")
GSPREAD_WBOOK = os.environ.get("GSPREAD_WBOOK")
GSPREAD_WSHEET = os.environ.get("GSPREAD_WSHEET")

MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASS = os.environ.get("MAIL_PASS")
MAIL_FOLDER = os.environ.get("MAIL_FOLDER")


def parse_message(msg_num):
    msg_num_bin = msg_num.encode()
    res, msg = imap.fetch(msg_num_bin, '(RFC822)')
    if res == 'OK':
        msg = email.message_from_bytes(msg[0][1])

        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                try:
                    # If filename is in cyrillic
                    filename = decode_header(part.get_filename())[0][0].decode()
                except Exception:
                    # If filename is in latin
                    filename = part.get_filename()

                # Save pdf
                with open('./last.pdf', 'wb') as f:
                    f.write(part.get_payload(decode=True))
                try:
                    date = re.findall('\d{2}[.]\d{2}', filename)[0].split('.')
                    date = int(date[0]), int(date[1]) + 2000
                except Exception:
                    date = (1, 1970)

                return date

def parse_pdf(period):
    if 'last.pdf' in os.listdir('./'):

        # Scan pdf to tables
        tables = camelot.read_pdf('./last.pdf', strip_text='\n')

        # Main data
        df2 = tables[2].df

        # Calculate slices
        range1_start = df2.index[df2[0].str.contains('Тех.обсл')][0]
        range1_stop = df2.index[df2[0].str.contains('Домофон')][0] + 1
        range2_start = df2.index[df2[0].str.contains('Холодное')][0]
        range2_stop = df2.index[df2[0].str.contains('Итого к оплате за расчетный период')][0]

        # Create df_month
        df_month = pd.concat([df2.iloc[range1_start:range1_stop], df2.iloc[range2_start:range2_stop]])
        df_month.columns = df2.iloc[0]
        df_month.iloc[:,2:15] = df_month.iloc[:,2:15].replace('Х', 0)
        df_month.iloc[:,1:2] = df_month.iloc[:,1:2].replace(['Х', 'кВт'], ['кВт*ч', 'кВт*ч'])
        df_month.iloc[:,:1] = df_month.iloc[:,:1].replace(['Электроэнергия:', '- дн. начисление', \
            '- нч. начисление'], ['Электроэнергия', 'Электроэнергия день', 'Электроэнергия ночь'])
        df_month[['Месяц', 'Год']] = period

        return df_month


gc = gs.service_account(filename=GSPREAD_TOKEN)
ws = gc.open(GSPREAD_WBOOK).worksheet(GSPREAD_WSHEET)

imap = imaplib.IMAP4_SSL(MAIL_SERVER)
imap.login(MAIL_USERNAME, MAIL_PASS)
imap.select(MAIL_FOLDER)
answer_folder = imap.search(None, "UNSEEN")
if (answer_folder[0] == 'OK') & (answer_folder[1] != [b'']):
    msg_list = answer_folder[1][0].decode().split(' ')

    for msg_num in msg_list:
        try:
            date = parse_message(msg_num)
            new_data = parse_pdf(date)
            existing_data = gd.get_as_dataframe(ws)
            new_data.columns = existing_data.columns
            updated_data = pd.concat([existing_data, new_data])
            gd.set_with_dataframe(ws, updated_data)
        except:
            pass

imap.close()
imap.logout()
