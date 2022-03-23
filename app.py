from flask import Flask
from functions import checker

app = Flask(__name__)

@app.route('/')
def dummy():
  checker()
  
  return "a dummy site, nothing here."

if __name__ == "__main__":
  app.run()
