import streamlit as st
import json
from author import hash_password,autor
from datetime import datetime
from collections import defaultdict
import random
import base64
from io import BytesIO
from PIL import Image
import pytest
import requests as req



st.logo("duke.png")


def register_user(username, password):
    if 'users' not in st.session_state:
        st.session_state.users = {}
    st.session_state.users[username] = password
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False 
    
    

if not st.session_state.logged_in:
    # Переключатель между формами входа и регистрации    
        
    if st.session_state.show_register:
        st.logo("duke.png")
        st.title("📝 Регистрация")
        new_username = st.text_input("Новый логин", key="reg_user")
        new_password = st.text_input("Новый пароль", type="password", key="reg_pass1")
        confirm_password = st.text_input("Повторите пароль", type="password", key="reg_pass2")
        
        if st.button("Зарегистрироваться"):
            with open('user2.json','r') as file:
                print('Test base working')
                d = json.load(file)
                
            # проверяю еслть ли такой пользователб или нет    
            if new_username in d:
                st.error('This username is already taken')
            else:   
                if not new_username or not new_password:
                    st.error("Заполните все поля")
                elif new_password != confirm_password:
                    st.error("Пароли не совпадают!")
                else:
                    register_user(new_username, new_password)
                    url = "http://0.0.0.0:8000/load/default/videos"
                    data = {
                        "username":new_username
                    }
                    resp = req.post(url,json = data)
                    print(f"Satus code : {resp.status_code}")
                    print(f"Text : {resp.text}")
                    st.success("Регистрация успешна! Можете войти")
                    st.session_state.show_register = False
                    with open('user2.json','r', encoding="utf-8") as file:
                        data = json.load(file)
                        
                    data[new_username] = hash_password(new_password) # записываем нового пользователя 
                   
                    
                    # Запись в базу нового пользователя (уже обновляем базу)
                    with open('user2.json','w', encoding="utf-8") as file:
                        json.dump(data,file,indent=4, ensure_ascii=False)
                        
                        
                        
                    
        if st.button("← Назад к входу"):
            st.session_state.show_register = False
            st.rerun()
    
    else:
        # Форма входа
        st.logo("duke.png")
        st.title("🔒 Вход в систему")
        username = st.text_input("Логин")
        password = st.text_input("Пароль", type="password")
        us2 = username
        if st.button("Войти"):
            # Проверяю на подписку
            if autor(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Неверные данные")
        if st.button("Создать новый аккаунт"):
            st.session_state.show_register = True
            st.rerun()
    
    st.stop()
# Основной интерфейс после авторизации
st.success(f"✅ Welcome to Alexandria, {st.session_state.username}!")        






def count_subs() -> int:
    with open("pages/posts.json",'r') as file:
        subs = json.load(file)
    for user in subs:
        if user["username"] == st.session_state.username:
            return len(user["subscribers"])


with open("pages/posts.json","r") as file:
    bd = json.load(file)


data = defaultdict(list)

for user in bd:
    if user["username"] != "":
        t2 = []
        p2 = []
        for i in user["titles"]:
            if i not in t2:
                t2.append(i)
        for i in user["posts"]:
            if i not in p2:
                p2.append(i)        
        data[user["username"]].append(t2)
        data[user["username"]].append(p2)
        data[user["username"]].append(user["username"])
        data[user["username"]].append(user["likes"])
        data[user["username"]].append(user["photos"])
        data[user["username"]].append(user["videos"])


russian_government_surnames = [
    # Президенты
    "путин", "Путин", "ПУТИН",
    "putin", "Putin", "PUTIN",

    # Премьер‑министр
    "мишинестин", "Мишустин", "МИШУСТИН",
    "mishustin", "Mishustin", "MISHUSTIN",

    # Директор ФСБ
    "бортников", "Бортников", "БОРТНИКОВ",
    "bortnikov", "Bortnikov", "BORTNIKOV",

    # Пресс‑секретарь президента
    "песков", "Песков", "ПЕСКОВ",
    "peskov", "Peskov", "PESKOV",

    # Министры (пример)
    "кологольцев", "Колокольцев", "КОЛОКОЛЬЦЕВ",  # МВД
    "kolokoltsev", "Kolokoltsev", "KOLOKOLTSEV",

    "чуйченко", "Чуйченко", "ЧУЙЧЕНКО",  # юстиции
    "chuychenko", "Chuychenko", "CHUYCHENKO",

    "лавров", "Лавров", "ЛАВРОВ",  # иностранных дел
    "lavrov", "Lavrov", "LAVROV"
]


def cens(title:str,content:str) -> bool:
    if title in russian_government_surnames or content in russian_government_surnames:
        return False
    return True


def create_post(title, author, content,tags=None):
    """
    Создает красивый пост в Streamlit с заданными параметрами, включая кнопки лайка/дизлайка
    
    Параметры:
    - title: заголовок поста
    - author: автор поста
    - content: содержание поста
    - tags: список тегов (необязательный)
    """
    if tags is None:
        tags = []
    
    # Создаем уникальные ключи для счетчиков на основе заголовка
    
    
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
            Автор: {author}
        </div>
        <p style="color: #34495e; line-height: 1.6;">{content}</p>
        {f'<div style="margin-top: 15px; margin-bottom: 15px;">' + 
         ''.join([f'<span style="background: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 12px; margin-right: 5px; font-size: 0.8em;">{tag}</span>' 
                 for tag in tags]) + '</div>' if tags else ''}
    </div>
    """, unsafe_allow_html=True)
    
            
    def delete_post_from_user():
        with open("pages/posts.json",'r') as file:
            data = json.load(file)
        for user in data:
            if user["username"] == author:
                try:
                    post_index = user["titles"].index(title)
                    user["titles"].pop(post_index)
                    user["posts"].pop(post_index)
                    user["likes"].pop(post_index)
                    try:
                        user["photos"].pop(title)
                    except Exception as e:
                        print("This post doesnt have a photo on it") 
                    try:
                        user["videos"].pop(title)
                    except Exception as e:
                        print(f"Vide delte exc: {e}")        
                    st.success("Success, post deleted")       
                except Exception as e:
                    st.error(f"Something went wrong,error {e}")         
        with open("pages/posts.json","w") as file:
            json.dump(data,file)
                    

    

    with open("pages/posts.json",'r') as file:
        pictures = json.load(file)
    try:
        pict = data[author][-2]
        try:
            decoded_img = base64.b64decode(pict[title])
            img = Image.open(BytesIO(decoded_img))
            st.image(img)
        
        except Exception as e:
            print(f"Exceptrion proto {e}")    
    except Exception as e:
        print(f"Exception photos {e}")    



    def show_video_from_api() -> str:
        url = "http://0.0.0.0:8000/get/video"
        data = {
            "username":st.session_state.username,
            "title":title
        }
        resp  = req.post(url,json = data)
        return str(resp.text)
    
    encoded_video_from_api = show_video_from_api()
    try:
        vide_byes_2 = base64.b64decode(encoded_video_from_api)
        st.video(vide_byes_2)
    except Exception as e:
        print("#########################")
        print(f"Exception as {e}")  
        print("#########################")     

    #try:
        #vid = data[author][-1]
        
       # try:
            #video_bytes = base64.b64decode(vid[title])
            #st.video(video_bytes)
           # try:
                #st.video(video_bytes)
           # except Exception as e:
                #raise
       # except Exception as e:
           # raise
   # except Exception as e:
       # print("Error")           

    # Кнопки лайка и дизлайка в одной строке
    
    with open("pages/likes.json","r") as file:
        data_like = json.load(file)
    f = 0 # likes
    k = 0 # dislikes
    for post in data_like:
        if post["post_title"] == title:
            f = len(post["likes"])
            k = len(post["dislikes"])  
    
    col1, col2 = st.columns(2)  # Делим строку на 2 колонки

    with col1:
        like_btn = st.button(f"👍{f}", key=f"like_{title}")


    with col2:
        #dislike_btn = st.button(f"👎{st.session_state[f"dislikes_{title}"]}",key = f"dislike_{title}")
        dislike_btn = st.button(f"👎{k}", key=f"dislike_{title}")
    delete_post = st.button("Delete post",key = f"{title}_delete",on_click=delete_post_from_user)
            

        
    
    
st.title(st.session_state.username)

subs = count_subs()


st.markdown(
    f"<span style='display:inline-block;background-color:#e0e0e0;color:#333;padding:4px 12px;border-radius:12px;font-size:14px;font-weight:bold;'>{subs} subscribers</span>",
    unsafe_allow_html=True
)

def exi():
    st.session_state.logged_in = False


def _SAFE_VIDEO(title:str,author:str,video_coded):
    with open("pages/posts.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == author:
            user["videos"][title] =  video_coded
    with open("pages/posts.json","w") as file:
        json.dump(data,file)




def safe_video(username:str,title:str,encoded_video):
    url = "http://0.0.0.0:8000/write/video/user"
    data = {
        "username":username,
        "code":encoded_video,
        "title":title
    }
    resp = req.post(url,json = data)
    print(f"Status code : {resp}")
    print(f"Text : {resp.text}")
    print(f"Json : {resp.json}")

def get_request(url:str,title:str):
    try:
        res = req.get(f"{url}/load_video/{title}")
        data = res.json()
        if "video_base64" in data:
            video = base64.b64decode(data["video_base64"])
            st.video(video)
    except Exception as e:
        return f"There was an error sending get request to the API, error : {e}"      

with st.sidebar:
    exit_button = st.button("Leave",on_click = exi)

  


with st.form("Create Post"):
    title = st.text_input("Title for the post",placeholder="Create a title")
    post = st.text_input("Make a post",placeholder="Today i...")
    uploaded_file = st.file_uploader("Add a photo?", type=["jpg", "png", "jpeg","mp4"])

    confirm_post = st.form_submit_button("Create")

    with open("pages/posts.json",'r') as file:
            ps = json.load(file)

    seen = []    
    titles = []    
    if confirm_post:
        if cens(title,post):
            for user in ps:
                if st.session_state.username == user["username"]:
                    for i in user["posts"]:
                        if i not in seen:
                            seen.append(i)
                    for j in user["titles"]:
                        if j not in titles:
                            titles.append(j)                
            d = datetime.now()
            f = str(d).split()[0]           
            if post != "":
                for i in ps:
                    if st.session_state.username == i["username"]:
                        try:
                            if post != "":
                                i["posts"].append(post)
                            else:
                                st.error("Post is empty")    
                            if title != "":    
                                i["titles"].append(title)
                            else:
                                st.error("Title is empty")    
                            i["likes"].append("0 0")
                            if uploaded_file:
                                if "mp4" in uploaded_file.name:
                                    vd = uploaded_file.read()
                                    encoded_video = base64.b64encode(vd).decode("utf-8")
                                    try:
                                        _SAFE_VIDEO(title,st.session_state.username,encoded_video)
                                        try:
                                            safe_video(st.session_state.username,title,encoded_video)
                                        except Exception as e:
                                            print(f"Error sending post request {e}")   
                                    except Exception as e:
                                        continue   

                                else:
                                    encoded_image = base64.b64encode(uploaded_file.read()).decode("utf-8")
                                    i["photos"][f"{title}"] = encoded_image
                            with open("pages/likes.json","r") as file:
                                l = json.load(file)
                            post_ex = False
                            if not post_ex:
                                l.append({
                                    "post_title":title,
                                    "likes":[],
                                    "dislikes":[]
                                })
                                with open("pages/likes.json","w") as file:
                                    json.dump(l,file,indent=2,ensure_ascii=False)

                            st.success("Post created.Reload the page.")
                        except Exception as e:
                            st.error(f"Test error {e}")    
                        
                with open("pages/posts.json",'w') as file:
                    json.dump(ps,file,indent=2)        
                seen.append(post)    
        else:
            st.error("Вам лучше переписать пост.")             

st.markdown(
    f"<span style='display:inline-block;background-color:#e0e0e0;color:#333;padding:4px 12px;border-radius:12px;font-size:14px;font-weight:bold;'>Your posts:</span>",
    unsafe_allow_html=True
)






s_posts = [] # посты которые мы уже создали
for i in data[st.session_state.username]:
    for title in data[st.session_state.username][0]:
        if title not in s_posts:
            t_i = data[st.session_state.username][0].index(title)
           # here is the fucking bug with te index #FIXME
            
            create_post(title,st.session_state.username,data[st.session_state.username][1][t_i],tags = None)
            st.divider()
            s_posts.append(title)


