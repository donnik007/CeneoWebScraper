from app import app
from app.models.product import Product

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/extract/<productId>')
def extract(productId):
    product = Product(productId)
    product.extractProduct()
    product.exportProduct()
    return str(product)
    

@app.route('/products')
def products():
    pass

@app.route('/about')
def about():
    pass

@app.route('/product/<productId>')
def product(productId):
    pass