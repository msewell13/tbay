from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)


class Item(Base):
    __tablename__ = 'items'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    # One-to-many relationship between User and Item
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref='items')
    
    
class Bid(Base):
    __tablename__ = 'bids'
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    # One-to-many relationship between Item and Bid
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    item = relationship('Item', backref="bid")

    # One-to-many relationship between User and Bid
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bidder = relationship('User', backref="bids")

Base.metadata.create_all(engine)

if __name__ == '__main__':
    matt = User(username='matt', password='password')
    jessica = User(username='jessica', password='password')
    bob = User(username='bob', password='password')
    
    baseball = Item(name='baseball', description='Official MLB baseball', owner=bob)
    
    bids = [Bid(price=2.0, item=baseball, bidder=matt),
            Bid(price=3.0, item=baseball, bidder=matt),
            Bid(price=2.2, item=baseball, bidder=jessica),
            Bid(price=3.2, item=baseball, bidder=jessica)]
            
    session.add_all([matt, jessica, bob, baseball] + bids)
    session.commit()
    
    highest_bid = session.query(Bid).filter(Item.name=='baseball').order_by(Bid.price.desc()).first()
    
    print(highest_bid.bidder.username)