from bottle import route, run, request
from mako.template import Template

from laptop import model

template_dir = "src/py/laptop/view"
secret_key = "548e8ce6f94cb5a225c55fe5a91bc33b"

@route('/')
def home():
  dbuser = model.config.get('sqlalchemy', 'username')
  return 'homepage. username: %s' % dbuser

@route('/blog')
def blog():
  # TODO(jon): Install apache, wordpress, send /blog to wordpress's install dir.
  return 'blog'

# Returns an empty but valid HTTP response for the LB health check
@route('/lbhc')
def load_balancer_healthcheck():
  return ''

# Simple hello world
@route('/hello/:name')
def index(name='World'):
  return '<b>Hello %s!</b>' % name

# Main selection page for laptops
@route('/laptop')
def laptop():
  # Get get params
  # Get Questions
  # Print from template
  return "laptop page" 

@route('/api/:version/:endpoint')
def api(version=None, endpoint=None):
  if version != '1.0':
    if endpoint == 'rank':
      return rank()
  return 'TODO send this to 500'

@route('/admin')
@route('/admin/')
def admin_home():
  template = Template(filename='%s/admin/home.mako' % template_dir)
  return template.render()

@route('/admin/brand')
@route('/admin/brand/')
def admin_brand():
  # Get product data
  brands = model.session.query(model.Brand).all()
  template = Template(filename='%s/admin/brand.mako' % template_dir)
  return template.render(brands=brands)

@route('/admin/brand/post', method="POST")
def admin_brand_post():
  real_secret = model.config.get('general', 'secret') 
  their_secret = request.forms.secret
  # Validate secret key
  if their_secret == real_secret:
    # Validate data
    reliability_score = int(request.forms.reliability_score)
    name = request.forms.name
    description = request.forms.description
    url = request.forms.url
    if reliability_score >= 0 and reliability_score <= 100 and \
       name != "" and description != "" and url != "":
      try:
        # Insert data, update session
        brand = model.Brand(reliability_score=reliability_score, 
          name=name, description=description, url=url)
        model.session.add(brand)
        model.session.commit()
      except:
        # TODO: Log error.
        model.session.rollback()
  return admin_brand()

@route('/admin/product')
@route('/admin/product/')
def admin_product():
  # Get product data
  products = model.session.query(model.Product).join(model.Product.brand).all()
  brands = model.session.query(model.Brand).all()
  template = Template(filename='%s/admin/product.mako' % template_dir)
  return template.render(products=products, brands=brands)

@route('/admin/product/post', method="POST")
def admin_product_post():
  real_secret = model.config.get('general', 'secret') 
  their_secret = request.forms.secret
  # Validate secret key
  if their_secret == real_secret:
    # Validate data
    brand_id = int(request.forms.brand_id)
    type = request.forms.type
    name = request.forms.name
    if brand_id > 0 and type != "" and name != "":
      try:
        # Insert data, update session
        product = model.Product(brand_id=brand_id, type=type, name=name)
        model.session.add(product)
        model.session.commit()
      except:
        # TODO: Log error.
        model.session.rollback()
  return admin_product()

@route('/admin/component-type')
@route('/admin/component-type/')
def admin_component_type():
  # Get component_type data
  component_types = model.session.query(model.ComponentType).all()
  template = Template(filename='%s/admin/component_type.mako' % template_dir)
  return template.render(component_types=component_types)

@route('/admin/component-type/post', method="POST")
def admin_component_type_post():
  real_secret = model.config.get('general', 'secret') 
  their_secret = request.forms.secret
  # Validate secret key
  if their_secret == real_secret:
    # Validate data
    name = request.forms.name
    description = request.forms.description
    if name != "" and description != "":
      try:
        # Insert data, update session
        component_type = model.ComponentType(
          name=name, description=description)
        model.session.add(component_type)
        model.session.commit()
      except:
        # TODO: Log error.
        model.session.rollback()
  return admin_component_type()

@route('/admin/component')
@route('/admin/component/')
def admin_component():
  # Get component data
  components = model.session.query(model.Component).all()
  component_types = model.session.query(model.ComponentType).all()
  template = Template(filename='%s/admin/component.mako' % template_dir)
  return template.render(components=components, component_types=component_types)

@route('/admin/component/post', method="POST")
def admin_component_post():
  real_secret = model.config.get('general', 'secret') 
  their_secret = request.forms.secret
  # Validate secret key
  if their_secret == real_secret:
    # Validate data
    component_type_id = int(request.forms.component_type_id)
    value = int(request.forms.value)
    name = request.forms.name
    description = request.forms.description
    if component_type_id > 0 and value > 0 and name != "" and \
       description != "":
      try:
        # Insert data, update session
        component = model.Component(component_type_id=component_type_id,
          value=value, name=name, description=description)
        model.session.add(component)
        model.session.commit()
      except:
        # TODO: Log error.
        model.session.rollback()
  return admin_component()

@route('/admin/product-component-map')
@route('/admin/product-component-map/')
def admin_product_component_map():
  # Get product_component_map data
  mappings = model.session.query(model.ProductComponentMap).join(model.Product).join(model.Component).all()
  components = model.session.query(model.Component).all()
  products = model.session.query(model.Product).all()
  template = Template(filename='%s/admin/product_component_map.mako' % template_dir)
  return template.render(mappings=mappings, products=products, components=components)

@route('/admin/product-component-map/post', method="POST")
def admin_product_component_map_post():
  real_secret = model.config.get('general', 'secret') 
  their_secret = request.forms.secret
  # Validate secret key
  if their_secret == real_secret:
    # Validate data
    component_id = int(request.forms.component_id)
    product_id = int(request.forms.product_id)
    
    if component_id > 0 and product_id > 0:
      try:
        # Insert data, update session
        mapping = model.ProductComponentMap(component_id=component_id,
          product_id=product_id)
        model.session.add(mapping)
        model.session.commit()
      except:
        # TODO: Log error.
        model.session.rollback()
  return admin_product_component_map()

# Import configuration params
def bootstrap():
  model.bootstrap()

# If run from CLI, not imported, run the app
if __name__ == '__main__':
  # TODO: move to apache/mod_wsgi, http://bottlepy.org/docs/dev/tutorial.html#apache-mod-wsgi
  # TODO: Load from configs. Localhost config to use 8080 and 127.0.0.1
  bootstrap()
  run(server="paste", host=model.config.get('general', 'host'),
      port=model.config.get('general', 'port'))

