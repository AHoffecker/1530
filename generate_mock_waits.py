import random
from datetime import datetime, timedelta, timezone
from app.app import app
from app.models import db, Restaurant, WaitTime

def main(n=100):
    with app.app_context():
        ids = [r.id for r in Restaurant.query.all()]
        for _ in range(n):
            r_id = random.choice(ids)
            length = random.randint(1, 60)
            now = datetime.now(timezone.utc)
            order_time = now - timedelta(minutes=length)
            db.session.add(WaitTime(
                restaurant_id=r_id,
                lengthOfWait=length,
                orderTime=order_time,
                receivedTime=now,
                timestamp=now
            ))
        db.session.commit()
        print(f"Inserted {n} fake wait times.")

if __name__ == "__main__":
    main(50)  # change 200 to however many you want