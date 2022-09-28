import os
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='0q923vrmuqj34tr7qw3vk04p'
db = SQLAlchemy(app)


class Symbol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbolcode = db.Column(db.String(6), unique=True, nullable=False)
    status = db.Column(db.SmallInteger)
    ceiling = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    notes = db.Column(db.Text)

@app.route('/', methods=['POST', 'GET'])
def index():
    requestedsymbol=request.args.get('s', '')
    if request.method == "POST":
        thisymbol=Symbol.query.filter_by(symbolcode=request.form['symbolcode']).one_or_none()
        if not thisymbol:
            thisymbol=Symbol(symbolcode=request.form['symbolcode'])
            db.session.add(thisymbol)
            db.session.commit()
        thisymbol.ceiling=request.form['ceiling']
        thisymbol.floor=request.form['floor']
        thisymbol.notes=request.form['notes']
        db.session.commit()
    elif requestedsymbol:
        thisymbol=Symbol.query.filter_by(symbolcode=requestedsymbol).one()
    else:
        thisymbol=None
    print("thisymbol",thisymbol)
    symbolist=Symbol.query.all()
    return render_template('index.html', symbolist=symbolist,thisymbol=thisymbol)
    
if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
