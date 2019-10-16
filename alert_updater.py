from models.alert import Alert

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    item = alert.item
    item.load_price()
    item.save_to_database()
    alert.notify_if_price_reached()
