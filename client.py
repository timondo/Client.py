from alpha_trader.client import Client

def load_all_credentials(filename="users.txt"):
    with open(filename, "r") as f:
        return [line.strip().split(",", 1) for line in f if "," in line]

PARTNER_ID = "your_partner_id_here"  # Ersetze dies mit deiner Partner-ID

while True:
    users = load_all_credentials()
    total_cph = 0
    total_stored_coins = 0  # Summe aller gespeicherten Coins

    for i, (username, password) in enumerate(users, 1):
        print(f"\nStarte User {i}: {username}")

        try:
            client = Client(
                base_url="https://stable.alpha-trader.com",
                username=username.strip(),
                password=password.strip(),
                partner_id=PARTNER_ID
            )
            client.login()

            miner = client.get_miner()
            if hasattr(miner, "refresh"):
                miner.refresh()

            stored_coins = miner.storage
            total_stored_coins += stored_coins
            print(f"Vorhandene Coins im Miner: {stored_coins:.2f}")

            coins_per_hour = miner.coins_per_hour
            total_cph += coins_per_hour
            print(f"Coins pro Stunde: {coins_per_hour:.2f}")

            # Upgrade durchführen, wenn Amortisation unter 7 Tagen (168 Stunden) ist
            if hasattr(miner, "next_level_amortization_hours"):
                print(f"Amortisation bis zum nächsten Level: {miner.next_level_amortization_hours:.2f} Stunden")
                if miner.next_level_amortization_hours < 24 * 30:
                    print("Amortisation unter 7 Tagen - Upgrade wird durchgeführt...")

                    try:
                        result = miner.upgrade()
                        # Prüfe ob ein Fehler im Ergebnis steht (z.B. als dict mit code/message)
                        if isinstance(result, dict) and "code" in result and result["code"] != 200:
                            print(f"Upgrade fehlgeschlagen mit Code {result['code']}: {result.get('message', 'Keine Fehlermeldung')}")
                        else:
                            print("Upgrade erfolgreich abgeschlossen.")
                    except Exception as e:
                        print(f"Fehler beim Upgrade: {e}")

                else:
                    print("Kein Upgrade nötig.")
            else:
                print("Attribut next_level_amortization_hours nicht gefunden.")

            # Transfer durchführen
            result = miner.transfer_coins()
            transferred = result.get("transferred", 0)


        except Exception as e:
            print(f"Fehler bei User {username}: {e}")

    print(f"\nGesamt-Coins pro Stunde aller User: {total_cph:.2f}")
    print(f"Gesamt gespeicherte Coins im Miner aller User: {total_stored_coins:.2f}")
    input("\nDrücke Enter zum Neustart oder Strg+C zum Beenden...")
