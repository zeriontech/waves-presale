from flask import Flask

app = Flask(__name__)


@app.route('/')
def test():
    response = Response("Hello World!")
    return response.to_json()

if __name__ == "__main__":
    app.run()