# # from flask import Flask
# # import os
# # from authentication import authentication_bp
# # from pdf_processing import pdf_processing_bp
# #
# # app = Flask(__name__)
# # app.config['SECRET_KEY'] = os.urandom(24)
# #
# # # Register blueprints
# # app.register_blueprint(authentication_bp)
# # app.register_blueprint(pdf_processing_bp)
# #
# # # Your existing configurations and routes
# #
# # if __name__ == '__main__':
# #     app.run(debug=True)
#
#
# from flask import Flask
# from authentication import authentication_bp
# from pdf_processing import pdf_processing_bp
# from configparser import ConfigParser
# import os
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(24)
#
#
#
# config = ConfigParser()
# config.read('config.ini')
# app.config['MYSQL_HOST'] = config.get('MySQL', 'host')
# app.config['MYSQL_USER'] = config.get('MySQL', 'user')
# app.config['MYSQL_PASSWORD'] = config.get('MySQL', 'password')
# app.config['MYSQL_DB'] = config.get('MySQL', 'database')
# app.config['MYSQL_PORT'] = config.getint('MySQL', 'port')
#
# # Register blueprints
# app.register_blueprint(authentication_bp)
# app.register_blueprint(pdf_processing_bp)
#
# if __name__ == '__main__':
#     app.run(debug=True)
#


from flask import Flask
from flask_mysqldb import MySQL
from authentication import authentication_bp
from pdf_processing import pdf_processing_bp
import os
from configparser import ConfigParser

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Load configuration from config.ini
config = ConfigParser()
config.read('config.ini')
app.config['MYSQL_HOST'] = config.get('MySQL', 'host')
app.config['MYSQL_USER'] = config.get('MySQL', 'user')
app.config['MYSQL_PASSWORD'] = config.get('MySQL', 'password')
app.config['MYSQL_DB'] = config.get('MySQL', 'database')
app.config['MYSQL_PORT'] = config.getint('MySQL', 'port')

# Initialize MySQL
mysql = MySQL(app)

# Register blueprints
app.register_blueprint(authentication_bp)
app.register_blueprint(pdf_processing_bp)

if __name__ == '__main__':
    app.run(debug=True)
