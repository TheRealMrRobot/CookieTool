import sqlite3
import pandas as pd
import datetime as dt


################################################################################
#   D A T A B A S E
################################################################################

class CookieDatabase:

    PATH = "/Users/Maxi/Library/Application Support/Firefox/Profiles/atr5e9t3.default-1534499409101/"
    TEST_PATH = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/backup/"
    CSV_SAVE = "/Users/Maxi/Desktop/atom/python/bachelor/tracking/data/csv"
    SELECT_ALL = "SELECT * FROM moz_cookies"
    SELECT_COMPLETE = "SELECT id, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies"
    SELECT_IMPORTANT = "SELECT name, host, isSecure FROM moz_cookies;"
    SELECT_SOMETHING = "SELECT * FROM moz_cookies"
    RESULT_AMOUNT = 0


    def __init__(self):
        pass
        # Print info
        #self.printDatabase()


    # Shows info about the cookie-data (TERMINAL)
    def printDatabase(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_IMPORTANT)
        entry_counter = 0
        site_counter = 0
        sites = []
        name_counter = 0
        names = []
        secure = 0
        unsecure = 0

        for row in db:
            entry_counter += 1

            if row[0] not in names:
                names.append(row[0])
                name_counter += 1

            if row[1] not in sites:
                sites.append(row[1])
                site_counter += 1

            if row[2] == 1:
                secure += 1
            else:
                unsecure += 1

            #print(row)

        print("\n\n[-] ENTRIES in Database: " + str(entry_counter))
        print("[-] THIRD-PARTY Cookies: " + str(name_counter))
        print("[-] SITE Cookies: " + str(site_counter))
        print("[-] SECURE Cookies: " + str(secure))
        print("[-] UNSCECURE Cookies: " + str(unsecure) + "\n")


    # Saves the most important Data
    def saveImportantDatabase(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_IMPORTANT)
        data_list = []


        for row in db:
            data_list.append(row)

        data = pd.DataFrame(data_list, columns=['name', 'HOST', 'SECURE'])
        data.to_csv(self.CSV_SAVE + "important_cookie_data.csv", sep=',', index=False)
        print("[*] SAVED IMPORTANT DATA: ~/data/important_cookie_data.csv")


    # Saves the complete Data
    def saveCompleteDatabase(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_COMPLETE)
        data_list = []


        for row in db:
            data_list.append(row)

        data = pd.DataFrame(data_list, columns=['ID', 'name', 'HOST', 'EXPIRY', 'LAST_ACCESSED', 'SECURE', 'HTTP_ONLY'])
        data.to_csv(self.CSV_SAVE + "complete_cookie_data.csv", sep=',', index=False)
        print("[*] SAVED COMPLETE DATA: ~/data/complete_cookie_data.csv")


    # Returns a String with INFO
    def getInfo(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_IMPORTANT)
        entry_counter = 0
        site_counter = 0
        sites = []
        unique_counter = 0
        unique_names = []
        secure = 0
        unsecure = 0

        for row in db:
            entry_counter += 1

            if row[0] not in unique_names:
                unique_names.append(row[0])
                unique_counter += 1

            if row[1] not in sites:
                sites.append(row[1])
                site_counter += 1

            if row[2] == 1:
                secure += 1
            else:
                unsecure += 1

        return ("\n[-] TOTAL Cookies: " + str(entry_counter) +
                "\n[-] UNIQUE Cookies: " + str(unique_counter) +
                "\n[-] UNIQUE Sites: " + str(site_counter) +
                "\n[-] SECURE Cookies: " + str(secure) +
                "\n[-] UNSCECURE Cookies: " + str(unsecure) + "\n")


    # Returns a String with INFO -> R E P O R T
    def getReport(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_IMPORTANT)
        entry_counter = 0
        site_counter = 0
        sites = []
        unique_counter = 0
        unique_names = []
        secure = 0
        unsecure = 0
        cookies_string = ""
        sites_string = ""


        for row in db:
            entry_counter += 1

            if row[0] not in unique_names:
                unique_names.append(row[0])
                unique_counter += 1


            if row[1] not in sites:
                sites.append(row[1])
                site_counter += 1

            if row[2] == 1:
                secure += 1
            else:
                unsecure += 1


        unique_names.sort()
        sites.sort()


        for entry in unique_names:
            cookies_string += entry + "\n"

        for site in sites:
            sites_string += site + "\n"

        return ("TOTAL Cookies: " + str(entry_counter) +
                "\nUNIQUE Cookies: " + str(unique_counter) +
                "\nUNIQUE Sites: " + str(site_counter) +
                "\nSECURE Cookies: " + str(secure) +
                "\nUNSCECURE Cookies: " + str(unsecure) + "\n" +
                "\nC O O K I E S : \n" + cookies_string + "\n\n\n\n\n\n" + ("#"*50) +
                "\n S I T E S : \n" + sites_string)


    # Returns a String with DATABASE
    def getDatabase(self):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        db = c.execute(self.SELECT_COMPLETE)
        database_string = "ID \t| NAME \t\t\t\t| HOST \t\t\t\t| LAST ACCESSED\t\t\t| EXPIRATION  \t\t\t |SECURE| HTTP \n"
        database_string += "#######################################################################################################################################\n"
        ex_date = ""
        ac_date = ""

        # BUILD String for DATABASE-INFO Output
        for row in db:
            # "WRONG" ORDER! -> normally: 1. expiry  2. access
            ac_date = dt.datetime.fromtimestamp(row[4] / 1000000).strftime('%d.%m.%Y-%H:%M:%S')
            ex_date = dt.datetime.fromtimestamp((row[4] + row[3]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S')
            database_string += (str(row[0]) + " \t# " + str(row[1][0:25]) + " \t\t\t\t# "
                              + str(row[2][0:25]) + " \t\t\t\t# " + str(ac_date) + " \t\t# "
                              + str(ex_date) + " \t\t\t# " + str(row[5]) + " \t\t# " + str(row[6]) + "\n")
            database_string += "--------#-------------------------------#-------------------------------#-----------------------#------------------------#------#-----\n"

        return database_string


    # Returns a String with all INFO for a SINGLE given ID:
    def getSelectedEntryInfo(self, filter, text):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        self.find_this = text

        # Could be changed according to the needs..
        self.SELECT_ID = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly, path FROM moz_cookies WHERE id = %s' % (self.find_this)
        result_string = ""

        if filter == 1:
            db = c.execute(self.SELECT_ID)
            db = c.fetchone()       # Fetches only one ID -> there is only one for each ID!
        elif filter == 2:
            pass
        elif filter == 3:
            pass

        if db == None:
            print("[X] NOTHING FOUND!\n")
            return "NOTHING FOUND!\n"
        else:
            result_string = "_ID_:\t\t" + str(db[0]) + "\n"
            result_string += "_LAST_ACCESS_: \t" + dt.datetime.fromtimestamp(db[5] / 1000000).strftime('%d.%m.%Y-%H:%M:%S') + "\n"
            result_string += "_EXPIRATION_: \t\t" + dt.datetime.fromtimestamp((db[5] + db[4]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S') + "\n"
            result_string += "_SECURE_: \t\t" + str(db[6]) + "\n"
            result_string += "_HTTP_: \t\t" + str(db[7]) + "\n"
            result_string += "_HOST_: \t\t" + str(db[3]) + "\n"
            result_string += "_PATH_: \t\t" + str(db[8]) + "\n"
            result_string += "_NAME_: \t\t" + str(db[2]) + "\n"
            result_string += "_VALUE_: \t\t" + str(db[1]) + "\n"
            print("[!] RESULT: \n############\n" + result_string)

        return result_string


    # Returns only matching results for any given String (ID, NAME, HOST)
    def getSelectedEntries(self, filter, text):
        conn = sqlite3.connect(self.PATH + "cookies.sqlite")
        c = conn.cursor()
        self.find_this = text
        result_amount = 0

        self.SELECT_ID = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE id LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)
        self.SELECT_NAME = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE name LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)
        self.SELECT_HOST = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE host LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)
        database_string = ""

        # Check what is selected:
        if filter == 1:
            db = c.execute(self.SELECT_ID)
        elif filter == 2:
            db = c.execute(self.SELECT_NAME)
        elif filter == 3:
            db = c.execute(self.SELECT_HOST)

        if db is None:
            print("\n[X] NOTHING FOUND!")
            return "NOTHING FOUND!"
        else:
            database_string = "ID \t| VALUE \t\t\t\t | NAME \t\t\t\t| HOST \t\t\t\t| LAST ACCESSED\t\t\t| EXPIRATION  \t\t\t |SECURE| HTTP \n"
            database_string += "#######################################################################################################################################################################\n"
            ex_date = ""
            ac_date = ""

            # BUILD String for DATABASE-INFO Output
            for row in db:
                self.RESULT_AMOUNT = 0
                result_amount += 1
                # "WRONG" ORDER! -> normally: 1. expiry  2. access
                ac_date = dt.datetime.fromtimestamp(row[5] / 1000000).strftime('%d.%m.%Y-%H:%M:%S')
                ex_date = dt.datetime.fromtimestamp((row[5] + row[4]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S')
                database_string += (str(row[0]) + " \t# " + (str(row[1][0:26]) + (26-len(row[1][0:26]))*" ") + " \t\t\t\t# " + str(row[2][0:25]) + "\t\t\t\t# "
                                  + str(row[3][0:25]) + " \t\t\t\t# " + str(ac_date) + " \t\t# "
                                  + str(ex_date) + " \t\t\t# " + str(row[6]) + " \t\t# " + str(row[7]) + "\n")
                database_string += "--------#--------------------------------#------------------------------#-------------------------------#-----------------------#------------------------#------#-----\n"

        self.RESULT_AMOUNT = result_amount
        #print(database_string)
        return database_string


    def getResultCount(self):
        return self.RESULT_AMOUNT
