from typing import Dict
import uuid
import re
from dataclasses import dataclass, Field, field
from models.model import Model

@dataclass(eq=False)
class Store(Model):
    name: str
    url_prefix: str # https://www.johnlewis.com/ or https://www.fnac.pt
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)
    collection: str = field(init=False, default="stores")

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query,
        }

    @classmethod
    def get_by_name(cls, store_name: str) -> "Store":
        return cls.find_one_by("name", store_name)

    @classmethod
    def get_by_url_prefix(cls, url_prefix: str) -> "Store":
        url_regex = {"$regex": "^{}".format(url_prefix)}
        # the $ regex is a command within mongo db it is called regular expression validation
        # ^means start with {url_prefix}
        # This will mean that if the argument given to the function is www.fnac.pt
        # And in the database there is only a register for www.fnac.pt/items
        # mongodb will still find a match
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def get_by_url(cls, url: str) -> "Store":
        """
        Return a store from a url like "https://www.fnac.pt./ipad/sdfsdf.html
        Arguments: 
        url -> The item's url
        """
        pattern = re.compile(r"(https?://.*?/)")
        match = pattern.search(url)
        url_prefix = match.group(1)
        return cls.get_by_url_prefix(url_prefix)
