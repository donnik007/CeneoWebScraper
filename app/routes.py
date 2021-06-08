from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request
from os import listdir
import os
import json


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
    opinions = []
    cons = []
    pros = []
    avr = []
    for product in products:
        with open(f"app/products/{product}.json", "r", encoding="UTF-8") as f:
            producto = json.load(f)
            opinions.append(len(producto["opinions"]))
            sumCons = 0
            sumPros = 0
            sumStar = 0
            for opinion in producto["opinions"]:
                sumCons += len(opinion["cons"])
                sumPros += len(opinion["pros"])
                sumStar += opinion["stars"]
                
            cons.append(sumCons)
            pros.append(sumPros)
            avr.append(round(sumStar/len(producto["opinions"]),1))

    products = [[products[i], opinions[i], cons[i], pros[i], avr[i]] for i in range(len(products))]


    return render_template('products.html.jinja',products=products)

@app.route('/about')
def about():
    return render_template('about.html.jinja')

@app.route('/product/<productId>')
def product(productId):
    product = Product(productId)
    product.importProduct()
    return  render_template('product.html.jinja',product=str(product), productName=product.productName)