import sqlite3
import pandas as pd
import datetime as dt
import os
import os.path


################################################################################
#   D A T A B A S E
################################################################################

class CookieDatabase:

    # Some PATHES:

    ROOT_DIR = "/Users/Maxi/Desktop/atom/python/bachelor"

    TEST_PATH = ROOT_DIR + "/tracking/backup/"
    CSV_SAVE = ROOT_DIR + "/tracking/data/csv/"
    SQLITE_SAVE = ROOT_DIR + "/tracking/data/firefox_data/"        # CHANGE this one on your computer REST should work!
    REPORT_SAVE = ROOT_DIR + "/tracking/data/reports/"
    TRANSFORM_PATH = ROOT_DIR + "/tracking/data/transformed_csv/"
    # IMPORTANT PATH: (to the Path defined in SETTINGS)
    SETTINGS = ROOT_DIR + "/tracking/data/settings/settings.txt"
    SETTINGS_CONTENT = ""
    #PATH = "/Users/Maxi/Library/Application Support/Firefox/Profiles/atr5e9t3.default-1534499409101/"           # LIVE PATH - MacBook Air


    # SQL:
    SELECT_ALL = """SELECT * FROM moz_cookies"""
    SELECT_COMPLETE = """SELECT id, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies"""
    SELECT_NECCESSARY = """SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies"""
    SELECT_INFO = """SELECT name, host, isSecure, isHttpOnly FROM moz_cookies"""
    SELECT_IMPORTANT = """SELECT name, host, isSecure FROM moz_cookies"""
    SELECT_SOMETHING = """SELECT * FROM moz_cookies"""
    RESULT_AMOUNT = 0


    def __init__(self):

        self.BASE_DIR = self.SQLITE_SAVE
        self.changeable_path = open(self.SETTINGS, 'r')
        self.FILE_TO_READ = self.changeable_path.read()
        self.SETTINGS_CONTENT = self.FILE_TO_READ           # FOR global access of this variable
        if self.changeable_path:
            self.PATH = os.path.join(self.BASE_DIR, self.FILE_TO_READ)
            #print("[LOOKUP] DATABASE from: " + str(self.changeable_path.name))


    # RELOADS the Path after the file "settings.txt" was altered in the Settings Menu
    def reload_path(self):
        self.BASE_DIR = self.SQLITE_SAVE
        self.changeable_path = open(self.SETTINGS, 'r')
        self.FILE_TO_READ = self.changeable_path.read()
        self.SETTINGS_CONTENT = self.FILE_TO_READ           # FOR global access of this variable
        if self.changeable_path:
            self.PATH = os.path.join(self.BASE_DIR, self.FILE_TO_READ)
            print("\n[UPDATE] Updating DATABASE...")
            print("[INFO] UPDATED SQLITE-PATH: '~/%s'\n" % self.FILE_TO_READ)


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
        conn.close()
        print("\n\n[-] ENTRIES in Database: " + str(entry_counter))
        print("[-] THIRD-PARTY Cookies: " + str(name_counter))
        print("[-] SITE Cookies: " + str(site_counter))
        print("[-] SECURE Cookies: " + str(secure))
        print("[-] UNSCECURE Cookies: " + str(unsecure) + "\n")


    # Saves the most important Data
    def saveImportantDatabase(self):
        conn = sqlite3.connect(self.PATH)
        c = conn.cursor()
        db = c.execute(self.SELECT_IMPORTANT)
        data_list = []


        for row in db:
            data_list.append(row)

        data = pd.DataFrame(data_list, columns=['name', 'HOST', 'SECURE'])
        data.to_csv(self.CSV_SAVE + "important_cookie_data.csv", sep=',', index=False)
        print("[*] SAVED IMPORTANT DATA: ~/data/important_cookie_data.csv")
        conn.close()


    # Saves the complete Data
    def saveCompleteDatabase(self):
        conn = sqlite3.connect(self.PATH)
        c = conn.cursor()
        db = c.execute(self.SELECT_COMPLETE)
        data_list = []


        for row in db:
            data_list.append(row)

        data = pd.DataFrame(data_list, columns=['ID', 'name', 'HOST', 'EXPIRY', 'LAST_ACCESSED', 'SECURE', 'HTTP_ONLY'])
        data.to_csv(self.CSV_SAVE + "complete_cookie_data.csv", sep=',', index=False)
        print("[*] SAVED COMPLETE DATA: ~/data/complete_cookie_data.csv")
        conn.close()


    # Returns a String with INFO
    def getInfo(self):
        conn = sqlite3.connect(self.PATH)
        c = conn.cursor()
        db = c.execute(self.SELECT_INFO)
        entry_counter = 0
        site_counter = 0
        sites = []
        unique_counter = 0
        unique_names = []
        secure = 0                      # Flagged TRUE for secure transport of cookie
        unsecure = 0                    # Flagged FALSE for secure transport of cookie (or no info available)
        http_only = 0                   # Cookie only accessible via HTTP
        script_access = 0                        # Cookie Accessible through client side script (or no info available?)

        for row in db:
            entry_counter += 1

            if row[0] not in unique_names:
                unique_names.append(row[0])
                unique_counter += 1

            if row[1] not in sites:
                # print("[%s]\n" % row[1])
                sites.append(row[1])
                site_counter += 1

            if row[2] == 1:
                secure += 1
            else:
                unsecure += 1

            if row[3] == 1:
                http_only += 1
            else:
                script_access += 1


        # print("----- UNIQUE COOKIE-NAMES:")
        # print(unique_names)
        # print()
        # print("----- UNIQUE HOSTNAMES")
        # print(sites)
        conn.close()
        return ("[#] GENERAL INFO ABOUT COOKIES STORED IN " +
                "\n['~/%s']:" % self.FILE_TO_READ +
                "\n--------------------------------------" +
                "\n[-] TOTAL Cookies: " + str(entry_counter) +
                # "\n[-] UNIQUE Names for Cookies: " + str(unique_counter) +
                # "\n[-] UNIQUE Hostnames for Cookies: " + str(site_counter) +
                "\n[-] SECURE FLAGGED Cookies: " + str(secure) +
                "\n[-] UNSCECURE FLAGGED Cookies: " + str(unsecure) +
                "\n[-] ACCESSIBLE via HTTP-ONLY: " + str(http_only) +
                "\n[-] ACCESSIBLE via Client Side Scipts: " + str(script_access) + "\n")


    # Returns a String with INFO -> R E P O R T
    def getReport(self):
        conn = sqlite3.connect(self.PATH)
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

        conn.close()
        return ("TOTAL Cookies: " + str(entry_counter) +
                "\nUNIQUE Cookies: " + str(unique_counter) +
                "\nUNIQUE Sites: " + str(site_counter) +
                "\nSECURE Cookies: " + str(secure) +
                "\nUNSCECURE Cookies: " + str(unsecure) + "\n" +
                "\nC O O K I E S : \n" + cookies_string + "\n\n\n\n\n\n" + ("#"*50) +
                "\n S I T E S : \n" + sites_string)


    # Returns a String with DATABASE
    def getDatabase(self):
        conn = sqlite3.connect(self.PATH)
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

        conn.close()
        return database_string


    # Returns a String with all INFO for a SINGLE given ID:
    def getSelectedEntryInfo(self, filter, text):
        conn = sqlite3.connect(self.PATH)
        diff = ""
        duration = ""
        c = conn.cursor()
        self.find_this = text

        # Could be changed according to needs..
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
            diff = ((dt.datetime.fromtimestamp((db[5] + db[4]) / 1000000)) - (dt.datetime.fromtimestamp(db[5] / 1000000)))
            duration = divmod(diff.days * 86400 + diff.seconds, 60)
            result_string = "<ID:\t\t" + str(db[0]) + "\n"
            result_string += "<LAST_ACCESS: \t\t" + dt.datetime.fromtimestamp(db[5] / 1000000).strftime('%d.%m.%Y-%H:%M:%S') + "\n"
            result_string += "<EXPIRATION: \t\t" + dt.datetime.fromtimestamp((db[5] + db[4]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S') + "\n"
            result_string += "<DURATION: \t\t%s:%smin\n" % (str(duration[0]), str(duration[1]))
            result_string += "<SECURE: \t\t" + str(db[6]) + "\n"
            result_string += "<HTTP: \t\t" + str(db[7]) + "\n"
            result_string += "<HOST: \t\t" + str(db[3]) + "\n"
            result_string += "<PATH: \t\t" + str(db[8]) + "\n"
            result_string += "<NAME: \t\t" + str(db[2]) + "\n"
            result_string += "<VALUE: \t\t" + str(db[1]) + "\n"
            print("[!] RESULT: \n############\n" + result_string)

        conn.close()
        return result_string


    # Returns only matching results for any given String (ID, NAME, HOST)
    def getSelectedEntries(self, filter, text):
        conn = sqlite3.connect(self.PATH)
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
        conn.close()
        return database_string


    def getResultCount(self):
        return self.RESULT_AMOUNT


    # Takes a sqlite DB name and transforms it into dataframe -> RETURNS DataFrame!
    def transformToDataFrame(self, search_term):
        conn = sqlite3.connect(self.SQLITE_SAVE + search_term + ".sqlite")
        c = conn.cursor()
        result_amount = 0
        data_row = []
        data = pd.DataFrame(columns=['ID', 'VALUE', 'NAME', 'HOST', 'ACCESSED', 'EXPIRY', 'DURATION', 'SECURE', 'HTTP'], index=None)

        db = c.execute(self.SELECT_NECCESSARY)
        if db is None:
            print("\n[X] NOTHING FOUND!")
            return "NOTHING FOUND!"
        else:
            ex_date = ""
            ac_date = ""
            diff = ""
            duration = ""

            # BUILD DATABASE Output
            for row in db:
                self.RESULT_AMOUNT = 0

                # "WRONG" ORDER! -> normally: 1. expiry  2. access
                id = str(row[0])
                value = str(row[1])
                name = str(row[2])
                host = str(row[3])
                ac_date = str(dt.datetime.fromtimestamp(row[5] / 1000000).strftime('%d.%m.%Y-%H:%M:%S'))
                ex_date = str(dt.datetime.fromtimestamp((row[5] + row[4]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S'))
                diff = ((dt.datetime.fromtimestamp((row[5] + row[4]) / 1000000)) - (dt.datetime.fromtimestamp(row[5] / 1000000)))
                duration = divmod(diff.days * 86400 + diff.seconds, 60)
                #print("Minutes: " + str(duration[0]) + " | Seconds: " + str(duration[1]) + " | ID: " + id)
                secure = str(row[6])
                http = str(row[7])

                data_row = [id, value, name, host, ac_date, ex_date, str(duration[0]), secure, http]
                data.loc[result_amount] = (data_row)
                result_amount += 1


        self.RESULT_AMOUNT = result_amount
        conn.close()
        return data


    def makeCSV(self, filter, text):
        conn = sqlite3.connect(self.PATH)
        c = conn.cursor()
        self.find_this = text
        result_amount = 0
        data_row = []
        data = pd.DataFrame(columns=['ID', 'VALUE', 'NAME', 'HOST', 'ACCESSED', 'EXPIRY', 'SECURE', 'HTTP'], index=None)

        self.SELECT_ID = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE id LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)
        self.SELECT_NAME = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE name LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)
        self.SELECT_HOST = 'SELECT id, value, name, host, expiry, lastAccessed, isSecure, isHttpOnly FROM moz_cookies WHERE host LIKE "%{}%"  ORDER BY lastAccessed DESC'.format(self.find_this)

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
            ex_date = ""
            ac_date = ""

            # BUILD DATABASE Output
            for row in db:
                self.RESULT_AMOUNT = 0

                # "WRONG" ORDER! -> normally: 1. expiry  2. access
                id = str(row[0])
                value = str(row[1])
                name = str(row[2])
                host = str(row[3])
                ac_date = str(dt.datetime.fromtimestamp(row[5] / 1000000).strftime('%d.%m.%Y-%H:%M:%S'))
                ex_date = str(dt.datetime.fromtimestamp((row[5] + row[4]) / 1000000).strftime('%d.%m.%Y-%H:%M:%S'))
                secure = str(row[6])
                http = str(row[7])

                data_row = [id, value, name, host, ac_date, ex_date, secure, http]
                data.loc[result_amount] = (data_row)
                result_amount += 1


        self.RESULT_AMOUNT = result_amount
        conn.close()
        return data


    # Checks if the given file exists:   (Could be moved to BACKEND?! -> too complicated?)
    def checkExistance(self, path, file):

        if path == "sqlite":
            self.sqlite_location = self.SQLITE_SAVE + file + ".sqlite"

            if os.path.exists(self.sqlite_location):
                return True
            else:
                return False
        elif path == "transformed":
            self.csv_location = self.TRANSFORM_PATH + file + ".csv"

            if os.path.exists(self.csv_location):
                return True
            else:
                return False
        elif path == "csv":
            self.csv_location = self.CSV_SAVE + file + ".csv"

            if os.path.exists(self.csv_location):
                return True
            else:
                return False
        elif path == "report":
            self.csv_location = self.REPORT_SAVE + file + ".csv"

            if os.path.exists(self.csv_location):
                return True
            else:
                return False
        else:
            print("FATAL ERROR IN [backend.py] -> checkExistance() method -> UNKNOWN path!")
            return None


    def loadCSV(self, path, file):

        if path == "transformed":
            self.csv_location = self.TRANSFORM_PATH + file + ".csv"

            if os.path.exists(self.csv_location):
                self.file = pd.read_csv(self.csv_location, names=['ID', 'VALUE', 'NAME', 'HOST', 'ACCESSED', 'EXPIRY', 'DURATION', 'SECURE', 'HTTP'], sep=";", index_col=0)
                return self.file.fillna('')
            else:
                return None
        elif path == "csv":     # Results of grouping!
            self.csv_location = self.CSV_SAVE + file + ".csv"

            if os.path.exists(self.csv_location):
                self.file = pd.read_csv(self.csv_location, names=['ID', 'VALUE', 'NAME', 'HOST', 'ACCESSED', 'EXPIRY', 'SECURE', 'HTTP'], index_col=0)
                return self.file
            else:
                return None
        else:
            print("FATAL ERROR IN [backend.py] -> checkExistance() method -> UNKNOWN path!")
            return None
