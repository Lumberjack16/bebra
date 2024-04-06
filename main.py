from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition, SlideTransition, SwapTransition
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy import platform
from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import pygame
import json
pygame.init()
import socket
import threading
import os

priority={"init":5,
          "donate":0,
          "update_resource":8}
path=""
if platform=="android":
    path=os.path.abspath('')+'/'
if platform=="win":
    w,h=pygame.display.Info().current_w,pygame.display.Info().current_h
    Window.size=[w/2.3,h/5*4]
    Window.left=w//2-Window.size[0]//2
    Window.top=h//2-Window.size[1]//2
import heapq
import time
all_commands=[]
resource_mining_time={}
resource_mining_time_control={}
def start_game():
    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            obj.connect(("80.77.36.110",2023))
            break
        except:
            pass
    with open(path+"file/userdata.json","r") as f:
        text=f.read()
    #text="token ({0})".format(text)
    obj.sendall(text.encode("utf-8"))
    text=json.loads(text)
    date=obj.recv(1024)
    command=json.loads(date)
    print(json.dumps(command))
    if command["action"]=="init":
        text["token"]=command["token"]
        text["id"]=command["id"]
        heapq.heappush(all_commands,(priority["init"],time.time(),command))
    elif command["action"]=="update_resource":
        heapq.heappush(all_commands,(priority["update_resource"],time.time(),command))
    #all_commands.update(command)
    with open(path+"file/userdata.json", "w") as g:
        g.write(json.dumps(text))
    #print(date.decode("utf-8"))
    obj.close()

    obj=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    while True:
        try:
            obj.connect(("80.77.36.110",2023))
            break
        except:
            pass
    command={"action":"mining_resource"}
    date=json.dumps(command)
    obj.sendall(date.encode("utf-8"))
    date=obj.recv(1024)
    time_now=time.time()
    command=json.loads(date)
    resource_mining_time.update(command)
    for res in resource_mining_time:
        resource_mining_time_control.setdefault(res,time_now)
    obj.close()


server_thread=threading.Thread(target=start_game)

fon_music=pygame.mixer.Sound("music/something_lost-185380.mp3")
file=open(path+"file/options.json","r")
options=json.loads(file.read())
file.close()
options["text_size"]=Window.size[0]/13
options["server_run"]=False
fon_music.play(-1)
fon_music.set_volume(options["volume"])

class City(Screen):
    name="city"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Місто"))
class Infrastructure(Screen):
    name="infrastructure"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Інфраструктура"))
class Army(Screen):
    name="army"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Армія"))

class Policy(Screen):
    name="policy"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Політика"))

class Trade(Screen):
    name="trade"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(Button(text="Торгівля"))

class Menu(Screen):
    name="menu"
    background_menu_pic=path+"sprites/background_menu.png"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.play=Button(text="Play",size_hint=[0.3,0.05],
        pos_hint={"center_x":0.5,"center_y":0.65},
        font_size=options["text_size"], color=[0,0,0.2],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.go_game
        )
        self.add_widget(self.play)
        self.settings=Button(text="Settings",size_hint=[0.3,0.05],
        pos_hint={"center_x":0.5,"center_y":0.55},
        font_size=options["text_size"], color=[0,0,0.2],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.go_settings
        )
        self.add_widget(self.settings)
        self.records=Button(text="Records",size_hint=[0.3,0.05],
        pos_hint={"center_x":0.5,"center_y":0.45},
        font_size=options["text_size"], color=[0,0,0.2],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.go_records
        )
        self.add_widget(self.records)
    def go_game(self,button):
        if not options["server_run"]:
            options["server_run"]=True
            server_thread.start()
        self.manager.current="game"
    def go_settings(self,button):
        self.manager.current="settings"
    def go_records(self,button):
        self.manager.current="records"
class Game(Screen):
    name="game"
    def __init__(self, **kw):
        super().__init__(**kw)
        box=BoxLayout(orientation="vertical")
        self.add_widget(box)
        panel=BoxLayout(size_hint=[1,0.2])
        box.add_widget(panel)
        menu=Button(text="Menu",
        font_size=options["text_size"], color=[1,1,0],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.go_menu
        )
        panel.add_widget(menu)
        resource=GridLayout(size_hint=[4,1],cols=7)
        ###### ресурси додатково..

        people_box=BoxLayout(orientation="vertical")
        people_image=Button(background_normal=path+"sprites/people.png",background_down=path+"sprites/people.png")
        self.people_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        people_box.add_widget(people_image)
        people_box.add_widget(self.people_text)
        resource.add_widget(people_box)

        food_box=BoxLayout(orientation="vertical")
        food_image=Button(background_normal=path+"sprites/food.png",background_down=path+"sprites/food.png")
        self.food_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        food_box.add_widget(food_image)
        food_box.add_widget(self.food_text)
        resource.add_widget(food_box)

        tree_box=BoxLayout(orientation="vertical")
        tree_image=Button(background_normal=path+"sprites/tree.png",background_down=path+"sprites/tree.png")
        self.tree_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        tree_box.add_widget(tree_image)
        tree_box.add_widget(self.tree_text)
        resource.add_widget(tree_box)

        stone_box=BoxLayout(orientation="vertical")
        stone_image=Button(background_normal=path+"sprites/stone.png",background_down=path+"sprites/stone.png")
        self.stone_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        stone_box.add_widget(stone_image)
        stone_box.add_widget(self.stone_text)
        resource.add_widget(stone_box)

        iron_box=BoxLayout(orientation="vertical")
        iron_image=Button(background_normal=path+"sprites/iron.png",background_down=path+"sprites/iron.png")
        self.iron_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        iron_box.add_widget(iron_image)
        iron_box.add_widget(self.iron_text)
        resource.add_widget(iron_box)


        gold_box=BoxLayout(orientation="vertical")
        gold_image=Button(background_normal=path+"sprites/gold.png",background_down=path+"sprites/gold.png")
        self.gold_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        gold_box.add_widget(gold_image)
        gold_box.add_widget(self.gold_text)
        resource.add_widget(gold_box)

        oil_box=BoxLayout(orientation="vertical")
        oil_image=Button(background_normal=path+"sprites/oil.png",background_down=path+"sprites/oil.png")
        self.oil_text=Button(size_hint=[1,0.15],background_normal=path+"",background_down=path+"",color=[1,0,1,1],text="-")
        oil_box.add_widget(oil_image)
        oil_box.add_widget(self.oil_text)
        resource.add_widget(oil_box)

        panel.add_widget(resource)
        box_actions=BoxLayout() # коробка для меню та вікон
        box.add_widget(box_actions)
        actions_bar=BoxLayout(orientation="vertical") # меню
        box_actions.add_widget(actions_bar)


        self.all_game_screen=ScreenManager(transition=SwapTransition(),size_hint=[4,1])
        self.all_game_screen.add_widget(City())
        self.all_game_screen.add_widget(Infrastructure())
        self.all_game_screen.add_widget(Army())
        self.all_game_screen.add_widget(Policy())
        self.all_game_screen.add_widget(Trade())
        box_actions.add_widget(self.all_game_screen)

        def go_city(button):
            self.all_game_screen.current="city"
        city_button=Button(background_normal=path+"sprites/city_icon0.png",background_down=path+"sprites/city_icon1.png",
        on_press=go_city
        )
        actions_bar.add_widget(city_button)
        def go_infrastructure(button):
            self.all_game_screen.current="infrastructure"
        infrastructure_button=Button(background_normal=path+"sprites/Infrastructure_icon0.png",background_down=path+"sprites/Infrastructure_icon1.png",
        on_press=go_infrastructure
        )
        actions_bar.add_widget(infrastructure_button)
        def go_army(button):
            self.all_game_screen.current="army"
        army_button=Button(background_normal=path+"sprites/army.png",background_down=path+"sprites/army3.png",
        on_press=go_army
        )
        actions_bar.add_widget(army_button)
        def go_policy(button):
            self.all_game_screen.current="policy"
        policy_button=Button(background_normal=path+"sprites/policy_icon0.png",background_down=path+"sprites/policy_icon1.png",
        on_press=go_policy
        )
        actions_bar.add_widget(policy_button)
        def go_trade(button):
            self.all_game_screen.current="trade"
        trade_button=Button(background_normal=path+"sprites/trade_icon0.png",background_down=path+"sprites/trade_icon1.png",
        on_press=go_trade
        )
        actions_bar.add_widget(trade_button)

        Clock.schedule_interval(self.update,1/60)
    
    def go_menu(self,button):
        self.manager.current="menu"
    def update(self,clock):
        if all_commands:
            _,_,command=heapq.heappop(all_commands)
            if command["action"]=="init" or command["action"]=="update_resource":
                self.people_text.text=str(command["people"])
                self.food_text.text=str(command["food"])
                self.tree_text.text=str(command["tree"])
                self.iron_text.text=str(command["iron"])
                self.gold_text.text=str(command["gold"])
                self.stone_text.text=str(command["stone"])
                self.oil_text.text=str(command["oil"])
        if resource_mining_time:
            pass

            

        
class MySettings(Screen):
    name="settings"
    def __init__(self, **kw):
        super().__init__(**kw)
        self.menu=Button(text="Menu",size_hint=[0.3,0.05],
        pos_hint={"center_x":0.5,"center_y":0.65},
        font_size=options["text_size"], color=[0,0,0.2],
        background_color=[0,0,0,0],font_name=options["font"],
        on_press=self.go_menu
        )
        self.add_widget(self.menu)
        slide_music=Slider(min=0,max=1,value=options["volume"],size_hint=[0.5,0.1],pos_hint={"center_x":0.5,"center_y":0.55})
        self.add_widget(slide_music)
        def sliders(button,value):
            fon_music.set_volume(value)
            file=open(path+"file/options.json","w")
            options["volume"]=value
            file.write(json.dumps(options))
            file.close()
        slide_music.bind(value=sliders)
    def go_menu(self,button):
        self.manager.current="menu"
class Records(Screen):
    name="records"
    def __init__(self, **kw):
        super().__init__(**kw)
    def go_menu(self,button):
        self.manager.current="menu"
class CivilizationApp(App):
    background_pic="sprites/fon.png"
    def build(self):
        all_windows=ScreenManager(transition=WipeTransition())
        all_windows.add_widget(Menu())
        all_windows.add_widget(Game())
        all_windows.add_widget(MySettings())
        all_windows.add_widget(Records())
        return all_windows
if __name__=="__main__":
    CivilizationApp().run()