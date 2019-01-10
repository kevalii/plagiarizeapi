from flask import Flask, request
from flask_restful import Resource, Api
from dotenv import load_dotenv
from os import getenv
from plagiarize import parse_word

app = Flask(__name__)
api = Api(app)
load_dotenv()
key = getenv('API-KEY')

class Plagiarize(Resource):
	def put(self):
		if request.args.get('sentence') is None and request.form['sentence'] is None:
			return {'issue': 'bad input'}, 400
		return {'sentence': parse_word(request.form['sentence'], key)} if request.args.get('sentence') is None else {'sentence': parse_word(request.args.get('sentence'), key)} 


api.add_resource(Plagiarize, '/plagiarize')