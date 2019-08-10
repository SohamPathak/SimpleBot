import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 

def sent_mail(toa,bdy,subject):   
	fromaddr = "lkpsoham@gmail.com"
	#toaddr = "kaisersoham@gmail.com"
	toaddr = toa   
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
	  
	# storing the senders email address   
	msg['From'] = fromaddr 
	  
	# storing the receivers email address  
	msg['To'] = toaddr 
	  
	# storing the subject  
	msg['Subject'] = subject
	  
	# string to store the body of the mail 
	body = bdy
	  
	# attach the body with the msg instance 
	msg.attach(MIMEText(body, 'plain')) 
	  
	# open the file to be sent  
	filename1 = "SohamPathakRESUME.pdf" 
	filename2 = "pan.JPEG"
	#attachment = open("D:\\resources", "rb") 
	  
	# instance of MIMEBase and named as p 
	p = MIMEBase('application', 'octet-stream') 


	#p.set_payload(open("SohamPathakRESUME.pdf", "rb").read())

	p.set_payload(open("pan.JPEG", "rb").read())


	  
	# To change the payload into encoded form 
	#p.set_payload((attachment).read()) 
	  
	# encode into base64 
	encoders.encode_base64(p) 
	   
	#p.add_header('Content-Disposition', 'attachment; filename= "SohamPathakRESUME.pdf"') 
	p.add_header('Content-Disposition', 'attachment; filename= "SohamPathakRESUME.pdf"')  
	# attach the instance 'p' to instance 'msg' 
	msg.attach(p) 
	  
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(fromaddr, "Mike@636") 
	  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	  
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
	  
	# terminating the session 
	s.quit() 


subject = 'Subject - urgent'
body = 'Hey !!'
toa = '1605402@kiit.ac.in'
#print("enter the email :")
#toa = input()
#print("enter the subject")
#subject = input()
#print("enter the body")
#body = input()
sent_mail(toa,body,subject)