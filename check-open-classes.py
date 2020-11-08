import urllib.request
import json
import ast  # the lib that handles the url stuff
import smtplib
import sys
import datetime
#from gi.repository import Notify

#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

#Notify.init("Check open classes")
#Notify.Notification.new("Checking for open classes... ").show()

needed_classes = ['HSS 141B', 'HSS 141D', 'HSS 127B', 'HSS 127A', 'HSS 141A', 'E 321D', 'E 321E', 'E 321F', 'PE 200I1', 'HSS 175A', 'CPE 490A']

email = "cgarren18@gmail.com"
password = "ramymneqhhqwwile"

sms_gateway = '9133962110@mms.att.net'
# The server we use to send emails in our case it will be gmail but every email provider has a different smtp
# and port is also provided by the email provider.
smtp = "smtp.gmail.com"
port = 587
#msg = MIMEMultipart()
try:
	file = open("classes_output.txt", "r")
	lines = []
	for line in file:
	    lines.append(line)
	lastline = lines[len(lines)-2].split()
	lastline2 = lines[len(lines)-3].split()
	lastline3 = lines[len(lines)-4].split()
	#print(lastline, lastline2, lastline3)
	try:
	    last_run = datetime.datetime.strptime(
	        lastline[1] + " " + lastline[2], "%Y-%m-%d %H:%M:%S.%f")
	except:
	    try:
	        last_run = datetime.datetime.strptime(
	            lastline2[1] + " " + lastline2[2], "%Y-%m-%d %H:%M:%S.%f")
	    except:
	        last_run = datetime.datetime.strptime(
	            lastline3[1] + " " + lastline3[2], "%Y-%m-%d %H:%M:%S.%f")
	file.close()

	file = open("classes_output.txt", "a")
	# if datetime.datetime.today() - 5min == last_run
	file.write("Timestamp: " + str(datetime.datetime.today()) + '\n')

	######

    course_list = ast.literal_eval(list(urllib.request.urlopen(
        'https://stevens-scheduler.cfapps.io/p/2020F'))[0].decode('ascii'))

    # This will start our email server
    server = smtplib.SMTP(smtp, port)
    # Starting the server
    server.starttls()
    # Now we need to login
    server.login(email, password)
    num = 0
    for course in course_list:
        # if num == 0:
        # 	print('yes')
        # 	course['section'] = 'HSS 141B'
        # 	course['status'] = 'O'
        # 	course['title'] = 'Eng Dsgn V: Mat Sel & Proc Opt'
        # 	num = 1
        if course['section'] in needed_classes:
            if course['status'] == 'C':
                body = "(" + course['callNumber'] + ", " + \
                    course['section'] + ") " + course['title'] + " is CLOSED"
                print(body)
                #file.write(body + '\n')
            elif course['status'] == 'O':
                #msg['Subject'] = course['section']
                # course['maxEnrollment'] = "1"
                # course['currentEnrollment']= "0"
                if int(course['maxEnrollment'])-int(course['currentEnrollment']) == 1:
                    body = course['section'] + " (" + course['callNumber'] + ") " + course['title'] + " is OPEN! There is " + str(
                        int(course['maxEnrollment'])-int(course['currentEnrollment'])) + " spot available"
                else:
                    body = course['section'] + " (" + course['callNumber'] + ") " + course['title'] + " is OPEN! There are " + str(
                        int(course['maxEnrollment'])-int(course['currentEnrollment'])) + " spots available"
                print(body)
                #file.write(body + '\n') #NOTE: Uncommenting this could brek the program
                # Notify.Notification.new(body).show()
                #msg.attach(MIMEText(body, 'plain'))
                #sms = msg.as_string()
                sms = '\n' + body
                #print("----")
                #print(lines[len(lines)-2].split())
                #print(body.split())
                if lines[len(lines)-2].split() == body.split():
                    pass
                else:
                    server.sendmail(email, sms_gateway, sms)
                    # server.sendmail(email,sms_gateway,course['callNumber'])
                    print("sent")
            else:
                print("Course status not recognized for " + course['section'] + ". Status: " + course['status'])
                #file.write("Course status not recognized for " + course['section'] + ". Status: " + course['status'] + '\n')
                #server.sendmail(email, sms_gateway, "Error")
    #server.sendmail(email,sms_gateway,"checked classes")
    # Now we use the MIME module to structure our message.
    #msg['From'] = email
    #msg['To'] = sms_gateway
    # Make sure you add a new line in the subject
    #msg['Subject'] = "You can insert anything\n"
    # Make sure you also add new lines to your body
    #body = "You can insert message here\n"
    # and then attach that body furthermore you can also send html content.

    # lastly quit the server
except:
    error = "An error occured: {} {}, line: {}".format(
        sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno)
    print(error)
    file.write(error + '\n')
    # Notify.Notification.new(error).show()
    server.sendmail(email, sms_gateway, str(sys.exc_info()[1]))
server.quit()
# Notify.uninit()
file.write("\n")
file.close()
