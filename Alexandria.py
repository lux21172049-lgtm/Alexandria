import streamlit as st
import json
from author import hash_password,autor
import random
from collections import defaultdict
import datetime
import base64
from io import BytesIO
from PIL import Image
import requests as req



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



st.logo("duke.png")

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
    
    
if not st.session_state.logged_in:
    # Переключатель между формами входа и регистрации    
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
            background-attachment: fixed;  # Фиксирует фон при прокрутке
        }
        </style>
        """,
        unsafe_allow_html=True
    )    
    if st.session_state.show_register:
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
        st.title("🔒 Вход")
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
st.logo("duke.png")
main_search = st.text_input("",placeholder = "Search")



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

#Creating the cookies for the posts
            # Останавливаем приложение, если куки не загружены
  

# function for counting subscribers of a user
def count_subs_of_user_(username:str) -> int:
    with open("pages/posts.json","r") as file:
        data = json.load(file)

    for user in data:
        if user["username"] == username:
            try:
                return len(user["subscribers"])
            except Exception as e:
                return 0


def gramar_transalte(count_subs:int) -> str:
    if count_subs == 0:
        return "0 подписчиков"
    if count_subs == 1:
        return "1 подписчик"
    if 2 <= count_subs <= 4:
        return f"{count_subs} подписчика"
    return f"{count_subs} подписчиков"



def create_post(title, author, content,likes, tags=None):
    
    count_of_subs = count_subs_of_user_(author)
    gr = gramar_transalte(count_of_subs)
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
                margin-bottom: 5px;
            ">
                Автор: {author}
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
        with open("pages/posts.json","r") as file:
            s = json.load(file)
        for user in s:
            if user["username"] == author:
                if st.session_state.username in user["subscribers"]:
                    return True
        return False  
    def remove_subs():
        with open("pages/posts.json","r") as file:
            s = json.load(file)
        for user in s:
            if user["username"] == author:
                if st.session_state.username in user["subscribers"]:
                    new_subs = []
                    for sub in user["subscribers"]:
                        if sub != st.session_state.username:
                            new_subs.append(sub) 
                    user["subscribers"] = new_subs
                    with open("pages/posts.json","w") as file:
                        json.dump(s,file,indent=2)



    def subs():
        if not is_subed():
            with open("pages/posts.json","r") as file:
                sub = json.load(file)
            for user in sub:
                if user["username"] == author:
                    if st.session_state.username not in user["subscribers"]:
                        user["subscribers"].append(st.session_state.username) 
                        with open("pages/posts.json",'w') as file:
                            json.dump(sub,file)
        else:
            remove_subs()
                                
                            

    

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
       # except Exception as e:
            #print(f"Error video {e}")
    #except Exception as e:
        #print("Error")         

      

    # Инициализация состояний
   
    def like():
        with open("pages/likes.json","r") as file:
            data = json.load(file)
        pos_ex = False
        for post in data:
            if post["post_title"] == title:
                pos_ex = True
        if pos_ex:
            for post in data:
                if post["post_title"] == title:
                    if st.session_state.username not in post["likes"] and st.session_state.username not in post["dislikes"]:
                        post["likes"].append(st.session_state.username)
                        
                    elif st.session_state.username not in post["likes"] and st.session_state.username in post["dislikes"]:
                        y = post["dislikes"].index(st.session_state.username)
                        post["dislikes"].pop(y)
                        post["likes"].append(st.session_state.username)
                        
                    elif st.session_state.username in post["likes"] and st.session_state.username not in post["dislikes"]:
                        t = post["likes"].index(st.session_state.username)
                        post["likes"].pop(t)
                        
                    with open("pages/likes.json","w") as file:
                        json.dump(data,file) 
        else:
            st.error("Nothing")                   



    def dislike():
        with open("pages/likes.json","r") as file:
            data = json.load(file)
        pos_ex = False
        for post in data:
            if post["post_title"] == title:
                pos_ex = True
        if pos_ex:
            for post in data:
                if post["post_title"] == title:
                    if st.session_state.username not in post["likes"] and st.session_state.username not in  post["dislikes"]:
                        post["dislikes"].append(st.session_state.username)
                    elif st.session_state.username not in post["dislikes"] and st.session_state.username in post["likes"]:
                        g = post["likes"].index(st.session_state.username)
                        post["likes"].pop(g)
                        post["dislikes"].append(st.session_state.username) 
                    elif st.session_state.username in post["dislikes"] and st.session_state.username not  in post["likes"]:
                        h = post["dislikes"].index(st.session_state.username)
                        post["dislikes"].pop(h)


                    with open("pages/likes.json","w") as file:
                        json.dump(data,file)     




                



    def update_post_reaction():
        try:
            # Загружаем данные один раз
            with open("pages/posts.json", "r") as file:
                data_posts = json.load(file)
            
            # Находим нужный пост
            for user in data_posts:
                if user["username"] == author:
                    title_index = user["titles"].index(title)
                    # Обновляем данные в файле
                    user["likes"][title_index] = f"{st.session_state[f'post_{title}_likes']} {st.session_state[f'post_{title}_dislikes']}"
                    break
            
            # Сохраняем изменения
            with open("pages/posts.json", "w") as file:
                json.dump(data_posts, file, indent=2)
            
           
            
        except Exception as e:
            st.error(f"Ошибка при обновлении: {str(e)}")

    

    # Отображение кнопок
    col1, col2 = st.columns(2)
    with open("pages/likes.json","r") as file:
        data_like = json.load(file)
    f = 0 # likes
    k = 0 # dislikes
    for post in data_like:
        if post["post_title"] == title:
            f = len(post["likes"])
            k = len(post["dislikes"])  
    #st.session_state[f'post_{title}_likes']  
    # st.session_state[f'post_{title}_dislikes']       
    with col1:
        st.button(
            f"👍{f}", 
            key=f"like_post_{title}",
            on_click=like
        )
    with col2:
        st.button(
            f"👎{k}", 
            key=f"dislike_posts{title}",
            on_click=dislike
        )
    with open("pages/posts.json",'r') as file:
        sb = json.load(file)
    for user in sb:
        if user["username"] == author:
            if st.session_state.username in user["subscribers"]:    
                sub_btn = st.button("Вы подписаны",key = f"{title}_sub",on_click = subs)
            else:
                sub_btn = st.button("Подписаться",key = f"{title}_sub",on_click = subs)
                    

        
        
        
    
    
with open("pages/posts.json",'r') as file:
        ps = json.load(file)
user_ex = False        
for user in ps:
    if user["username"] == st.session_state.username:
        user_ex = True
if not user_ex:                
    ps.append({
        "username":st.session_state.username,
        "posts":[],
        "titles":[],
        "likes":[],
        "photos":{},
        "subscribers":[],
        "videos":{}
    })  
    with open("pages/posts.json","w") as file:
        json.dump(ps,file,indent=2,ensure_ascii=False)      

with open('pages/posts.json',"r") as file:
    lenta = json.load(file)


                           
usernames = []
titles = []
posts = [] 
usernames = []


with open("pages/posts.json","r") as file:
    j = json.load(file)
for user in j:
    usernames.append(user["username"]) 

 
for i in data["lm"]:
    print(i) 

def recomaendation():
    with open("pages/posts.json","r") as file:
        data_posts = json.load(file)
    for user in data_posts:
        if st.session_state.username in user["subscribers"]:
            with open("pages/user_properities.json","r") as file:
                props = json.load(file)
            if st.session_state.username not in props:
                props[st.session_state.username] = [] 
                with open("pages/user_properities.json","w") as file:
                    json.dump(props,file,indent=2)
            with open("pages/user_properities.json","r") as file:
                p = json.load(file)
            seen = []    
            
            if user["username"] not in seen:
                seen.append(user["username"])
                p[f"{st.session_state.username}"].append(user["username"])  
            with open("pages/user_properities.json","w") as file:
                json.dump(p,file,indent=2)


recomaendation()


for user in usernames:
    if main_search != "":
        try:
            for title in data[user][0]:
                if main_search.lower() in title.lower() or title.lower() in main_search.lower() or (main_search.lower() in user.lower() or user.lower() in main_search.lower()):
                    t_i = data[user][0].index(title)
                    
                    create_post(title,user,data[user][1][t_i],data[user][-2],tags = None)
                    st.divider()
        except Exception as e:
            print(f"Exception {e}")        
    else:
        try:
            title = random.choice(data[user][0])
            t_i_i = data[user][0].index(title)
            
            create_post(title,user,data[user][1][t_i_i],data[user][-2],tags = None)        
            st.divider()
        except Exception as e:
            print(f"Exception{e}")        


def test():
    assert recomaendation()
    assert create_post("test","test","test",[1,2],tags = None)
    assert register_user("test","test")
