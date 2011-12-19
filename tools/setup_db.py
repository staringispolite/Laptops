from laptop import model
from laptop.model import Brand

model.bootstrap()
print "password: %s" % model.config.get('sqlalchemy', 'password')
print "engine: %s" % model.engine
print "select 1: %s " % model.engine.execute("select 1").scalar()
model.metadata.create_all();
print "tables created\n"
