import json
from flask import Flask, jsonify, render_template,  request, redirect 
from flask_sqlalchemy import SQLAlchemy  
from datetime import datetime 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)  

class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return '<Grocery %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        new_stuff = Grocery(name=name)

        try:
            db.session.add(new_stuff)
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem adding new stuff."

    else:
        groceries = Grocery.query.order_by(Grocery.created_at).all()
        title = "My home Data"
        return render_template('index.html', title=title, groceries=groceries)

@app.route('/delete/<int:id>')
def delete(id):
    grocery = Grocery.query.get_or_404(id)

    try:
        db.session.delete(grocery)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting data."

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    grocery = Grocery.query.get_or_404(id)

    if request.method == 'POST':
        grocery.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating data."

    else:
        title = "Update Data"
        return render_template('update.html', title=title, grocery=grocery)

@app.route('/data', methods=['GET'])
def get_current_data():
    with open('json/data.json','r') as f:
        data = json.load(f);
        response = jsonify({"Message": "Data read"}, data)
        response.status_code = 200
        return response
    # return jsonify(username=g.user.username,
    #                email=g.user.email,
    #                id=g.user.id)

if __name__ == '__main__':
    app.run(debug=True)