from app import app
from app.models.product import Product
from flask import render_template, redirect, url_for, request, Response, send_file
from os import listdir
import json
import csv
import xml.etree.cElementTree as e
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os


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
    
    return  render_template('product.html.jinja',product=product.toDict(), productName=product.productName, productId = product.productId)

@app.route('/getCSV/<productId>')
def getCSV(productId):
    inputFile = open(f"app/products/{productId}.json", "r", encoding="UTF-8") #open json file
    outputFile = open("app/static/opinions.csv", 'w', encoding="UTF-8") #load csv file
    data = json.load(inputFile) #load json content
    inputFile.close() #close the input file
    output = csv.writer(outputFile) #create a csv.write
    output.writerow(data["opinions"][0].keys())  # header row
    for row in data["opinions"]:
        output.writerow(row.values()) #values row

    path = "static/opinions.csv"
    return send_file(path, as_attachment=True)

@app.route('/getJSON/<productId>')
def getJSON(productId):
    path = f"products/{productId}.json"
    return send_file(path, as_attachment=True)
    

@app.route('/getXML/<productId>')
def getXML(productId):
    with open(f"app/products/{productId}.json", "r", encoding="UTF-8") as f:
        producto = json.load(f)
    r = e.Element("Opinions")
    e.SubElement(r,"productId").text = producto["productId"]
    e.SubElement(r,"productName").text = producto["productName"]
    kazda = e.SubElement(r,"Opinions")
    for z in producto["opinions"]:
        project = e.SubElement(kazda,"opinia")
        e.SubElement(project,"opinionId").text = z["opinionId"]
        e.SubElement(project,"author").text = z["author"]
        e.SubElement(project,"rcmd").text = str(z["rcmd"])
        e.SubElement(project,"stars").text = str(z["stars"])
        e.SubElement(project,"content").text = str(z["content"])
        e.SubElement(project,"pros").text = str(z["pros"])
        e.SubElement(project,"cons").text = str(z["cons"])
        e.SubElement(project,"purchased").text = str(z["purchased"])
        e.SubElement(project,"publishDate").text = str(z["publishDate"])
        e.SubElement(project,"purchaseDate").text = str(z["purchaseDate"])
        e.SubElement(project,"useful").text = str(z["useful"])
        e.SubElement(project,"useless").text = str(z["useless"])
        a = e.ElementTree(r)
    a.write('opinions.xml')
    
    path = "app/static/opinions.xml"
    return send_file(path, as_attachment=True)
    

@app.route('/product/<productId>/wykresy')
def wykresy(productId):
    product = Product(productId)
    product.importProduct()
    x = product.toDict()
    opinions = x["opinions"]
    pd.set_option("display.max_columns", None)
    
    # pol,npol,niemam = 0,0,0
    # for each in opinions:
    #     if each["rcmd"] == True:
    #         pol += 1
    #     elif each["rcmd"] == False:
    #         npol += 1
    #     else:
    #         niemam+= 1
    # labels = 'Polecam', 'Nie polecam', 'Niemam zdania',
    # sizes = [pol, npol, niemam]

    # ax1 = plt.plot()
    # ax1.pie(sizes, labels=labels, colors = ["lightskyblue","crimson","forestgreen"], autopct = "%1.1f%%", pctdistance = 1.2, labeldistance = 1.4)
    # ax1.axis('equal')
    # plt.title("udział poszczególnych rekomendacji w ogólnej liczbie opinii")
    # plt.savefig(f"app/static/chart_rcmd.png", bbox_inches="tight")
    # plt.close()

    opinions = pd.DataFrame(opinions)

    

    recommendations = opinions.rcmd.value_counts(dropna = False).sort_index()
    recommendations.plot.pie(
        label="",
        colors = ["lightskyblue","crimson","forestgreen"],
        autopct = "%1.1f%%",
        pctdistance = 1.2,
        labeldistance = 1.4
    )
    plt.title("Udział poszczególnych rekomendacji w ogólnej liczbie opinii")
    plt.legend(bbox_to_anchor = (1.0,1.0))
    plt.savefig(f"app/static/chart_rcmd.png", bbox_inches="tight")
    plt.close()

     
    
    stars = opinions.stars.value_counts().reindex(np.arange(0,5.5,0.5), fill_value=0)
    stars.plot.barh(color = "lightskyblue")
    plt.title("Częstość występowania poszczególnych ocen produktu w opiniach")
    plt.xlabel("Liczba opinii")
    plt.ylabel("Liczba gwiazdek")
    plt.savefig(f"app/static/chart_stars.png", bbox_inches="tight")
    plt.close()



    return render_template('wykresy.html.jinja',productId = product.productId)