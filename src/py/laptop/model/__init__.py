import ConfigParser

from sqlalchemy import Column, Index, Integer, SmallInteger, String, Enum, ForeignKey
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref

metadata = MetaData()
Base = declarative_base(metadata)
config = ConfigParser.ConfigParser()
engine = None
session = None

def bootstrap():
  global config, engine, metadata, session
  # Local config
  config.read('config/app-local.cfg')
  # Live config
  #config.read('config/app.cfg')

  username = config.get('sqlalchemy', 'username')
  password = config.get('sqlalchemy', 'password')
  host = config.get('sqlalchemy', 'host')
  database = config.get('sqlalchemy', 'database')
  # Note(jon): set pool_recycle timeout to prevent MySQL's 8-hr connection
  #   timeout feature from causing problems.
  engine = create_engine('mysql://%s:%s@%s/%s' % \
    (username, password, host, database), pool_recycle=3600)
  metadata = Brand.metadata
  metadata.bind = engine
  Session = sessionmaker(bind=engine)
  session = Session()

# Brand info for the devices on the site.
class Brand(Base):
  __tablename__ = 'brand'
  __table_args__ = {'mysql_engine':'InnoDB'}
 
  id = Column(Integer, nullable=False, primary_key=True)
  reliability_score = Column(Integer, nullable=False, index=True)
  name = Column(String(128), nullable=False)
  description = Column(String(512), nullable=False, default="")
  url = Column(String(128), nullable=False, default="")

  def __repr__(self):
    return "<Brand('%s','%s')>" % (self.id, self.name)

# Sets the bar (value) that each component in the device must reach or surpass
class QuestionComponentMap(Base):
  __tablename__ = 'question_component_map'
  __table_args__ = {'mysql_engine':'InnoDB'}

  question_id = Column(Integer, ForeignKey('question.id'), primary_key=True)
  component_id = Column(Integer, ForeignKey('component.id'), index=True)
  value = Column(Integer, nullable=False, default=0, index=True)

  components = relationship("Component", backref="question_mapping")

# Questions to ask users. Their answers 1-5 become weights in the score calculation.
class Question(Base):
  __tablename__ = 'question'
  __table_args__ = {'mysql_engine':'InnoDB'}
 
  id = Column(Integer, nullable=False, primary_key=True)
  text = Column(String(256), nullable=False)
  is_active = Column(SmallInteger, nullable=False, default=1, index=True)

  component_mapping = relationship("QuestionComponentMap", backref="questions")

  def __repr__(self):
    return "<Question('%s','%s','%s')>" % (self.id, self.text, self.is_active)

#TODO: class User
#TODO: class Answer

class Product(Base):
  __tablename__ = 'product'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  brand_id = Column(Integer, ForeignKey('brand.id'), nullable=False, index=True)
  type = Column(Enum("desktop", "laptop", "tablet"))
  name = Column(String(256), nullable=False, index=True)

  brand = relationship("Brand", backref=backref("products", order_by=id))
  affiliate_link = relationship("AffiliateLink", uselist=False)

  def __repr__(self):
    return "<Product('%s','%s')>" % (self.id, self.name)


class Component(Base):
  __tablename__ = 'component'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  component_type_id = Column(Integer, ForeignKey("component_type.id"),
    nullable=False, index=True)
  value = Column(Integer, nullable=False, default=0, index=True)
  name = Column(String(256), nullable=False)
  description = Column(String(512), nullable=False)

  component_type = relationship("ComponentType", uselist=False)
  
  def __repr__(self):
    return "<Component('%s','%s')>" % (self.id, self.name)


class ComponentType(Base):
  __tablename__ = 'component_type'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  name = Column(String(256), nullable=False, index=True)
  description = Column(String(512), nullable=False)
  
  def __repr__(self):
    return "<ComponentType('%s','%s')>" % (self.id, self.name)


class ProductComponentMap(Base):
  __tablename__ = 'product_component_map'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
  component_id = Column(Integer, ForeignKey('component.id'), nullable=False)

  product = relationship("Product", uselist=False)
  component = relationship("Component", uselist=False)
  
  def __repr__(self):
    return "<ProductComponentMap('%s','%s', '%s')>" % (
      self.id, self.product_id, self.component_id)

Index('idx_product_id_component_id', 
  ProductComponentMap.product_id, ProductComponentMap.component_id,
  unique=True)


class AffiliateLink(Base):
  __tablename__ = 'affiliate_link'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
  affiliate_site_id = Column(Integer, ForeignKey('affiliate_site.id'), nullable=False)
  url = Column(String(1024), nullable=False)
  
  def __repr__(self):
    return "<AffiliateLink('%s','%s', '%s', '%s')>" % (
      self.id, self.product_id, self.affiliate_site_id, self.url)

Index('idx_product_id_component_id', 
  AffiliateLink.product_id, AffiliateLink.affiliate_site_id,
  unique=True)


class AffiliateSite(Base):
  __tablename__ = 'affiliate_site'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  name = Column(String(128), nullable=False)
  
  affiliate_links = relationship("AffiliateLink", 
    order_by="AffiliateLink.id", backref="affiliate_site")

  def __repr__(self):
    return "<AffiliateSite('%s','%s')>" % (self.id, self.name)


