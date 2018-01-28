from flask import Flask
from flask_ask import Ask, statement
from chatterbot import ChatBot
import logging
import yaml

app = Flask(__name__)
ask = Ask(app, '/')
app.config['SECRET_KEY'] = 'adlfkja;ldsklka;lklklwlqrtuiotequrujfal;cxvae'

logging.basicConfig(level=logging.INFO)

botBrain = ChatBot(
  "dadBot",
  storage_adapter="chatterbot.storage.MongoDatabaseAdapter",
  logic_adapters=[
    "chatterbot.logic.BestMatch"
  ],
  trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
  database="testo",
  database_uri="mongodb://toejamb:lamb@ds117878.mlab.com:17878/testo"
)

botBrain.train('./dad.yml')

@ask.launch
def launched():
  return question('Chat with dadBot the wise')

@ask.session_ended
def session_ended():
  return "{}", 200

@ask.intent('WisIntent')
def wisdom(ask):
    wisdom = botBrain.get_response(ask)
    return statement(wisdom)
