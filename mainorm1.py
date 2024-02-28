import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from modelsorm import create_tables, Publisher, Book, Shop, Stock, Sale

DSN = "postgresql://postgres:postgres@localhost:5432/orm"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

author = input()
q = session.query(Publisher, Book.title, Shop.name, Sale.price, Sale.date_sale).\
                join(Book).\
                join(Stock).\
                join(Shop).\
                join(Sale)
if author.isdigit():
    result = q.filter((Publisher.id == author)).all()
else:
    result = q.filter((Publisher.name == author)).all()

for publisher, title, name, price, date_sale in result:
    print(f"Название книги: {publisher}, Магазин: {name}, Стоимость продажи: {price}, Дата продажи: {date_sale}")
#result = session.query(Book, Shop, Sale).filter(Publisher.name == zapros).filter(Publisher.id == Book.id_publisher).filter(Book.id_publisher == Stock.id_book).filter(Stock.id_shop == Shop.id).filter(Stock.id == Sale.id_stock).all()
#for r in result:
    #print(f'{r[0]} | {r[1]} | {r[2]}')

session.close