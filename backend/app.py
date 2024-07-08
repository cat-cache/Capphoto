from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database import init_db
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # 64MB max-limit
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')

api = Api(app)
jwt = JWTManager(app)

# Initialize database
db = init_db()

# Import resources after app initialization
from resources import UserRegister, UserLogin, UserLogout, PhotoUpload, PhotoDelete, PhotoFetch, PhotoCluster, UserClusters

# API routes
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(PhotoUpload, '/upload-photo')
api.add_resource(PhotoDelete, '/delete-photo/<string:photo_id>')
api.add_resource(PhotoFetch, '/fetch-photos')
api.add_resource(PhotoCluster, '/photo-cluster/<string:photo_id>')
api.add_resource(UserClusters, '/user-clusters')

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Server starting on http://localhost:{port}")
    app.run(debug=True, host='0.0.0.0', port=port)