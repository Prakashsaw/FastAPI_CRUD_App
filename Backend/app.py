from flask import Flask
from routes.user_route import auth_bp
from routes.product_route import product_routes
from config import Config
app = Flask(__name__)
app.config.from_object(Config)  # Load the configuration

@app.route("/")
def root():
   return "<p>Hello World! Namaste! Welcome to the Flask CRUD App!<p>"

app.register_blueprint(auth_bp, url_prefix='/api/v1/auth')
app.register_blueprint(product_routes, url_prefix='/api/v1/products')

if __name__ == '__main__':
  app.run(debug=True)

