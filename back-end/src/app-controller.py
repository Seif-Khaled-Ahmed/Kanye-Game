from flask import Flask
from  imageproc import hide_random_word

app = Flask(__name__)

@app.route('/image', methods=['GET']) 
def add(): 
    todo = Todo(text=request.form['todoitem'], complete=False) 
    db.session.add(todo) 
    db.session.commit() 
  
    return redirect(url_for('index')) 

if __name__ == '__main__':
    app.run(debug=True, port=8001)