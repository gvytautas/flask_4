"""
-Flask-SQLAlchemy
    foreign key
    One2Many
    Many2One
    Many2Many
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = "?``§=)()%``ÄLÖkhKLWDO=?)(_:;LKADHJATZQERZRuzeru3rkjsdfLJFÖSJ"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database?check_same_thread=False'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


class Client(db.Model):
    __tablename__ = 'client'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String)
    stock = db.relationship('Stock', back_populates='product')


class Stock(db.Model):
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product', back_populates='stock')


with app.app_context():
    import forms

    db.create_all()


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = forms.AddClientForm()
    if request.method == 'POST':
        name = form.name.data
        client = Client(name=name)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('show_clients'))

    return render_template('add_client.html', form=form)


@app.route('/clients')
def show_clients():
    clients = db.session.execute(db.select(Client)).scalars()
    return render_template('clients.html', data=clients)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = forms.CreateProductForm()
    if request.method == 'POST':
        product = Product(name=form.name.data, code=form.code.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_product.html', form=form)


@app.route('/add_stock', methods=['GET', 'POST'])
def add_stock():
    form = forms.CreateStockForm()
    if request.method == 'POST':
        stock = Stock(quantity=form.quantity.data, product_id=form.product_id.data.id)
        db.session.add(stock)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_stock.html', form=form)


@app.route('/show_stock')
def show_stock():
    stock = Stock.query.all()
    return render_template('show_stock.html', data=stock)


if __name__ == '__main__':
    app.run(debug=True)
