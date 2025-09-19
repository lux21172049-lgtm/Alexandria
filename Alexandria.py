import streamlit as st
import json
from author import hash_password, autor
import random
from collections import defaultdict
import datetime
import base64
from io import BytesIO
from PIL import Image
import requests as req
from typing import Optional, Dict, Any
import uuid

# Базовый URL API на Render
API_BASE_URL = "https://alexandria-api-o9ev.onrender.com"

print('''
                            ....
                                %
                                    ^
                        L
                        "F3  $r
                        $$$$.e$"  .
                        "$$$$$"   "
    (ALEXANDRIA.  )        $$$$c  /
    .                   $$$$$$$P
    ."c                      $$$
    .$c3b                  ..J$$$$$e
    4$$$$             .$$$$$$$$$$$$$$c
    $$$$b           .$$$$$$$$$$$$$$$$r
        $$$.        .$$$$$$$$$$$$$$$$$$
        $$$c      .$$$$$$$  "$$$$$$$$$r
==============================================
[developer] => WHITEDUKE - 0xfff0800 [developer_email] => NONE) 
[developer_snapchat] => NONE
==============================================
        
''')



def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 
if 'username' not in st.session_state:
    st.session_state.username = ""

def write_all_default_api(username: str) -> bool:
    url = f"{API_BASE_URL}/write_default/posts"
    data = {
        "username": username
    } 
    resp = req.post(url, json=data)
    return resp.status_code == 200

def registration_api(username: str, password: str) -> bool:
    url = f"{API_BASE_URL}/register"
    data = {
        "username": username,
        "hash_psw": password
    }        
    resp = req.post(url, json=data)
    return resp.status_code == 200

def login_api(username: str, password: str) -> bool:
    url = f"{API_BASE_URL}/login"  
    data = {
        "username": username,
        "hash_psw": password
    }  
    resp = req.post(url, json=data)
    return resp.status_code == 200

if not st.session_state.logged_in:
    st.set_page_config(layout="wide")
    st.logo("duke.png")

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
                st.error("Fill all the field.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")       
            else:    
                api_answer = registration_api(new_username, hash_password(new_password)) 
                if not api_answer:
                    st.error("This username is already taken.")
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
                    mian = write_all_default_api(new_username)
                    if mian:
                        print("Default posts created successfully")
                    else:
                        print("Failed to create default posts")    
                    
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
st.logo("duke.png")

main_search = st.text_input(
    "Search",
    placeholder="Search...",
    label_visibility="collapsed"
)

def count_subs_of_user_(username: str) -> int:
    url = f"{API_BASE_URL}/subs/count"
    data = {"username": username}
    resp = req.post(url, json=data)
    return int(resp.text)

def gramar_transalte(count_subs: int) -> str:
    if count_subs == 0:
        return "0 subscribers"
    if count_subs == 1:
        return "1 subscriber"
    return f"{count_subs} subscribers"

def add_to_liked(author: str, post: str, title: str, username: str):
    url = f"{API_BASE_URL}/liked/posts"
    data = {
        "username": username,
        "author": author,
        "title": title,
        "post": post
    }
    res = req.post(url, json=data)
    print(f"Add to liked Status code: {res.status_code}")
    print(f"Add to liked Text: {res.text}")

def remove_from_liked(author: str, username: str, title: str, post: str):
    url = f"{API_BASE_URL}/liked/delete"
    data = {
        "username": username,
        "author": author,
        "title": title,
        "post": post
    }
    res = req.post(url, json=data)
    print(f"Remove from liked Status code: {res.status_code}")
    print(f"Remove from liked Text: {res.text}")

def create_post(title: str, author: str, content: str, files: str, type_file: str, id: str, tags=None):
    count_of_subs = count_subs_of_user_(author)
    gr = gramar_transalte(count_of_subs)
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
                margin-bottom: 5px;
            ">
                Author: {author}
            </div>
            <div style="
                color: #7f8c8d;
                font-size: 0.8em;
                margin-bottom: 15px;
            ">
                {gr}
            </div>
            <p style="color: #34495e; line-height: 1.6;">{content}</p>
            {f'<div style="margin-top: 15px; margin-bottom: 15px;">' + 
            ''.join([f'<span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' 
                    for tag in tags]) + '</div>' if tags else ''}
        </div>
        """, unsafe_allow_html=True)

    def is_subed() -> bool:
        url = f"{API_BASE_URL}/user/issubed"
        data = {
            "username": st.session_state.username,
            "creator": author
        }
        resp = req.post(url, json=data)
        print(f"IS SUBED RESULT: {resp.text}")
        return resp.json()
        
    def remove_subs():
        url_unsub = f"{API_BASE_URL}/user/unsub"
        data_unsub = {
            "username": str(st.session_state.username),
            "creator": author
        }
        resp = req.post(url_unsub, json=data_unsub)
        print(f"Unsubscribe Status: {resp.status_code}")

    def subs():
        if not is_subed():
            url = f"{API_BASE_URL}/user/sub"
            data_sub = {
                "username": str(st.session_state.username),
                "creator": author
            }
            resp = req.post(url, json=data_sub)
            print(f"Subscribe Status: {resp.status_code}")
        else:
            remove_subs()
                                
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

    def like():
        url_to_like = f"{API_BASE_URL}/like/post"
        data_like = {
            "username": st.session_state.username,
            "author": author,
            "id": id
        }
        resp = req.post(url_to_like, json=data_like)
        print(f"Like Status: {resp.status_code}")

    def dislike():
        url_to_dis = f"{API_BASE_URL}/dislike/post"
        data_dis = {
            "username": st.session_state.username,
            "author": author,
            "id": id
        }
        resp = req.post(url_to_dis, json=data_dis)
        print(f"Dislike Status: {resp.status_code}")

    col1, col2 = st.columns(2)
    
    with col1:
        st.button(
            f"👍{len(likes)}", 
            key=f"like_post_{title}_{id}",
            on_click=like
        )
    with col2:
        st.button(
            f"👎{len(dislikes)}", 
            key=f"dislike_post_{title}_{id}",
            on_click=dislike
        )
    
    if is_subed():    
        st.button("Subscribed", key=f"{title}_sub_{id}", on_click=subs)
    else:
        st.button("Subscribe", key=f"{title}_sub_{id}", on_click=subs)

def request_search_api(search: str):
    url = f"{API_BASE_URL}/search"
    data = {"search": search}
    resp = req.post(url, json=data)
    return resp.json()

def request_random_list_of_posts():
    url_random = f"{API_BASE_URL}/random/post"
    resp = req.get(url_random)
    return resp.json()

searc_count = 0
if main_search != "":
    post_search = request_search_api(main_search)
    for post in post_search:
        if "photo" in post:
            create_post(post["title"], post["author"], post["content"], post["photo"], "photo", post["id"], tags=None)
        elif "video" in post:
            create_post(post["title"], post["author"], post["content"], post["video"], "video", post["id"], tags=None)    
        else:
            create_post(post["title"], post["author"], post["content"], "", "text", post["id"], tags=None)   
    
    if searc_count == 0:
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
                <span style='font-size: 16px;'>🔍</span>
                <div style='font-size: 18px; font-weight: 500; margin: 10px 0;'>
                    Nothing found :(
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    random_posts = request_random_list_of_posts()
    for post in random_posts:
        if "photo" in post:
            create_post(post["title"], post["author"], post["content"], post["photo"], "photo", post["id"], tags=None)
        elif "video" in post:
            create_post(post["title"], post["author"], post["content"], post["video"], "video", post["id"], tags=None)    
        else:
            create_post(post["title"], post["author"], post["content"], "", "text", post["id"], tags=None)
