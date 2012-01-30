import ConfigParser

from sqlalchemy import Column, Index, Integer, String, Enum
from sqlalchemy.engine.base import Engine
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

metadata = MetaData()
Base = declarative_base(metadata)
config = ConfigParser.ConfigParser()
engine = None
session = None

def bootstrap():
  global config, engine, metadata, session
  # Local config
  #config.read('config/app-local.cfg')
  # Live config
  config.read('config/app.cfg')

  username = config.get('sqlalchemy', 'username')
  password = config.get('sqlalchemy', 'password')
  host = config.get('sqlalchemy', 'host')
  database = config.get('sqlalchemy', 'database')
  engine = create_engine('mysql://%s:%s@%s/%s' % (username, password, host, database))
  metadata = Brand.metadata
  metadata.bind = engine
  Session = sessionmaker(bind=engine)
  session = Session()


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


class Question(Base):
  __tablename__ = 'question'
  __table_args__ = {'mysql_engine':'InnoDB'}
 
  id = Column(Integer, nullable=False, primary_key=True)
  component_id = Column(Integer, nullable=False, index=True)
  text = Column(String(256), nullable=False)

  def __repr__(self):
    return "<Question('%s','%s','%s')>" % (self.id, self.component_id, self.text)


class Product(Base):
  __tablename__ = 'product'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  brand_id = Column(Integer, nullable=False, index=True)
  type = Column(Enum("desktop", "laptop", "tablet"))
  name = Column(String(256), nullable=False, index=True)

  def __repr__(self):
    return "<Product('%s','%s')>" % (self.id, self.name)


class Component(Base):
  __tablename__ = 'component'
  __table_args__ = {'mysql_engine':'InnoDB'}

  id = Column(Integer, nullable=False, primary_key=True)
  component_type_id = Column(Integer, nullable=False, index=True)
  value = Column(Integer, nullable=False, default=0, index=True)
  name = Column(String(256), nullable=False)
  description = Column(String(512), nullable=False)
  
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
  product_id = Column(Integer, nullable=False)
  component_id = Column(Integer, nullable=False)
  
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
  product_id = Column(Integer, nullable=False)
  affiliate_site_id = Column(Integer, nullable=False)
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
  
  def __repr__(self):
    return "<AffiliateSite('%s','%s')>" % (self.id, self.name)


