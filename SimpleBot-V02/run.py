from chatterbot import ChatBot #import the chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from flask import Flask, render_template, request,session
from models import create_post, get_posts
import re

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 



app = Flask(__name__)
#CORS(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0cde280ba245'

def sent_mail(toa,flag_id):   
	fromaddr = "xxxxxxx@gmail.com"
	#toaddr = "yyyyyyy@gmail.com"
	toaddr = toa   
	# instance of MIMEMultipart 
	msg = MIMEMultipart() 
  
	msg['From'] = fromaddr 
 
	msg['To'] = toaddr 
 
	msg['Subject'] = 'job posting xyz - cv'
	body = 'respected sir/mam , please find my CV attached regards'
	msg.attach(MIMEText(body, 'plain')) 
	p = MIMEBase('application', 'octet-stream') 
	if flag_id == "1":
		msg['Subject'] = 'Pan card'
		body = 'respected sir/mam , please find my pan card attached regards'
		msg.attach(MIMEText(body, 'plain')) 
		p = MIMEBase('application', 'octet-stream')
		p.set_payload(open("pan.JPEG", "rb").read())
		encoders.encode_base64(p) 
		p.add_header('Content-Disposition', 'attachment; filename= "pan.JPEG"')   
		msg.attach(p)

	if flag_id == "2":
		msg['Subject'] = 'job posting xyz - cv'
		body = 'respected sir/mam , please find my CV attached regards'
		msg.attach(MIMEText(body, 'plain')) 
		p = MIMEBase('application', 'octet-stream')
		p.set_payload(open("SohamPathakRESUME.pdf", "rb").read())
		encoders.encode_base64(p) 
		p.add_header('Content-Disposition', 'attachment; filename= "SohamPathakRESUME.pdf"')   
		msg.attach(p)


    
		      
	# attach the instance 'p' to instance 'msg' 
	#msg.attach(p) 
	  
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(fromaddr, "1234567") 
	  
	# Converts the Multipart msg into a string 
	text = msg.as_string() 
	  
	# sending the mail 
	s.sendmail(fromaddr, toaddr, text) 
	  
	# terminating the session 
	s.quit() 



subject = 'Subject - urgent'
body = 'Hey !!'
toadd = 'kaisersoham@gmail.com'


bot= ChatBot('Bot')
trainer = ChatterBotCorpusTrainer(bot)

corpus_path = 'C:\\Users\\KIIT_Intern\\AppData\\Roaming\\nltk_data\\corpora\\chatterbot-corpus-master\\chatterbot_corpus\\data\\english\\'

for file in os.listdir(corpus_path):
    trainer.train(corpus_path + file)

#while True:
#    message = input('You:')
#    print(message)
#    if message.strip() == 'Bye':
#        print('ChatBot: Bye')
#        break
#    else:
#        reply = bot.get_response(message)


#session['flag'] = 0



flag = 0
flag_id = "0"
app = Flask(__name__)
@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():
	global flag
	global flag_id
	global toadd
    
	if request.method == 'POST':

		user_input=request.form['user_input']
		if (len(re.compile(r"\bbye\b",re.I).findall(user_input))):
			print('ChatBot: Bye')
			bot_response = 'Bye'
			return render_template('bye.html', title='Bye')
		if (len(re.compile(r"\bmail\b",re.I).findall(user_input))!=0):
			bot_response = 'Whom do you want to sent the mail'
			create_post(user_input, bot_response)
			flag = 1
			posts = get_posts()	
			return render_template('index.html',posts=posts)
		if (len(re.compile(r"[^@]+@[^@]+\.[^@]+",re.I).findall(user_input))!=0 and flag == 1):
			flag = 2
			toadd = user_input 
			print(user_input)
			bot_response = 'What do you want to attach in the mail use @@ followed by 1)Resume 2)PAN 3)ADHAR 4)Resignation Letter'
			create_post(user_input, bot_response)
			posts = get_posts()
			return render_template('index.html',posts=posts)
#		else:
#			print('try again with some correct email')
#			bot_response = 'try again with some correct email'
#			create_post(user_input, bot_response)
#			posts = get_posts()
#			return render_template('index.html',posts=posts)			

		if len(re.compile(r"@@",re.I).findall(user_input))!=0:
			flag_id = user_input[2:]
			print(flag_id)
			sent_mail(toadd,flag_id)
			flag = 0
			flag_id = 0
			bot_response = 'Hold on I am sending it'
			create_post(user_input, bot_response)
			posts = get_posts()
			return render_template('index.html',posts=posts)			


    	



		bot_response=bot.get_response(user_input)
		bot_response=str(bot_response)
		#nameb = 'Assistant'
		create_post(user_input, bot_response)

		print("Friend: "+bot_response)

	posts = get_posts()	
	return render_template('index.html',posts=posts)


if __name__=='__main__':
	app.run(debug=True,port=5000)	