import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from lxml import etree
import MySQLdb
import random
import math
from time import sleep
import constant

class halloween():

    def openDatabase(self):
        db = MySQLdb.Connect(host=constant.host, port=constant.dbport, user=constant.dbuser, passwd=constant.dbpassword, db=constant.database)
        return db

    def sendEmail(self, people, roles):
        # The below code never changes, though obviously those variables need values.
        session = smtplib.SMTP('smtp.gmail.com', constant.GMAIL_PORT)
        session.ehlo()
        session.starttls()
        session.login(constant.GMAIL_USERNAME, constant.GMAIL_PASSWORD)
        emailTitle = 'Halloween 2014'

        for person in people:
            sleep(1)
            emailTo = person['email'] 
            name = person['name']
            role = roles[person['rolltype']]
            headers = "\r\n".join(["from: " + constant.GMAIL_USERNAME,
                               "subject: " + emailTitle,
                               "to: " + emailTo,
                               "mime-version: 1.0",
                               "content-type: text/html"])
            body_of_email = "Hi %s,<br>\r\n<br>\r\nGet ready for some an eventful night!<br>\r\nYour role is %s.<br>\r\n<br>\r\nSee you at the event!<br>\r\n%s" % (name, role, constant.HOST_NAME)
            content = headers + "\r\n\r\n" + body_of_email
            print content
            # session.sendmail(constant.GMAIL_USERNAME, emailTo, content)
        return

    def playerInfo(self, db, name):
        # Collect all the column names
        query_col = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '%s'" % constant.dbtable
        cursor = db.cursor()
        cursor.execute(query_col)
        data = cursor.fetchall()
        cursor.close()
        
        columns = []
        for row in data:
            columns.append(row[0]) 

        # Collect all the data
        query_all = "SELECT %s FROM %s %s" % (",".join(columns), constant.dbtable, name)
        cursor = db.cursor()
        cursor.execute(query_all)
        data = cursor.fetchall()
        cursor.close()
        
        people = []
        for row in data:
            row_data = {}
            for idx, col in enumerate(row):
                row_data[columns[idx]] = col
            people.append(row_data)
        return people

    def loadXml(self, file):
        tree = etree.parse(file)
        root = tree.getroot()
        items = {}
        for child in root:
           items[child.tag] = child.text
        return items

    def numberOfUsers(self, db):
        user_count = []
        names = []
        name = ""
        query = "SELECT idgoodvsevil,name FROM %s WHERE rollvalue is NULL" % constant.dbtable
        cursor = db.cursor()
        cursor.execute(query)
        count = cursor.fetchall()
        # List all empty users
        if count:
            for rowid in count:
                user_count.append(int(rowid[0]))
                names.append(rowid[1])
        cursor.close()
        
        if names:
            name_string = []
            for one in names:
                name_string.append("'"+one+"'")
            name_commas = ",".join(name_string)
            name = "WHERE name IN ("+name_commas+")"

        return user_count, name
        
    def assignRoles(self, db, user_count, rollvalues, rolltypes):
        query_list = []
        base_query = "UPDATE %s.%s SET rolltype='%s', rollvalue=%s WHERE idgoodvsevil=%s;" % (constant.database, constant.dbtable, '%s', '%s', '%s')
        for index, value in enumerate(user_count):
            query_list.append(base_query % (rolltypes[index], rollvalues[index], user_count[index]))
        query = " ".join(query_list)
        cursor = db.cursor()
        cursor.execute(query)
        cursor.close()
        return

    def computeRoles(self, user_count, roles):
        total_distribution = [.1,.9]
        items = [[count]*int(math.ceil(percent*user_count)) for count, percent in enumerate(total_distribution)]
        all_items = [y for x in items for y in x]
        all_items = all_items[:user_count]
        random.shuffle(all_items)
        all_rolltype = roles.keys()
        rolltype = [all_rolltype[rollvalue] for rollvalue in all_items]
        return all_items, rolltype

def main():
    
   file = "roles.xml"
   eval = halloween()
   # Open database
   db = eval.openDatabase()
   # Get number of users
   user_count, name = eval.numberOfUsers(db)
   
   # Load roles from xml
   roles = eval.loadXml(file)
   # Compute roles
   rollvalues, rolltypes = eval.computeRoles(len(user_count), roles)
   if user_count:
       # Set the roles
       eval.assignRoles(db, user_count, rollvalues, rolltypes)
       # commit your changes
       db.commit()
       # Query database for all player info
       people = eval.playerInfo(db, name)
       # Send email
       eval.sendEmail(people, roles)

   # Close database
   db.close()

main()