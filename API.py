import sqlite3

class DataBase:
    PROMPT_INSERT = "INSERT INTO Citizen (Name, ACN, MobileNumber, Image) VALUES (?, ?, ?, ?)"
    PROMPT_RETRIEVE_IMAGES = "SELECT ACN, Image FROM Citizen"
    PROMPT_RETRIEVE_INFO = "SELECT Name, MobileNumber FROM Citizen WHERE ACN = ?"
    def __init__(self):
        self.conn = sqlite3.connect("Sample.db")
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def converttoBinary(self, filename):
        with open(filename,'rb') as file:
            binarydata = file.read()
        return binarydata

    def convertToFile(self, binarydata,filename):
        with open(filename,'wb') as file:
            file.write(binarydata)

    def insert_record(self, name, acn, mn, im):
        self.cursor.execute(self.PROMPT_INSERT, (name, acn, mn, self.converttoBinary(im)))

    def retrieve_images(self, path):
        data = self.cursor.execute(self.PROMPT_RETRIEVE_IMAGES)

        for e in data:
            self.convertToFile(e[1], path + str(e[0]) + ".jpg")

    def retrieve_info(self, acn):
        self.cursor.execute(self.PROMPT_RETRIEVE_INFO, (acn, ))

        return self.cursor.fetchone()
