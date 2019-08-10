from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from models import create_post, get_posts

app = Flask(__name__)
#CORS(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0cde280ba245'

bot = ChatBot('Virtual Assistant') #create the bot



#bot.set_trainer(ListTrainer) # Teacher old version

bot = ListTrainer(chatBot)


#bot.train(conv) # teacher train the bot

for knowledeg in os.listdir('base'):
	BotMemory = open('base/'+ knowledeg, 'r').readlines()
	bot.train(BotMemory)



app = Flask(__name__)
@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

@app.route('/process',methods=['POST'])
def process():

	if request.method == 'POST':

		user_input=request.form['user_input']
	    #nameu = 'User'
	    #create_post(nameu, user_input)
		bot_response=bot.get_response(user_input)
		bot_response=str(bot_response)
		#nameb = 'Assistant'
		create_post(user_input, bot_response)

		print("Friend: "+bot_response)

	posts = get_posts()	
	return render_template('index.html',posts=posts)


if __name__=='__main__':
	app.run(debug=True,port=5000)