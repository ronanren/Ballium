from tkinter import *
import random
import time
from winsound import *
import sys
from timeit import default_timer
import requests
import re
from tkinter import messagebox

# Modifier couleur des balles (systeme de couleur aleatoire)

fenetre = Tk()
fenetre.title("Ballium")
fenetre.geometry("450x300+400+200")
fenetre.resizable(width=False, height=False)
canvas = Canvas(fenetre, width=1000, height=600, bg="#202F3E", bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)
fenetre.configure(cursor='dot')

level = 1
speed = 0 # les % de increased (titre indicatif)
vitesse = 10 # la vitesse des balles (titre qualitatif)

def updatebdd():
    r = requests.get('https://ballium.000webhostapp.com/gestiondata.php')
    data = r.text
    pos1 = data.find('<table style')
    pos2 = data.find('<table>')
    scores = r.text[pos1:pos2]
    newscore = int(str_time)
    file = open("username.txt", "r")
    username = file.read()[0:12]
    file.close()
    pos3 = scores.find(str(username))
    score = scores[pos3:pos3 + 30]
    score = score.replace("</td>", "")
    score = score.replace("<td>", "")
    score = re.sub("\D", "", score)
    if score == "":
        score = 0
    if int(newscore) > int(score):
        print("Nouveau record !!")
        r = requests.get('https://ballium.000webhostapp.com/gestiondata.php?login=' + str(username) + '&score=' + str(newscore))
    else:
        print("Play again")

def gameover(event):
    global pp, tt2, images2, canvas, anim
    tt2 = 1
    PlaySound("Sound/GameOverYeah.wav", SND_FILENAME | SND_ASYNC)
    fenetre.bind("<Button-1>", restart)
    fenetre.unbind("<Escape>")
    fenetre.after_cancel(updatetime)
    fenetre.after_cancel(anim)
    canvas.create_image(500, 300, image=backgroundjeu)
    canvas.create_text(500, 150, fill="white", font="Impact 70", text="Game Over")
    canvas.create_text(500, 300, fill="white", font="Impact 70", text="Click to play again")
    canvas.create_text(500, 450, fill="white", font="Impact 70", text="Your score : " + str(str_time))
    updatebdd()


def restart(event):
    global tt2, level, speed
    fenetre.unbind("<Button-1>")
    fenetre.bind("<Escape>", pause)
    PlaySound("Sound/ExtraStage.wav", SND_FILENAME | SND_ASYNC)
    tt2 = 0
    level = 1
    speed = 0
    canvas.delete(ALL)
    canvas.create_image(500, 300, image=backgroundjeu)
    startTime()
    level1()
    animation()

def level1():
    global textelevel1, speed, vitesse
    x = -400
    y = -420

    color1 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    color2 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    color3 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    color4 = "#{:06x}".format(random.randint(0, 0xFFFFFF))

    if level == 1:
        textelevel1 = canvas.create_text(500, 300, fill="white", font="Impact 80 bold", text="Let's go !")
    else:
        speed = speed + 5
        vitesse = vitesse + 1
        textelevel1 = canvas.create_text(500, 300, fill="white", font="Impact 80 bold", text=str(speed) + "% increased speed")
    for i in range(0, 75):
        globals()['balle%s' % i] = canvas.create_oval(x, -700, y, -720, fill=color1)
        x = x + 20
        y = y + 20
    x, y = -400, -420
    for i in range(75, 150):
        globals()['balle%s' % i] = canvas.create_oval(x, -1000, y, -1020, fill=color2)
        x = x + 20
        y = y + 20
    x, y = -400, -420
    for i in range(150, 225):
        globals()['balle%s' % i] = canvas.create_oval(x, -1200, y, -1220, fill=color3)
        x = x + 20
        y = y + 20
    x, y = -400, -420
    for i in range(225, 300):
        globals()['balle%s' % i] = canvas.create_oval(x, -1500, y, -1520, fill=color4)
        x = x + 20
        y = y + 20
    x, y = -400, -420

    for i in range(0, 300):
        canvas.tag_bind(globals()['balle%s' % i], "<Any-Enter>", gameover)



def animation():
    global anim, level, text_clock
    w = fenetre.winfo_width()
    h = fenetre.winfo_height()
    if canvas.coords(balle50)[3] < -150:
        for i in range(0, 150):
            canvas.move(globals()['balle%s' % i], 0, random.randint(0, 40))
        for i in range(150, 300):
            canvas.move(globals()['balle%s' % i], 0, random.randint(0, 30))
    else:
        for i in range(0, 300):
            canvas.move(globals()['balle%s' % i], 0, random.uniform(0, vitesse))
    if canvas.coords(balle50)[3] > -150:
        canvas.delete(textelevel1)
    if canvas.coords(balle250)[3] > h + 250:
        level = 2
        for i in range(0, 300):
            canvas.delete(globals()['balle%s' % i])
        level1()
    anim = fenetre.after(60, animation)


def pause(event):
    global transparent, anim, continueButton, boutonquit, boutonmainmenu, pausetime, timepause
    fenetre.unbind("<Escape>")
    fenetre.unbind("<Leave>")
    fenetre.after_cancel(anim)
    fenetre.after_cancel(updatetime)
    timepause = 0
    pausetime = default_timer()
    transparent = canvas.create_image(500, 300, image=transp)
    continueButton = canvas.create_image(500, 525, image=ContinueButton)
    boutonmainmenu = canvas.create_image(200, 525, image=btnmainmenu)
    boutonquit = canvas.create_image(800, 525, image=boutonquitt)
    canvas.tag_bind(continueButton, '<Button-1>', resume)
    canvas.tag_bind(boutonquit, '<Button-1>', destroy)
    canvas.tag_bind(boutonmainmenu, '<Button-1>', backtomenu)


def resume(event):
    global timepause
    canvas.delete(transparent)
    canvas.delete(continueButton)
    canvas.delete(boutonmainmenu)
    canvas.delete(boutonquit)
    fenetre.bind("<Escape>", pause)
    fenetre.bind("<Leave>", gameover)
    timepause = default_timer() - pausetime
    updateTime()
    animation()


def updateTime():
    global updatetime, str_time, timepause, timeepause
    timeepause = timeepause + timepause
    now = default_timer() - starts - timeepause
    timepause = 0
    minutes, seconds = divmod(now, 10000)
    str_time = "%02d" % (seconds)
    canvas.itemconfigure(text_clock, text=str_time)
    updatetime = fenetre.after(1000, updateTime)

def startTime():
    global text_clock, starts, timepause, timeepause
    starts = default_timer()
    timepause = 0
    timeepause = 0
    text_clock = canvas.create_text(920, 50, fill="white", font="Impact 80 bold")
    updateTime()



def start(event):
    global tt1, speed, level
    tt1 = 0
    speed = 0
    level = 1
    PlaySound("Sound/ExtraStage.wav", SND_FILENAME | SND_ASYNC)
    fenetre.unbind("<Return>")
    fenetre.bind("<Escape>", pause)
    canvas.delete(ALL)
    fenetre.bind("<Leave>", gameover)
    canvas.create_image(500, 300, image=backgroundjeu)
    startTime()
    level1()
    animation()



def menu(event):
    global tt, tt1, giflist1, images1
    tt = 0
    fenetre.geometry("1000x600+150+80")
    canvas.delete(ALL)
    fenetre.bind("<Return>", start)
    while 1:
        for gif in giflist1:
            try:
                canvas.delete(images1)
                images1 = canvas.create_image(500, 300, image=gif)
                canvas.update()
            except TclError:
                pass
            if tt1 == 0:
                break
            time.sleep(0.03)
        if tt1 == 0:
            break


################################# MENU ################################

# Gif pour le menu
imagelist = []
for i in range(1, 16):
    imagelist.append("gif/menu/frame-" + str(i).zfill(2) + ".gif")
photo = PhotoImage(file=imagelist[0])
width = photo.width()
height = photo.height()
giflist = []
for imagefile in imagelist:
    photo = PhotoImage(file=imagefile)
    giflist.append(photo)
images = ""
tt = 1

# gif pour le jeu "Enter to start"
imagelist1 = []
for i in range(1, 16):
    imagelist1.append("gif/entertostart/frame-" + str(i).zfill(2) + ".gif")
photo1 = PhotoImage(file=imagelist1[0])
giflist1 = []
for imagefile1 in imagelist1:
    photo1 = PhotoImage(file=imagefile1)
    giflist1.append(photo1)
images1 = ""
tt1 = 1

transp = PhotoImage(file='Images/transparent.gif')
ContinueButton = PhotoImage(file='Images/ContinueButton.gif')
boutonquitt = PhotoImage(file='Images/boutonquitpause.gif')
btnmainmenu = PhotoImage(file='Images/boutonmainmenupause.gif')

# image pour le jeu "Game over"
gameoverimage = PhotoImage(file='gif/gameover.gif')
# image pour le fond d'ecran du jeu
backgroundjeu = PhotoImage(file='gif/background.gif')

# Images pour les 3 boutons (Play, Options, Quit)
photo1 = PhotoImage(file='Images/bouton_play1.gif')
photo2 = PhotoImage(file='Images/bouton_play2.gif')
button1 = canvas.create_image(66, 274, image=photo1)

photo3 = PhotoImage(file='Images/bouton_options1.gif')
photo4 = PhotoImage(file='Images/bouton_options2.gif')
button2 = canvas.create_image(225, 274, image=photo3)

photo5 = PhotoImage(file='Images/bouton_quit1.gif')
photo6 = PhotoImage(file='Images/bouton_quit2.gif')
button3 = canvas.create_image(384, 274, image=photo5)

imageRetour = PhotoImage(file='Images/bouton_BackMenu.gif')
imagechangeusername = PhotoImage(file='Images/bouton_change-username.gif')
imagechangesaving = PhotoImage(file='Images/bouton_saving-scores.gif')



# Animation pour les boutons
def button1anim1(event):
    canvas.itemconfig(button1, image=photo2)


def button1anim2(event):
    canvas.itemconfig(button1, image=photo1)


def button2anim1(event):
    canvas.itemconfig(button2, image=photo4)


def button2anim2(event):
    canvas.itemconfig(button2, image=photo3)


def button3anim1(event):
    canvas.itemconfig(button3, image=photo6)


def button3anim2(event):
    canvas.itemconfig(button3, image=photo5)


def destroy(event):
    global tt, tt1
    tt, tt1 = 0, 0
    fenetre.destroy()
    try:
        sys.exit()
    except:
        pass

def backtomenu(event):
    global tt, tt1, images
    fenetre.geometry("450x300+400+200")
    canvas.delete(ALL)

    # Animation pour les boutons
    def button1anim1(event):
        canvas.itemconfig(button1, image=photo2)

    def button1anim2(event):
        canvas.itemconfig(button1, image=photo1)

    def button2anim1(event):
        canvas.itemconfig(button2, image=photo4)

    def button2anim2(event):
        canvas.itemconfig(button2, image=photo3)

    def button3anim1(event):
        canvas.itemconfig(button3, image=photo6)

    def button3anim2(event):
        canvas.itemconfig(button3, image=photo5)

    tt = 1
    tt1 = 1
    button1 = canvas.create_image(66, 274, image=photo1)
    button2 = canvas.create_image(225, 274, image=photo3)
    button3 = canvas.create_image(384, 274, image=photo5)
    canvas.tag_bind(button1, "<Button-1>", menu)
    canvas.tag_bind(button3, "<Button-1>", destroy)
    canvas.tag_bind(button2, "<Button-1>", options)
    canvas.tag_bind(button1, "<Enter>", button1anim1)
    canvas.tag_bind(button1, "<Leave>", button1anim2)
    canvas.tag_bind(button2, "<Enter>", button2anim1)
    canvas.tag_bind(button2, "<Leave>", button2anim2)
    canvas.tag_bind(button3, "<Enter>", button3anim1)
    canvas.tag_bind(button3, "<Leave>", button3anim2)

    while 1:
        for gif in giflist:
            try:
                canvas.delete(images)
                images = canvas.create_image(width / 2.0, height / 2.0, image=gif)
                canvas.update()
            except TclError:
                pass
            if tt == 0:
                break
            time.sleep(0.08)
        if tt == 0:
            break

def changeuser():
    file = open("username.txt", "w")
    file.write(login.get())
    file.close()
    messagebox.showinfo("Info", "Your username has been changed.")
    fenetre1.destroy()


def changeusername1(event):
    global login, fenetre1
    fenetre1 = Tk()
    fenetre1.title("Change username")
    fenetre1.geometry("200x65+400+200")
    fenetre1.resizable(width=False, height=False)
    login = StringVar(fenetre1)
    entrylogin = Entry(fenetre1, textvariable=login)
    entrylogin.pack()
    file = open("username.txt", "r")
    username = file.read()[0:12]
    file.close()
    login.set(username)
    boutonchange = Button(fenetre1, text="Change username", command=changeuser)
    boutonchange.pack()
    Label(fenetre1, text="12 characters max").pack()
    fenetre1.mainloop()


def changesavingscore(event):
    global varsavescore
    fenetre1 = Tk()
    fenetre1.title("Saving score")
    fenetre1.geometry("150x60+400+200")
    fenetre1.resizable(width=False, height=False)
    file = open("optionsave.txt", "r")
    varsavescore = file.read()
    file.close()

    fenetre1.mainloop()


def options(event):
    global tt
    canvas.delete(ALL)
    tt = 0
    fenetre.config(bg="#202F3E")
    backButton = canvas.create_image(225, 274, image=imageRetour)
    canvas.tag_bind(backButton, "<Button-1>", backtomenu)
    changeusername = canvas.create_image(225,70, image=imagechangeusername)
    canvas.tag_bind(changeusername, "<Button-1>", changeusername1)

    changesaving = canvas.create_image(225, 160, image=imagechangesaving)
    canvas.tag_bind(changesaving, "<Button-1>", changesavingscore)



# Assignement des boutons pour leurs actions/animations
canvas.tag_bind(button1, "<Button-1>", menu)
canvas.tag_bind(button3, "<Button-1>", destroy)
canvas.tag_bind(button2, "<Button-1>", options)
canvas.tag_bind(button1, "<Enter>", button1anim1)
canvas.tag_bind(button1, "<Leave>", button1anim2)
canvas.tag_bind(button2, "<Enter>", button2anim1)
canvas.tag_bind(button2, "<Leave>", button2anim2)
canvas.tag_bind(button3, "<Enter>", button3anim1)
canvas.tag_bind(button3, "<Leave>", button3anim2)

# Animation du gif du menu
while 1:
    for gif in giflist:
        try:
            canvas.delete(images)
            images = canvas.create_image(width / 2.0, height / 2.0, image=gif)
            canvas.update()
        except TclError:
            pass
        if tt == 0:
            break
        time.sleep(0.08)
    if tt == 0:
        break




fenetre.mainloop()
