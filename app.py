import logging
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@app.route('/health')
def health():
    app.logger.info("Health check accessed.")
    return jsonify(status="UP"), 200


@app.route('/')
def home():
    return jsonify(message="Welcome to my Flask API!")

def retry(x, y):
    if x is None or y is None:
        logger.error("Missing parameters: x=%s, y=%s", x, y)
        abort(400, description="Both 'x' and 'y' are required!")
        
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        logger.error("Invalid integer values: x=%s, y=%s", x, y) 
        abort(400, description="Both 'x' and 'y' must be valid integers!")
    
    return x, y

@app.route('/add')
def add():
    x = request.args.get('x', None)
    y = request.args.get('y', None)
    
    x, y = retry(x, y)
    
    return jsonify(result=x + y)

@app.route('/subtract')
def subtract():
    x = request.args.get('x', None)
    y = request.args.get('y', None)
    
    x, y = retry(x, y)
    
    return jsonify(result=x - y)

@app.route('/divide')
def divide():
    x = request.args.get('x', None)
    y = request.args.get('y', None)
    
    x, y = retry(x, y)
    
    if y == 0:
        logger.error("Division by zero attempted: x=%s, y=%s", x, y)
        abort(400, description="Division by zero is not allowed!")
    
    return jsonify(result=x / y)

@app.route('/multiply')
def multiply():
    x = request.args.get('x', None)
    y = request.args.get('y', None)
    
    x, y = retry(x, y)
    
    return jsonify(result=x * y)

@app.errorhandler(400)
def bad_request(e):
    logger.error("Bad request: %s", str(e.description))
    return jsonify(error=str(e.description)), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
