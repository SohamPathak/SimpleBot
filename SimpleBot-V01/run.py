from chatterbot import ChatBot #import the chatbot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from flask import Flask, render_template, request
from models import create_post, get_posts
app = Flask(__name__)
#CORS(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0cde280ba245'

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



app = Flask(__name__)
@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():

	if request.method == 'POST':

		user_input=request.form['user_input']
		bot_response=bot.get_response(user_input)
		bot_response=str(bot_response)
		#nameb = 'Assistant'
		create_post(user_input, bot_response)

		print("Friend: "+bot_response)

	posts = get_posts()	
	return render_template('index.html',posts=posts)


if __name__=='__main__':
	app.run(debug=True,port=5000)	