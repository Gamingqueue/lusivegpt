from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Flask is working!"

if __name__ == '__main__':
    print("Starting Flask test app...")
    app.run(debug=True, port=5001)
