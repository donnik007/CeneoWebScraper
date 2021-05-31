from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for
from os import listdir


@app.route('/')
@app.route('/index')
def index():
    return render_template('layout.html.jinja')

@app.route('/extract/<productId>')
def extract(productId):
    product = Product(productId)
    product.extractProduct()
    product.exportProduct()
    return redirect(url_for('product', productId=productId))
    #return render_template('extract.html.jinja')
    

@app.route('/products')
def products():
    products = [product.split('.')[0] for product in listdir("app/products")]
    return render_template('products.html.jinja',products=products)

@app.route('/about')
def about():
    pass

@app.route('/product/<productId>')
def product(productId):
    product = Product(productId)
    product.importProduct()
    return  render_template('product.html.jinja',product=str(product))