from tkinter import * 
import random
import time
from winsound import *


fenetre = Tk() 
fenetre.title("Ballium") 
fenetre.geometry("450x300+400+200")
fenetre.resizable(width=False,height=False)
canvas = Canvas(fenetre, width = 1000, height = 600,bg="#202F3E", bd=0, highlightthickness=0) 
canvas.pack(fill="both", expand=True)
fenetre.configure(cursor='dot')


level = 1
def gameover(event):
    global pp, tt2, images2, canvas, anim
    tt2 = 1
    PlaySound("Sound/GameOverYeah.wav", SND_FILENAME | SND_ASYNC)
    fenetre.bind("<Button-1>", restart)
    fenetre.unbind("<Escape>")
    fenetre.after_cancel(anim)
    canvas.create_image(500,300, image=gameoverimage)
       
        


    

def restart(event):
    global tt2, level
    fenetre.unbind("<Button-1>")
    fenetre.bind("<Escape>", pause)
    PlaySound("Sound/ExtraStage.wav", SND_FILENAME | SND_ASYNC)
    tt2 = 0
    level = 1
    canvas.delete(ALL)
    canvas.create_image(500,300, image=backgroundjeu)
    level1()
    animation()
 
def level1():
    global textelevel1
    x = -400
    y = -420
    textelevel1 = canvas.create_text(500,300,fill="white",font="Impact 80 bold", text="LEVEL 1")
    for i in range(0, 75):
        globals()['balle%s' % i] = canvas.create_oval(x,-400,y,-420, fill='#C180FE')
        x = x + 20
        y = y + 20
    x, y = -400, -420
    for i in range(75, 150):
        globals()['balle%s' % i] = canvas.create_oval(x,-800,y,-820, fill='#54C5F3')
        x = x + 20
        y = y + 20
    x, y = -400, -420


    for i in range(0, 150):
        canvas.tag_bind(globals()['balle%s' % i], "<Any-Enter>", gameover)
    


def level2():
    global textelevel2
    x = -400
    y = -420
    canvas.delete(ALL)
    canvas.create_image(500,300, image=backgroundjeu)
    textelevel2 = canvas.create_text(500,300,fill="white",font="Impact 80 bold", text="LEVEL 2")
    for i in range(0, 100):
        globals()['balle%s' % i] = canvas.create_oval(x,-400,y,-420, fill='#C180FE')
        x = x + 20
        y = y + 20
    for i in range(0, 100):
        canvas.tag_bind(globals()['balle%s' % i], "<Any-Enter>", gameover)


def animation():
    global anim, level
    w = fenetre.winfo_width() 
    h = fenetre.winfo_height()
    if level == 1:
        for i in range(0, 150):
            canvas.move(globals()['balle%s' % i],0,random.randint(0,10)) 
        if canvas.coords(balle50)[3] > -200:
            canvas.delete(textelevel1)
        if canvas.coords(balle100)[3] > h + 400:
            level += 1
            level2()
    if level == 2:
        for i in range(0, 100):
            canvas.move(globals()['balle%s' % i],0,random.randint(0,11))
        if canvas.coords(balle50)[3] > -200:
            canvas.delete(textelevel2)

    anim = fenetre.after(30, animation)


def continu(event):
    canvas.delete(transparent)
    fenetre.bind("<Escape>", pause)
    fenetre.unbind("<c>")
    animation()


def pause(event):
    global transparent, anim
    fenetre.unbind("<Escape>")
    fenetre.unbind("<Leave>")
    fenetre.after_cancel(anim)
    transparent = canvas.create_image(500,300, image=transp)
    fenetre.bind("<c>", continu)


def start(event):
    global tt1
    tt1 = 0
    PlaySound("Sound/ExtraStage.wav", SND_FILENAME | SND_ASYNC)
    fenetre.unbind("<Return>")
    fenetre.bind("<Escape>", pause)
    canvas.delete(ALL)
    fenetre.bind("<Leave>", gameover)
    canvas.create_image(500,300, image=backgroundjeu)
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
                images1 = canvas.create_image(500,300, image=gif)
                canvas.update()
            except TclError:
                pass
            if tt1 == 0: 
                break
            time.sleep(0.03)
        if tt1 == 0:
            break
    



################################# MENU ################################

#Gif pour le menu
imagelist = []
for i in range(1,16):
    imagelist.append("gif/menu/frame-" +str(i).zfill(2) + ".gif")
photo = PhotoImage(file=imagelist[0])
width = photo.width()
height = photo.height()
giflist = []
for imagefile in imagelist:
    photo = PhotoImage(file=imagefile)
    giflist.append(photo)
images = ""
tt = 1

#gif pour le jeu "Enter to start"
imagelist1 = []
for i in range(1,16):
    imagelist1.append("gif/entertostart/frame-" +str(i).zfill(2) + ".gif")
photo1 = PhotoImage(file=imagelist1[0])
giflist1 = []
for imagefile1 in imagelist1:
    photo1 = PhotoImage(file=imagefile1)
    giflist1.append(photo1)
images1 = ""
tt1 = 1

transp = PhotoImage(file ='Images/transparent.gif')


#image pour le jeu "Game over"
gameoverimage = PhotoImage(file ='gif/gameover.gif')
#image pour le fond d'ecran du jeu
backgroundjeu = PhotoImage(file = 'gif/background.gif')

#Images pour les 3 boutons (Play, Options, Quit)
photo1 = PhotoImage(file = 'Images/bouton_play1.gif')
photo2 = PhotoImage(file = 'Images/bouton_play2.gif')
button1 = canvas.create_image(66,274, image=photo1)

photo3 = PhotoImage(file = 'Images/bouton_options1.gif')
photo4 = PhotoImage(file = 'Images/bouton_options2.gif')
button2 = canvas.create_image(225,274, image=photo3)

photo5 = PhotoImage(file = 'Images/bouton_quit1.gif')
photo6 = PhotoImage(file = 'Images/bouton_quit2.gif')
button3 = canvas.create_image(384,274, image=photo5)


#Animation pour les boutons
def button1anim1(event):
    canvas.itemconfig(button1, image = photo2)
def button1anim2(event):
    canvas.itemconfig(button1, image = photo1)

def button2anim1(event):
    canvas.itemconfig(button2, image = photo4)
def button2anim2(event):
    canvas.itemconfig(button2, image = photo3)

def button3anim1(event):
    canvas.itemconfig(button3, image = photo6)
def button3anim2(event):
    canvas.itemconfig(button3, image = photo5)

def destroy(event):
    fenetre.destroy()


#Assignement des boutons pour leurs actions/animations
canvas.tag_bind(button1, "<Button-1>", menu)
canvas.tag_bind(button3, "<Button-1>", destroy)

canvas.tag_bind(button1, "<Enter>", button1anim1)
canvas.tag_bind(button1, "<Leave>", button1anim2)
canvas.tag_bind(button2, "<Enter>", button2anim1)
canvas.tag_bind(button2, "<Leave>", button2anim2)
canvas.tag_bind(button3, "<Enter>", button3anim1)
canvas.tag_bind(button3, "<Leave>", button3anim2)


#Animation du gif du menu
while 1:
    for gif in giflist:
        try:
            canvas.delete(images)
            images = canvas.create_image(width/2.0, height/2.0, image=gif)
            canvas.update()
        except TclError:
            pass
        if tt == 0: 
            break
        time.sleep(0.08)
    if tt == 0:
        break


fenetre.mainloop()