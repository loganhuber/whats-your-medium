from flask import Flask
from routes import register_routes


app = Flask(__name__)




if __name__ in '__main__':
    app.run(debug=True)
    register_routes(app)    

