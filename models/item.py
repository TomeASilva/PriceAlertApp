import re  # regular expression
import uuid
from dataclasses import dataclass, field
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from common.database import Database
from models.model import Model

URL = "https://www.fnac.pt/Apple-iPad-Pro-12-9-256GB-WiFi-Cinzento-Sideral-Tablet-iPad/a6348788#st=ipad+pro&ct=Todos+os+produtos&t=p"
TAG_NAME = "span"
QUERY = {"class": "f-priceBox-price f-priceBox-price--reco checked"}


@dataclass(eq=False)
class Item(Model):
    url: str = field(default=URL)
    tag_name: str = field(default=TAG_NAME)
    query: Dict = field(default_factory=lambda: QUERY)
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    collection: str = field(init=False, default="items")

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()
        string_price = "".join(string_price.split())

        pattern = re.compile(r"(\d+,?\d\d)")  # r stands for raw string

        match = pattern.search(string_price)
        found_price = match.group(1).replace(",", ".")
        self.price = float(found_price)

        return self.price

    def json(self) -> Dict:
        "Puts the information of the item in a format to be stored in mongodb database"

        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }


if __name__ == "__main__":
    item = Item()
    print(item.load_price())
