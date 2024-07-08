from database import db
import pickle
from bson.binary import Binary
import atexit
from models import Photo
import numpy as np
from sklearn.cluster import DBSCAN
import face_recognition
import requests
from PIL import Image
from io import BytesIO

class IncrementalDBSCAN:
    def __init__(self, eps=0.5, min_pts=4):  # minimum people for one cluster is 4
        self.eps = eps
        self.min_pts = min_pts
        self.clusterer = DBSCAN(eps=self.eps, min_samples=self.min_pts)
        self.encodings = []
        self.labels = []

    def partial_fit(self, encoding):
        # Add the new encoding to the list
        self.encodings.append(encoding)
        # Update the DBSCAN clustering with new data
        self.clusterer.fit(self.encodings)
        self.labels = self.clusterer.labels_
        # Return the label of the new encoding
        return self.labels[-1]

    def get_cluster_labels(self):
        return self.labels

# Global dictionary to store clusterers for active users
active_clusterers = {}

def save_clusterer_state(user_id, clusterer):
    serialized_clusterer = Binary(pickle.dumps(clusterer))
    db.clusterers.update_one(
        {'user_id': user_id},
        {'$set': {'clusterer': serialized_clusterer}},
        upsert=True
    )

def load_clusterer_state(user_id):
    if user_id in active_clusterers:
        return active_clusterers[user_id]
    
    clusterer_doc = db.clusterers.find_one({'user_id': user_id})
    if clusterer_doc and 'clusterer' in clusterer_doc:
        clusterer = pickle.loads(clusterer_doc['clusterer'])
    else:
        clusterer = IncrementalDBSCAN()
    
    active_clusterers[user_id] = clusterer
    return clusterer

def cluster_photos(user_id):
    clusterer = load_clusterer_state(user_id)

    # Fetch unclustered photos
    unclustered_photos = list(db.photos.find({'user_id': user_id, 'clusters': []}))
    
    if not unclustered_photos:
        return

    # Extract features from photos
    features = extract_features(unclustered_photos)

    # Update the clusterer with new data
    for i, feature in enumerate(features):
        new_cluster = clusterer.partial_fit(feature)
        if new_cluster is not None:
            Photo.add_to_cluster(unclustered_photos[i]['_id'], user_id, new_cluster)

    # Update the clusterer in memory (no need to save to DB here)
    active_clusterers[user_id] = clusterer

def extract_features(photos):
    features = []
    for photo in photos:
        image = load_image(photo['photo_url'])
        encoding = face_recognition.face_encodings(image)
        if encoding:
            features.append(encoding[0])
    return features

def load_image(url):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return np.array(image)

def save_all_clusterers():
    for user_id, clusterer in active_clusterers.items():
        save_clusterer_state(user_id, clusterer)

# Register the save_all_clusterers function to run on exit
atexit.register(save_all_clusterers)
