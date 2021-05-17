import requests
import json
from bs4 import BeautifulSoup
from app.utils import extractComponent
from app.models.opinion import Opinion


class Product:

    def __init__(self, productId, productName = None, opinions = []) -> None:
        self.productId = productId
        self.productName = productName
        self.opinions = opinions

    def extractProduct(self):
        response = requests.get("https://www.ceneo.pl/{}#tab=reviews".format(self.productId))
        page = 2

        while response:
            pageDOM = BeautifulSoup(response.text, 'html.parser')
            opinions = pageDOM.select("div.js_product-review")
            for opinion in opinions:
                self.opinions.append(Opinion().extractOpinion(opinion))

            response = requests.get("https://www.ceneo.pl/{}/opinie-".format(self.productId)+str(page), allow_redirects=False)
            if response.status_code == 200:
                page += 1
            else:
                break

    def exportProduct(self):
        with open(f"./opinions/{self.productId}.json", "w", encoding="UTF-8") as f:
            json.dump(self.opinions, f, indent = 4, ensure_ascii=False)
        
    def __dict__(self):
        pass

    def __str__(self) -> str:
        pass
    