import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import MySQLdb
import constant

class cult_leader():

    def sendEmail(self, emailTo):
        # The below code never changes, though obviously those variables need values.
        session = smtplib.SMTP('smtp.gmail.com', constant.GMAIL_PORT)
        session.ehlo()
        session.starttls()
        session.login(constant.GMAIL_USERNAME, constant.GMAIL_PASSWORD)
        emailTitle = 'Halloween 2014'
        headers = "\r\n".join(["from: " + constant.GMAIL_USERNAME,
                           "subject: " + emailTitle,
                           "to: " + emailTo,
                           "mime-version: 1.0",
                           "content-type: text/html"])
        body_of_email = "This is a special email just for the cult leader done by SQL query as to not reveal your role. Some additional info for you. You have a special job. You must not tell anyone you are the leader! There will be special items that make people talk. But you are above those!!! Nothing can make you reveal who you are until the end of the game. We will give you instructions when that is. You may lie and say you are an occult specialist even if someone uses items on you. There will be secret cult members there. They are there to make you win. If the occult specialists find out who you are... the game is over! Good luck taking all the specialists on!<br>\r\n<br>\r\nSee you at the event!<br>\r\n%s" % constant.HOST_NAME
        content = headers + "\r\n\r\n" + body_of_email
        session.sendmail(constant.GMAIL_USERNAME, emailTo, content)
        print "Email Sent"
        return

    def get_cult_leader_email(self):
        query = "SELECT email FROM %s WHERE rolltype = 'leader'" % constant.dbtable
        db = MySQLdb.Connect(host=constant.host, port=constant.dbport, user=constant.dbuser, passwd=constant.dbpassword, db=constant.database)
        
        cursor = db.cursor()
        cursor.execute(query)
        leader = cursor.fetchone()
        cursor.close()
        emailTo = leader[0]
        # Close database
        db.close()
        return emailTo
    
        
eval = cult_leader()
emailTo = eval.get_cult_leader_email()
eval.sendEmail(emailTo)