from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "一切正常"

if __name__ == "__main__":
    app.run(debug=True)
