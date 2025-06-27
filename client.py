import os
from dotenv import load_dotenv
from alpha_trader.client import Client
from alpha_trader.order import Order

load_dotenv()

client = Client(
    base_url="https://stable.alpha-trader.com",
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    partner_id=os.getenv("PARTNER_ID")
)
client.login()
print(client.token)

order = Order.create(
    action="BUY",  # oder "SELL"
    quantity=100,  # Anzahl der Aktien
    price=55000,  # Preis pro Aktie
    client=client, # Nix hinschreiben, da es automatisch gesetzt wird
    owner_securities_account_id="",  # Deine Acccount-ID
    security_identifier="ACALPHCOIN",  # Name der AG die du kaufen oder verkaufen willst
    counter_party="", # ID des Gegenparts
)
