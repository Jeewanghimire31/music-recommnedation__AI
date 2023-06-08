from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
@app.route('/', methods=['GET'])
def my_profile():
    return{
        'name': 'John Doe',
        'about': 'I am a software developer',
    }
@app.route('/m', methods=['GET','POST'])
def musicapi():
    return 



if __name__ == '__main__':
    app.run(debug=True)