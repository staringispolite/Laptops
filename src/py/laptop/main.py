from bottle import route, run
from laptop import model

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
@route('laptop')
def laptop():
  # Get get params
  # Get Questions
  # Print from template
  return "laptop page" 

@route('api/:version/:endpoint')
def api(version=None, endpoint=None):
  if version != '1.0':
    if endpoint == 'rank':
      return rank()
  return 'TODO send this to 500'

# Import configuration params
def bootstrap():
  model.bootstrap()

# If run from CLI, not imported, run the app
if __name__ == '__main__':
  # TODO: move to apache/mod_wsgi, http://bottlepy.org/docs/dev/tutorial.html#apache-mod-wsgi
  # TODO: Load from configs. Localhost config to use 8080 and 127.0.0.1
  bootstrap()
  run(server="paste", host="0.0.0.0", port=8080)

