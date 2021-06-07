from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html.jinja')

@app.route('/extract', methods=['GET','POST'])
def extract():
    if request.method == 'POST':
        productId = request.form.get('productId')
        product = Product(productId)
        product.extractName()
        if product.productName is not None: 
            product.extractProduct()
            product.exportProduct()
            return redirect(url_for('product', productId=productId))
        error = "Podana watość nie jesy poprawnym kodem produktu!"
        return render_template('extract.html.jinja', error=error)
    return render_template('extract.html.jinja')
    

@app.route('/products')
def products():
    products = [product.split('.')[0] for product in listdir("app/products")]
    return render_template('products.html.jinja',products=products)

@app.route('/about')
def about():
    return render_template('about.html.jinja')

@app.route('/product/<productId>')
def product(productId):
    product = Product(productId)
    product.importProduct()
    return  render_template('product.html.jinja',product=str(product), productName=product.productName)