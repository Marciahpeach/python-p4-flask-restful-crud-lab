from server.app import app
from server.config import db
from server.models import Plant

with app.app_context():
    Plant.query.delete()

    plants = [
        Plant(name="Aloe", image="./images/aloe.jpg", price=11.50, is_in_stock=True),
        Plant(name="Fiddle Leaf", image="./images/fiddle-leaf.jpg", price=25.00, is_in_stock=True),
        Plant(name="Snake Plant", image="./images/snake.jpg", price=18.75, is_in_stock=False),
    ]

    db.session.add_all(plants)
    db.session.commit()

    print("🌱 Seeded database with plants!")
