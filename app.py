from flask import Flask, render_template, request, json
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submitMessage',methods=['POST','GET'])
def submitMessage():
    # print 'heard a request for submitMessage'
    print request.form['newMessage']
    return request.form['newMessage']


if __name__ == '__main__':
    app.run(debug=True)
    
