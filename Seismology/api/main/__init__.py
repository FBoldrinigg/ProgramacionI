import os
from flask import Flask
from dotenv import load_dotenv


def create_ap():
	app = Flask(__name__)
	load_dotenv()
	return app
