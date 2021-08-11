from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, FloatField, TextAreaField, FileField
from flask_wtf.file import FileField, FileAllowed, FileRequired

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product')
def product():
    return render_template('view-product.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


@app.route('/admin')
def admin():
    products = Product.query.all()

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


@app.route('/admin/order')
def order():
    return render_template('admin/view-order.html', admin=True)


if __name__ == '__main__':
    manager.run()
