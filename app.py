from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import *
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, IntegerField, FloatField, TextAreaField
from flask_wtf.file import FileField, FileAllowed

app = Flask(__name__)

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///maipi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'mysecret'

configure_uploads(app, photos)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    username = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(80))
    gender = db.Column(db.String(6))
    password = db.Column(db.String(80))


class AddUser(FlaskForm):
    name = StringField('Name')
    surname = StringField('Surname')
    username = StringField('Username')
    phone = StringField('Phone')
    address = StringField('Address')
    gender = StringField('Gender')
    password = StringField('Password')
    conpass = StringField('ConPass')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)
    stock = db.Column(db.Integer)
    description = db.Column(db.String(255))
    image = db.Column(db.String(100))


class AddProduct(FlaskForm):
    name = StringField('Name')
    price = FloatField('Price')
    stock = IntegerField('Stock')
    description = TextAreaField('Description')
    image = FileField('Image', validators=[FileAllowed(IMAGES, 'Only images are allowed')])


class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField("ID")


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/product/<id>')
def product(id):
    product = Product.query.filter_by(id=id).first()
    form = AddToCart()

    return render_template('view-product.html', product=product, form=form)


@app.route('/quick-add/<id>', methods=['GET'''])
def quick_add(id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append({'id': id, 'quantity': 1})
    session.modified = True
    print(session['cart'])
    return redirect(url_for('index'))


@app.route('/add-to-cart', methods=['POST'])
def Add_To_Cart():
    session['cart'].clear()
    if 'cart' not in session:
        session['cart'] = []

    form = AddToCart()

    if form.validate_on_submit():
        print(form.quantity.data)
        print(form.id.data)
        session['cart'].append({'id': form.id.data, 'quantity': form.quantity.data})
        session.modified = True

    return redirect(url_for('index'))


@app.route('/cart')
def cart():
    products = []
    grand_total = 0

    for item in session['cart']:
        product = Product.query.filter_by(id=item['id']).first()

        quantity = int(item['quantity'])
        total = quantity * product.price
        grand_total += total

        products.append({'id': product.id, 'name': product.name, 'price': product.price, 'image': product.image,
                         'quantity': quantity, 'total': total})

    grand_total_plus_shipping = grand_total + 1000

    return render_template('cart.html', products=products, grand_total=grand_total,
                           grand_total_plus_shipping=grand_total_plus_shipping)


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/admin')
def admin():
    products = Product.query.all()
    total=7

    products_available = Product.query.filter(Product.stock > 0).count()

    return render_template('admin/index.html', admin=True, products=products, products_available=products_available)


@app.route('/admin/add', methods=['GET', 'POST'])
def add():
    form = AddProduct()  # creates the object of the class

    if form.validate_on_submit():
        image_url = photos.url(photos.save(form.image.data))  # Gets the location of the iamge

        new_product = Product(name=form.name.data, price=form.price.data, stock=form.stock.data,
                              description=form.description.data, image=image_url)
        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('admin'))

    return render_template('admin/add-product.html', admin=True, form=form)


@app.route('/register', methods=['GET', 'POST'])
def adduser():
    form = AddUser()  # creates the object of the class

    if form.validate_on_submit():

        new_user = UserModel(name=form.name.data, surname=form.surname.data, username=form.username.data,
                              phone=form.phone.data, address=form.address.data,gender=form.gender.data,password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('register.html', admin=True, form=form)


@app.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)


if __name__ == '__main__':

    manager.run()
