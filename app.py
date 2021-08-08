from flask import Flask


app = Flask(__name__)

@app.route('/')
def dummy():
  return "a dummy site, nothing here."

if __name__ == "__main__":
  app.run()
