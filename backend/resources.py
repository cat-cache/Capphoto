from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models import User, Photo
from utils import cluster_photos, save_clusterer_state, active_clusterers
from bson import ObjectId

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User already exists'}, 400

        user = User(data['username'], data['password'])
        user.save_to_db()
        return {'message': 'User created successfully'}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        user = User.verify_password(data['username'], data['password'])
        if not user:
            return {'message': 'Invalid credentials'}, 401

        access_token = create_access_token(identity=str(user['_id']))
        return {'access_token': access_token}, 200

class UserLogout(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        if user_id in active_clusterers:
            save_clusterer_state(user_id, active_clusterers[user_id])
            del active_clusterers[user_id]
        # In a real-world scenario, you might want to blacklist the token here
        return {'message': 'Successfully logged out'}, 200

from flask import request
from werkzeug.utils import secure_filename
import os

class PhotoUpload(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('photo_url', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        user_id = get_jwt_identity()
        photo = Photo(user_id, data['photo_url'])
        photo_id = photo.save_to_db()

        # Perform clustering
        cluster_photos(user_id)

        return {'message': 'Photo uploaded successfully', 'photo_id': str(photo_id)}, 201

class PhotoDelete(Resource):
    @jwt_required()
    def delete(self, photo_id):
        user_id = get_jwt_identity()
        if Photo.delete_photo(photo_id, user_id):
            return {'message': 'Photo deleted successfully'}, 200
        return {'message': 'Photo not found'}, 404

class PhotoFetch(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        photos = Photo.find_by_user(user_id)
        
        # Group photos by cluster
        clustered_photos = {}
        for photo in photos:
            for cluster in photo['clusters']:
                if cluster not in clustered_photos:
                    clustered_photos[cluster] = []
                clustered_photos[cluster].append({
                    'photo_id': str(photo['_id']),
                    'photo_url': photo['photo_url']
                })

        return clustered_photos, 200

class PhotoCluster(Resource):
    @jwt_required()
    def post(self, photo_id):
        parser = reqparse.RequestParser()
        parser.add_argument('cluster', type=int, required=True, help='Cluster number is required')
        data = parser.parse_args()

        user_id = get_jwt_identity()
        if Photo.add_to_cluster(photo_id, user_id, data['cluster']):
            return {'message': 'Photo added to cluster successfully'}, 200
        return {'message': 'Photo not found or already in cluster'}, 404

    @jwt_required()
    def delete(self, photo_id):
        parser = reqparse.RequestParser()
        parser.add_argument('cluster', type=int, required=True, help='Cluster number is required')
        data = parser.parse_args()

        user_id = get_jwt_identity()
        if Photo.remove_from_cluster(photo_id, user_id, data['cluster']):
            return {'message': 'Photo removed from cluster successfully'}, 200
        return {'message': 'Photo not found or not in cluster'}, 404

class UserClusters(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        clusters = Photo.get_user_clusters(user_id)
        return {'clusters': clusters}, 200