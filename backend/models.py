from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    def save_to_db(self):
        return db.users.insert_one({
            'username': self.username,
            'password_hash': self.password_hash
        }).inserted_id

    @staticmethod
    def find_by_username(username):
        return db.users.find_one({'username': username})

    @staticmethod
    def verify_password(username, password):
        user = User.find_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            return user
        return None

class Photo:
    def __init__(self, user_id, photo_url, clusters=None):
        self.user_id = user_id
        self.photo_url = photo_url
        self.clusters = clusters or []

    def save_to_db(self):
        return db.photos.insert_one({
            'user_id': self.user_id,
            'photo_url': self.photo_url,
            'clusters': self.clusters
        }).inserted_id

    @staticmethod
    def find_by_user(user_id):
        return list(db.photos.find({'user_id': user_id}))

    @staticmethod
    def delete_photo(photo_id, user_id):
        result = db.photos.delete_one({'_id': ObjectId(photo_id), 'user_id': user_id})
        return result.deleted_count > 0

    @staticmethod
    def add_to_cluster(photo_id, user_id, cluster):
        result = db.photos.update_one(
            {'_id': ObjectId(photo_id), 'user_id': user_id},
            {'$addToSet': {'clusters': cluster}}
        )
        return result.modified_count > 0

    @staticmethod
    def remove_from_cluster(photo_id, user_id, cluster):
        result = db.photos.update_one(
            {'_id': ObjectId(photo_id), 'user_id': user_id},
            {'$pull': {'clusters': cluster}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_user_clusters(user_id):
        pipeline = [
            {'$match': {'user_id': user_id}},
            {'$unwind': '$clusters'},
            {'$group': {'_id': '$clusters'}},
            {'$sort': {'_id': 1}}
        ]
        return [doc['_id'] for doc in db.photos.aggregate(pipeline)]