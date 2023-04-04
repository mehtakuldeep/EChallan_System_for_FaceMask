from API import DataBase
import pywhatkit
import datetime

date = datetime.datetime.now()

def sendMessage(acn):
    db = DataBase()
    result = db.retrieve_info(acn)

    m = result[1]

    pywhatkit.sendwhatmsg(f"+91{m}"," You have been spotted without a face mask and for said offence you are being charged a sum of 500 INR. You will need to Pay this sum on or before 31st of March.", date.hour, (date.minute + 1))