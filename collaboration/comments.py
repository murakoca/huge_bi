import json
import os
from datetime import datetime

COMMENTS_FILE = "comments.json"

def load_comments():
    if os.path.exists(COMMENTS_FILE):
        with open(COMMENTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_comments(comments):
    with open(COMMENTS_FILE, 'w') as f:
        json.dump(comments, f)

def add_comment(user, text):
    comments = load_comments()
    comments.append({'user': user, 'text': text, 'time': datetime.now().isoformat()})
    save_comments(comments)

def get_comments():
    return load_comments()