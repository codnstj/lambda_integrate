from flask import Flask
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.core import patcher, xray_recorder

import requests
import slack

patcher.patch(('requests',))
app = Flask(__name__)

xray_recorder.configure(service='my serverless app with sqs')
XRayMiddleware(app, xray_recorder)


@app.route('/slack')
def receive_and_process():
    slack.receive_and_process_sqs_messages()
    return 'check slack!'


@app.route('/helloworld')
def hello_world():
    resp = requests.get('https://chaewoon.me')
    return 'hello, chaewoon: %s' % resp.url

# @app.route('/db')
# def get_database():
#     configDatabase()
