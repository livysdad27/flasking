from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from chatterbot import ChatBot
import logging
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = 'adlfkja;ldsklka;lklklwlqrtuiotequrujfal;cxvae'
bootstrap = Bootstrap(app)

logging.basicConfig(level=logging.INFO)

class GetWisdom(FlaskForm):
  ask = StringField('What do you want to ask dadbot?', validators=[DataRequired()])
  submit = SubmitField('Ask')

class GetQA(FlaskForm):
  q = StringField('Q:', validators=[DataRequired()])
  a = StringField('A:', validators=[DataRequired()])
  submit = SubmitField('Add')

botBrain = ChatBot(
  "dadBot",
  storage_adapter="chatterbot.storage.SQLStorageAdapter",
  logic_adapters=[
    "chatterbot.logic.BestMatch"
  ],
  trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
  database="./db/dadBot"
)

botBrain.train('./dad.yml')

@app.route('/')
def index():
  return render_template('index.html')
 
app.add_url_rule('/', 'index', index)

@app.route('/convo', methods=['GET', 'POST'])
def convo():
  with open ('dad.yml') as cf:
    convo_doc = yaml.load(cf)

  form = GetQA()
  if form.validate_on_submit():
    stream = open('dad.yml', 'w')
    convo_doc['conversations'].append([form.q.data, form.a.data])
    yaml.dump(convo_doc, stream)
    botBrain.train('./dad.yml')
    form.q.data = ''
    form.a.data = ''    

  return render_template('convo.html', doc=yaml.dump(convo_doc, default_flow_style=False), form=form)

@app.route('/dbot', methods=['GET', 'POST'])
def dbot():
  wisdom = '' 
  form = GetWisdom()
  if form.validate_on_submit():
    wisdom = botBrain.get_response(form.ask.data)
    form.ask.data = ''
  return render_template('dbot.html', wisdom=wisdom, form=form)

#@ask.launch
#def launched():
#  return question('Chat with dadBot the wise')
#
#@ask.session_ended
#def session_ended():
#  return "{}", 200
#
#@ask.intent('WisIntent')
#def wisdom(ask):
#    wisdom = botBrain.get_response(ask)
#    return statement(wisdom)
