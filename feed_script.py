from pyscript import document, window
import json
import datetime
import uuid

# Helper: Get posts from localStorage (default empty list)
def get_posts():
    storage = window.localStorage
    posts_json = storage.getItem("home_feed_posts") or "[]"
    posts = json.loads(posts_json)
    for post in posts:
        if "username" not in post:
            post["username"] = "Anonymous"
        if "id" not in post:
            post["id"] = str(uuid.uuid4())
    return posts

# Helper: Save posts to localStorage
def save_posts(posts):
    storage = window.localStorage
    storage.setItem("home_feed_posts", json.dumps(posts))

# Helper: Get default username from localStorage
def get_default_username():
    storage = window.localStorage
    return storage.getItem("default_username") or ""

# Helper: Save default username to localStorage
def save_default_username(name):
    storage = window.localStorage
    storage.setItem("default_username", name)

# Helper: Load default username into input
def load_username():
    default = get_default_username()
    username_elem = document.getElementById("username")
    username_elem.value = default

# Helper: Render feed to <ul>
def render_feed():
    feed_list = document.getElementById("feed-list")
    feed_list.innerHTML = ""  # Clear existing
    posts = get_posts()
    posts.reverse()  # Newest first
    
    for post in posts:
        li = document.createElement("li")
        timestamp = datetime.datetime.fromisoformat(post["timestamp"]).strftime("%Y-%m-%d %H:%M")
        li.innerHTML = f'''
            <div class="post-header">
                <span class="username">{post["username"]}</span>
                <span class="timestamp">[{timestamp}]</span>
            </div>
            <p class="post-text">{post["text"]}</p>
            <button class="delete-btn" py-click="delete_post" data-id="{post["id"]}">Delete</button>
        '''
        feed_list.appendChild(li)

# Delete post
def delete_post(event):
    target = event.target
    post_id = target.getAttribute("data-id")
    posts = get_posts()
    posts = [p for p in posts if p["id"] != post_id]
    save_posts(posts)
    render_feed()  # Refresh display

# Add new post
def add_post(event):
    username_elem = document.getElementById("username")
    text_elem = document.getElementById("post-text")
    
    username = username_elem.value.strip()
    text = text_elem.value.strip()
    
    if not text:
        return  # Ignore empty posts
    
    # Save default username if provided
    if username:
        save_default_username(username)
    
    # Use provided or default or anonymous
    final_username = username or get_default_username() or "Anonymous"
    
    posts = get_posts()
    new_post = {
        "id": str(uuid.uuid4()),
        "username": final_username,
        "text": text,
        "timestamp": datetime.datetime.now().isoformat()
    }
    posts.append(new_post)
    save_posts(posts)
    
    text_elem.value = ""  # Clear text
    if not username:
        # Restore default if input was empty
        username_elem.value = get_default_username() or ""
    else:
        username_elem.value = ""  # Clear if custom was entered
    render_feed()  # Refresh display

# Load feed and username on page start
render_feed()
load_username()
