# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 19:03:14 2015

@author: Ron


A gui for manually tracking objects in series of images. 
"""
#import numpy as np
#import matplotlib.pyplot as plt



import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog as fd
from tkinter import messagebox as mb


def nextIm():
    '''Next image button'''
    global i
    global z
    global imagelist
    if len(imagelist) > 0:
        i=i+1
        image = Image.open(imagelist[i%len(imagelist)])
        s = image.size
        image = image.resize((int(s[0]*z),int(s[1]*z)), Image.ANTIALIAS)
        new_bird = ImageTk.PhotoImage(image)
        board.configure(image = new_bird)
        board.image = new_bird
        canvas.delete('all')
        canvas.create_image(0, 0, image=new_bird, anchor='nw')
        imName.configure(text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+' : '+imagelist[i%len(imagelist)])    
    
def prevIm():
    '''Previous image button'''
    global i
    global z
    global imagelist
    if len(imagelist) > 0:
        i=i-1
        image = Image.open(imagelist[i%len(imagelist)])
        s = image.size
        image = image.resize((int(s[0]*z),int(s[1]*z)), Image.ANTIALIAS)
        new_bird = ImageTk.PhotoImage(image)
        board.configure(image = new_bird)
        board.image = new_bird
        canvas.delete('all')
        canvas.create_image(0, 0, image=new_bird, anchor='nw')
        imName.configure(text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+' : '+imagelist[i%len(imagelist)])  

def goto():
    '''go 2 image image button'''
    global i
    global z
    global imagelist
    user_input = int(userImNumber.get())
    if len(imagelist) > user_input-1:
        i=user_input-1
        image = Image.open(imagelist[i%len(imagelist)])
        s = image.size
        image = image.resize((int(s[0]*z),int(s[1]*z)), Image.ANTIALIAS)
        new_bird = ImageTk.PhotoImage(image)
        board.configure(image = new_bird)
        board.image = new_bird
        canvas.delete('all')
        canvas.create_image(0, 0, image=new_bird, anchor='nw')
        imName.configure(text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+' : '+imagelist[i%len(imagelist)]) 
    return 
    
    
def rightKey(event):
    '''right key = next image'''
    nextIm()
    
def leftKey(event):
    '''left key = previous image'''
    prevIm()

def zoomIn(event):
    '''zoom in the image with + key'''
    global i
    global z
    global imagelist
    z = z*1.1
    image = Image.open(imagelist[i%len(imagelist)])
    s = image.size
    image = image.resize((int(s[0]*z),int(s[1]*z)), Image.ANTIALIAS)
    new_bird = ImageTk.PhotoImage(image)
    board.configure(image = new_bird)
    board.image = new_bird
    canvas.delete('all')
    canvas.create_image(0, 0, image=new_bird, anchor='nw')
    imName.configure(text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+' : '+imagelist[i%len(imagelist)])  

    
def zoomOut(event):
    '''zoom out with - key'''
    global i
    global z
    global imagelist
    z = z*0.9
    image = Image.open(imagelist[i%len(imagelist)])
    s = image.size
    image = image.resize((int(s[0]*z),int(s[1]*z)), Image.ANTIALIAS)
    new_bird = ImageTk.PhotoImage(image)
    board.configure(image = new_bird)
    board.image = new_bird
    canvas.delete('all')
    canvas.create_image(0, 0, image=new_bird, anchor='nw')
    imName.configure(text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+' : '+imagelist[i%len(imagelist)])

def location_handler(event):
    '''handling the location of the mouse pointer'''
    global i
    global tracking_dic
    global imagelist
    #x,y = int(event.x/z), int(event.y/z)
    
    x = canvas.canvasx(event.x) + int(hbar.get()[1])
    y = canvas.canvasy(event.y) + int(vbar.get()[1])
    
    Xloc.configure(text = x) 
    Yloc.configure(text = y)
    tracking_dic[i%len(imagelist)]=(x,y)
    print( x,y )
    

def motion(event):
    '''handling the location of the mouse pointer'''
    #x, y = int(event.x/z), int(event.y/z)
    x = canvas.canvasx(event.x) + int(hbar.get()[1])
    y = canvas.canvasy(event.y) + int(vbar.get()[1])
    Mousepos.configure(text = '({}, {})'.format(x, y))   

   
def set_imagelist():
    '''setting the list of images'''
    global imagelist
    global i
    i=-1
    imagelist = sorted(list(fd.askopenfilenames()))
    if len(imagelist) > 0:
        nextIm()

def clear():
    '''clear trajectory data'''
    global tracking_dic
    tracking_dic = {}

def save():
    '''save trajectory data'''
    global tracking_dic
    if len(tracking_dic)<=0:
        mb.showerror('Error', 'no data to save!')
        return
        
    f = fd.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    f.write('x \t y \t t \n')
    for k in tracking_dic.keys():
        text2save = str(tracking_dic[k][0])+'\t'+str(tracking_dic[k][1])+'\t'+str(k)+'\n'
        f.write(text2save)
    f.close()
        
def Quit():
    '''quit the app'''
    root.destroy()





if __name__ == '__main__':
    imagelist = ["bird.jpg"]
    i=0
    z = 1.0
    root = tk.Tk()
    root.geometry('860x500+320+70')
    root.title('Traking')
    
    tracking_dic = {}
    
    image = Image.open(imagelist[i])
    photo = ImageTk.PhotoImage(image)
    
    
    board = tk.Label(image=photo)
    next_button = tk.Button(root,text='Next Image', command = nextIm, width=10)
    
    frame=tk.Frame(root,width=700,height=400,bg='#6699ff')
    frame.grid(row=0,column=0)
    canvas = tk.Canvas(frame, height=400, width=700, scrollregion=(0,0,3000,3000),  bg='#99ccff')
    
    hbar=tk.Scrollbar(frame,orient='horizontal')
    hbar.pack(side='bottom',fill='x')
    hbar.config(command=canvas.xview)
    vbar=tk.Scrollbar(frame,orient='vertical')
    vbar.pack(side='right',fill='y')
    vbar.config(command=canvas.yview)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.create_image(0, 0, image=photo, anchor='nw')
    
    
    
    go2_button = tk.Button(root,text='Go 2 Image', command = goto, width=10)
    userImNumber = tk.StringVar(root)
    userImNumber.set('0')
    gotoImnuber = tk.Entry(root, width=7, textvariable=userImNumber)
    
    
    imName = tk.Label(root, text=str((i)%len(imagelist)+1)+'/'+str(len(imagelist))+
    ' : '+imagelist[i%len(imagelist)], anchor='w')
    file_button = tk.Button(root,text='Select Files',command = set_imagelist, width=10)
    clear_button = tk.Button(root,text='Clear Track', command = clear, width=10)
    save_button = tk.Button(root,text='Save Track', command = save, width=10)
    quit_button = tk.Button(root,text='Quit',command = Quit, width=10) 
    xloc = tk.Label(root,text='x:')
    yloc = tk.Label(root,text='y:')
    Xloc = tk.Label(root,text='-')
    Yloc = tk.Label(root,text='-')
    Mousepos = tk.Label(root,text=' - , - ')
    
    root.bind('<Left>', leftKey)
    root.bind('<Right>', rightKey)
    root.bind('+', zoomIn)
    root.bind('-', zoomOut)
    
    
    
    file_button.place(x=15, y=10)
    next_button.place(x=15, y=40)
    go2_button.place(x=15, y=70)
    gotoImnuber.place(x=20, y=100)
    xloc.place(x=15,y=170)
    yloc.place(x=15,y=185)
    Xloc.place(x=35,y=170)
    Yloc.place(x=35,y=185)
    Mousepos.place(x=15, y=330)
    clear_button.place(x=15, y=210)
    save_button.place(x=15, y=240)
    imName.place(x=120,y=10)
    
    #board.place(x=140, y=30)
    
    quit_button.place(x=10, y=425)#image.size[1])
    
    frame.place(x=120, y=30)
    canvas.pack(side='left', fill='both', expand=1)
    
    canvas.focus()
    #board.bind("<Button-1>", location_handler)
    
    canvas.bind("<Button-1>", location_handler)
    canvas.bind("<Motion>", motion)
    
    root.mainloop()


