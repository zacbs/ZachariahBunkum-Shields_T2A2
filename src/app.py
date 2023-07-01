from flask import Flask
from models.user import User, UserSchema
app = Flask(__name__)

@app.route('/')
def index():
  return 'Hello World!'

if __name__ == '__main__':
  app.run(debug=True)