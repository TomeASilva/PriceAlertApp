
import uuid
from dataclasses import dataclass, field
from typing import Dict, List
from models.item import Item
from common.database import Database
from models.model import Model
from models.user import User
from libs import Mailgun


@dataclass(eq=False)  # remove all equality generation you can't compare two alerts
class Alert(Model):
    name: str
    item_id: str
    price_limit: float
    user_email: str
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="alerts")

    def __post_init__(self):
        self.item = Item.get_element_by_id(self.item_id)
        self.user = User.find_by_email(self.user_email)

    def json(self) -> Dict:
        return {
            "name": self.name,
            "_id": self._id,
            "price_limit": self.price_limit,
            "item_id": self.item_id,
            "user_email": self.user_email
        }

    def load_item_price(self) -> float:
        self.item.load_price()
        return self.item.price

    def notify_if_price_reached(self):
        if self.item.price < self.price_limit:
            print(f"Item {self.item} has reached a price below {self.price_limit}. Latest price {self.item.price}.")
            
            Mailgun.send_mail(
                [self.user_email],
                f'Notification for {self.name}',
                f'Your alert {self.name} has reached a price under {self.price_limit}. The latest price is : {self.item.price}. \n Go to this address to check your item : {self.item.url}.',
                f'<p> Your alert {self.name} has reached a price under {self.price_limit}.</p><p>The latest price is {self.item.price}.</p><p> Click <a href="{self.item.url}"> here </a> to purchase your item </p>'
            )
