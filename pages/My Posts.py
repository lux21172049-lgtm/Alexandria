import streamlit as st
import json
from author import hash_password, autor
from datetime import datetime
from collections import defaultdict
import random
import base64
from io import BytesIO
from PIL import Image
import requests as req
from typing import Optional, Dict, Any
import uuid

# Базовый URL API на Render
API_BASE_URL = "https://alexandria-api-o9ev.onrender.com"

st.logo("duke.png")

def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 

def registration_api(username: str, password: str):
    url = f"{API_BASE_URL}/register"
    data = {
        "username": username,
        "hash_psw": password
    }        
    resp = req.post(url, json=data)
    if resp.status_code == 200:
        return True
    else:
        return "This username is already taken"    

def login_api(username: str, password: str):
    url = f"{API_BASE_URL}/login"  
    data = {
        "username": username,
        "hash_psw": password
    }  
    resp = req.post(url, json=data)
    return resp.status_code == 200    

def write_all_default_api(username: str) -> bool:
    def default_posts(user: str) -> int:
        url = f"{API_BASE_URL}/write_default/posts"
        data = {
            "username": user
        } 
        resp = req.post(url, json=data)
        return resp.status_code
    st_post_code = default_posts(username)
    return st_post_code == 200

if not st.session_state.logged_in:
    st.set_page_config(layout="wide")
    

    # CSS для фонового изображения
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://sdmntprnortheu.oaiusercontent.com/files/00000000-5354-61f4-8366-13d2ef546511/raw?se=2025-07-27T08%3A19%3A55Z&sp=r&sv=2024-08-04&sr=b&scid=fa3ec800-3e9b-5ebe-b0c0-a23e05dc2e5f&skoid=b928fb90-500a-412f-a661-1ece57a7c318&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-07-27T05%3A28%3A47Z&ske=2025-07-28T05%3A28%3A47Z&sks=b&skv=2024-08-04&sig=4%2BESOEXeHX1wnQ4h3JvcwnCGCrRgdYh7PsnkEZIc290%3D");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        </style>
        """,
        unsafe_allow_html=True
    )    
    
    if st.session_state.show_register:
        st.title("📝 Registration")
        new_username = st.text_input("Username", key="reg_user")
        new_password = st.text_input("Password", type="password", key="reg_pass1")
        confirm_password = st.text_input("Retype the password", type="password", key="reg_pass2")
        
        if st.button("Create an account"):
            if not new_username or not new_password:
                st.error("Fill all the fields")
            elif new_password != confirm_password:
                st.error("Passwords do not match!") 
            api_answer = registration_api(new_username, hash_password(new_password))       
            if api_answer != True:
                st.error(api_answer) 
            else:    
                register_user(new_username, new_password)
                
                # Загрузка дефолтных видео
                url_videos = f"{API_BASE_URL}/load/default/videos"
                data_videos = {"username": new_username}
                resp_videos = req.post(url_videos, json=data_videos)
                print(f"Videos Status code: {resp_videos.status_code}")
                print(f"Videos Text: {resp_videos.text}")

                # Загрузка дефолтных лайков
                url_liked = f"{API_BASE_URL}/liked/default"
                data_liked = {"username": new_username}
                resp_liked = req.post(url_liked, json=data_liked)
                print(f"Liked Status code: {resp_liked.status_code}")
                print(f"Liked Text: {resp_liked.text}")

                # Создание дефолтных постов
                write_all_default_api(new_username)

                st.success("Successfully created an account. Now you can sign in.")
                st.session_state.show_register = False
                        
        if st.button("← Back to sign in"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        
        st.title("🔒 Sign in ")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Sign in"):
            if login_api(username, hash_password(password)):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Wrong password or username")
                
        if st.button("Sign up"):
            st.session_state.show_register = True
            st.rerun()
    
    st.stop()

# Основной интерфейс после авторизации
st.success(f"✅ Welcome to Alexandria, {st.session_state.username}!")        

def count_subs() -> int:
    url = f"{API_BASE_URL}/subs/count"
    data = {"username": st.session_state.username}
    resp = req.post(url, json=data)
    return int(resp.text)

def get_user_posts(username: str):
    url = f"{API_BASE_URL}/get/user/posts"
    data = {"username": username}
    resp = req.post(url, json=data)
    return resp.text

def write_post_to_user_api(author: str, title: str, content: str, type_file: str = "text", video: Optional[str] = None, photo: Optional[str] = None) -> bool:
    if author == st.session_state.username:
        data = {
            "author": author,
            "title": title,
            "content": content,
        }
        if type_file == "video" and video:
            data["type"] = "video"
            data["video"] = video
        elif type_file == "photo" and photo:
            data["type"] = "photo"
            data["photo"] = photo

        url = f"{API_BASE_URL}/write/post"
        try:
            resp = req.post(url, json=data)
            return resp.status_code == 200
        except Exception as e:
            print(f"Exception while sending request to API to create this post: {e}")
            return False

russian_government_surnames = [
    "путин", "Путин", "ПУТИН", "putin", "Putin", "PUTIN",
    "мишинестин", "Мишустин", "МИШУСТИН", "mishustin", "Mishustin", "MISHUSTIN",
    "бортников", "Бортников", "БОРТНИКОВ", "bortnikov", "Bortnikov", "BORTNIKOV",
    "песков", "Песков", "ПЕСКОВ", "peskov", "Peskov", "PESKOV",
    "кологольцев", "Колокольцев", "КОЛОКОЛЬЦЕВ", "kolokoltsev", "Kolokoltsev", "KOLOKOLTSEV",
    "чуйченко", "Чуйченко", "ЧУЙЧЕНКО", "chuychenko", "Chuychenko", "CHUYCHENKO",
    "лавров", "Лавров", "ЛАВРОВ", "lavrov", "Lavrov", "LAVROV",
    "СВО", "сво", "Война", "война", "Зеленский", "Украина", "зеленский", "украина"
]

def cens(title: str, content: str) -> bool:
    title2 = title.lower()
    cn = content.lower()
    for i in russian_government_surnames:
        if i in cn or i in title2:
            return False
    return True    

def create_post(title, author, content, files: str, type_file: str, id: str, tags=None):
    if tags is None:
        tags = []
    
    st.markdown(f"""
    <div style="
        padding: 20px;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 25px;
    ">
        <h2 style="margin-top: 0; color: #2c3e50;">{title}</h2>
        <div style="
            color: #7f8c8d;
            font-size: 0.85em;
            margin-bottom: 15px;
        ">
            Author: {author}
        </div>
        <p style="color: #34495e; line-height: 1.6;">{content}</p>
        {f'<div style="margin-top: 15px; margin-bottom: 15px;">' + 
         ''.join([f'<span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' 
                 for tag in tags]) + '</div>' if tags else ''}
    </div>
    """, unsafe_allow_html=True)
    
    def delete_post_form_user():
        data = {
            "username": st.session_state.username,
            "id": id
        }
        url = f"{API_BASE_URL}/delete/post"
        try:
            resp = req.post(url, json=data)
            print(f"Delete post Status: {resp.status_code}")
        except Exception as e:
            print(f"Exception while deleting post: {e}")
                        
    # Берем likes и dislikes массивы с API
    data_likes = {
        "author": author,
        "title": title,
        "content": content
    }     
    url_likes = f"{API_BASE_URL}/get/post/react"
    
    if type_file == "photo":
        data_likes["type"] = "photo"
        data_likes["photo"] = files
    elif type_file == "video":
        data_likes["type"] = "video" 
        data_likes["video"] = files

    resp = req.post(url_likes, json=data_likes)
    likes, dislikes = resp.json()
        
    if type_file == "photo":
        try:
            decoded_img = base64.b64decode(files)
            img = Image.open(BytesIO(decoded_img))
            st.image(img)
        except Exception as e:
            print(f"Exception photo: {e}")    

    if type_file == "video":
        try:
            video_bytes = base64.b64decode(files)
            st.video(video_bytes)
        except Exception as e:
            print(f"Exception video: {e}")     

    col1, col2 = st.columns(2)

    with col1:
        like_btn = st.button(f"👍{len(likes)}", key=f"like_{title}_{uuid.uuid4()}")

    with col2:
        dislike_btn = st.button(f"👎{len(dislikes)}", key=f"dislike_{title}_{uuid.uuid4()}")
    
    delete_post = st.button("Delete post", key=f"{title}_delete_{uuid.uuid4()}", on_click=delete_post_form_user)

st.title(st.session_state.username)
subs = count_subs()

st.markdown(
    f"<span style='display:inline-block;background-color:#e0e0e0;color:#333;padding:4px 12px;border-radius:12px;font-size:14px;font-weight:bold;'>{subs} subscribers</span>",
    unsafe_allow_html=True
)

def exi():
    st.session_state.logged_in = False

def safe_video(username: str, title: str, encoded_video: str):
    url = f"{API_BASE_URL}/write/video/user"
    data = {
        "username": username,
        "code": encoded_video,
        "title": title
    }
    resp = req.post(url, json=data)
    print(f"Safe video Status: {resp.status_code}")
    print(f"Safe video Text: {resp.text}")

def get_request(url: str, title: str):
    try:
        res = req.get(f"{url}/load_video/{title}")
        data = res.json()
        if "video_base64" in data:
            video = base64.b64decode(data["video_base64"])
            st.video(video)
    except Exception as e:
        return f"There was an error sending get request to the API, error: {e}"      

with st.sidebar:
    exit_button = st.button("Leave", on_click=exi)

with st.form("Create Post"):
    title = st.text_input("Title for the post", placeholder="Create a title")
    post = st.text_input("Make a post", placeholder="Today i...")
    uploaded_file = st.file_uploader("Add a photo?", type=["jpg", "png", "jpeg", "mp4"])

    confirm_post = st.form_submit_button("Create")
    create_post_indicator = False
    
    if confirm_post:
        if cens(title, post):
            if uploaded_file:
                if "mp4" in uploaded_file.name:
                    vd = uploaded_file.read()
                    encoded_video = base64.b64encode(vd).decode("utf-8")
                    safe_video_api = write_post_to_user_api(st.session_state.username, title, post, "video", encoded_video)
                    if safe_video_api:
                        create_post_indicator = True
                        safe_video(st.session_state.username, title, encoded_video)
                else:
                    encoded_image = base64.b64encode(uploaded_file.read()).decode("utf-8")
                    safe_video_api2 = write_post_to_user_api(st.session_state.username, title, post, "photo", photo=encoded_image)
                    if safe_video_api2:
                        create_post_indicator = True
            else:
                safe_video_api3 = write_post_to_user_api(st.session_state.username, title, post, "text")
                if safe_video_api3:
                    create_post_indicator = True
            
            if create_post_indicator:
                st.success("Post created. Reload the page.")
            else:
                st.error("Failed to create post.")
        else:
            st.error("You better rewrite this post.")             

st.markdown(
    f"<span style='display:inline-block;background-color:#e0e0e0;color:#333;padding:4px 12px;border-radius:12px;font-size:14px;font-weight:bold;'>Your posts:</span>",
    unsafe_allow_html=True
)

def get_user_posts_api_main():
    url = f"{API_BASE_URL}/get/user/posts"
    data = {"username": st.session_state.username}
    resp = req.post(url, json=data)
    return resp.json()

api_posts = get_user_posts_api_main()

if len(api_posts) == 0:
    st.markdown(
    """
    <div style='
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 8px;
        text-align: center;
        color: #606060;
        font-family: sans-serif;
        margin: 20px 0;
    '>
        <span style='font-size: 16px;'>404</span>
        <div style='font-size: 18px; font-weight: 500; margin: 10px 0;'>
            You don't have any posts yet
        </div>
        <div style='font-size: 14px;'>
            Upload your first post to get started
        </div>
    </div>
    """,
    unsafe_allow_html=True
)   

for post in api_posts:
    if "photo" in post:
        create_post(post["title"], post["author"], post["content"], post["photo"], "photo", post["id"], tags=None)
    elif "video" in post:
        create_post(post["title"], post["author"], post["content"], post["video"], "video", post["id"], tags=None)    
    else:
        create_post(post["title"], post["author"], post["content"], "", "text", post["id"], tags=None)   

def request_all_liked_posts():
    url = f"{API_BASE_URL}/get/liked"
    data = {"username": st.session_state.username}
    resp = req.post(url, json=data)
    return resp.json()

st.markdown(
    f"<span style='display:inline-block;background-color:#e0e0e0;color:#333;padding:4px 12px;border-radius:12px;font-size:14px;font-weight:bold;'>Liked posts:</span>",
    unsafe_allow_html=True
)

liked_posts = request_all_liked_posts()
print("LIKED POSTS")

if len(liked_posts) == 0:
    st.markdown(
    """
    <div style='
        background-color: #f8f9fa;
        padding: 40px;
        border-radius: 8px;
        text-align: center;
        color: #606060;
        font-family: sans-serif;
        margin: 20px 0;
    '>
        <span style='font-size: 16px;'>404</span>
        <div style='font-size: 18px; font-weight: 500; margin: 10px 0;'>
            You don't have any liked posts yet
        </div>
        <div style='font-size: 14px;'>
            Like someones post to get started
        </div>
    </div>
    """,
    unsafe_allow_html=True
)        

for post in liked_posts:
    if "photo" in post:
        create_post(post["title"], post["author"], post["content"], post["photo"], "photo", post["id"], tags=None)
    elif "video" in post:
        create_post(post["title"], post["author"], post["content"], post["video"], "video", post["id"], tags=None)    
    else:
        create_post(post["title"], post["author"], post["content"], "", "text", post["id"], tags=None)
