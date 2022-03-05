from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import pandas

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLE
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    map_url_2 = db.Column(db.String(500), nullable=True)

# db.create_all()


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = StringField(label='Cafe Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    img_url = StringField(label='Cafe Image url', validators=[DataRequired(), URL()])
    location = StringField('Cafe location', validators=[DataRequired()])
    has_sockets = SelectField(label='Sockets', validators=[DataRequired()], choices=['YES', 'NO'])
    has_toilet = SelectField(label='Toilet', validators=[DataRequired()], choices=['YES', 'NO'])
    has_wifi = SelectField(label='Wifi', validators=[DataRequired()], choices=['YES', 'NO'])
    can_take_calls = SelectField(label='Can take calls', validators=[DataRequired()], choices=['YES', 'NO'])
    seats = SelectField(label='Total Seats', validators=[DataRequired()],
                              choices=['0-10', '10-20', '20-30', '30-40', '40-50', '50+'])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    all_cafes = Cafe.query.all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if form.has_sockets == 'YES':
            sockets = 1
        else:
            sockets = 0
        if form.has_toilet == 'YES':
            toilet = 1
        else:
            toilet = 0
        if form.has_wifi == 'YES':
            wifi = 1
        else:
            wifi = 0
        if form.can_take_calls == 'YES':
            calls = 1
        else:
            calls = 0
        new_cafe = Cafe(
            name=form.cafe.data,
            map_url=form.location_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            has_sockets=sockets,
            has_toilet=toilet,
            has_wifi=wifi,
            can_take_calls=calls,
            seats=form.seats.data,
            coffee_price=form.coffee_price.data,
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
