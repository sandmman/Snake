import Tkinter
import tkMessageBox
import tkFont
import random
import copy
import time

board = []
size = 0
app = 0
color = ["black","red","blue","green yellow","light slate gray","yellow","purple","deep pink","orange","chartreuse","gold","magenta"]

class Snake(Tkinter.Tk):
    def __init__(self,parent):
        global size
        Tkinter.Tk.__init__(self, parent)
      #self.configure(bg="Black")

        self.s = size/15
        self.speed = 0
        self.snake = []
        self.food = [0,0]
        self.direction = [False,False,False,True] #[up,down,left,right]

        self.label = ""
        self.button = ""
        self.button1 = ""
        self.button2 = ""
        self.img= ""

        self.board_color = color[random.randint(0,len(color)-1)]
        self.food_color  = color[random.randint(0,len(color)-1)]
        self.snake_color = color[random.randint(0,len(color)-1)]

        self.title_page()

    def title_page(self):
        global size

        title = Tkinter.StringVar()
        self.configure(bg="white")
        self.label = Tkinter.Label(self, textvariable=title,font=(list(tkFont.families())[random.randint(0,100)],32,"bold","underline"), fg=self.snake_color)
        self.label.grid(column=1,row=0)
        title.set("SNAKE");

        card = Tkinter.PhotoImage(file="/Users/aaronliberatore/Documents/snake/snake/turtle.gif")
        self.img = Tkinter.Label(self, image=card)
        self.img.image = card
        self.img.grid(column=1,row=2)

        self.columnconfigure(0,minsize=(size / 3))
        self.columnconfigure(1,minsize=(size / 3))
        self.columnconfigure(2,minsize=(size / 3))

        self.button = Tkinter.Button(self,text="Slow!", command=self.slow)
        self.button.grid(column=0,row=3)

        self.button1 = Tkinter.Button(self,text="Medium!", command=self.medium)
        self.button1.grid(column=1,row=3)

        self.button2 = Tkinter.Button(self,text="Fast!", command=self.fast)
        self.button2.grid(column=2,row=3)

    def slow(self):
        self.speed = 150
        self.initialize()
    def medium(self):
        self.speed = 100
        self.initialize()
    def fast(self):
        self.speed = 50
        self.initialize()

    def run(self):
        self.after(self.speed, self.move)

    def initialize(self):
         global board
         global color

         self.label.destroy()
         self.button.destroy()
         self.button1.destroy()
         self.button2.destroy()
         self.img.destroy()

         board = []
         self.build_board()

         """Snake Setup"""
         self.canvas.itemconfig(self.rect[0,0],fill=self.snake_color)
         self.snake.append([0,0])

         """Food Setup"""
         self.food[0] = random.randint(1,self.s - 1)
         self.food[1] = random.randint(1,self.s - 1)
         self.canvas.itemconfig(self.rect[self.food[0],self.food[1]],fill=self.food_color)

         """Bind Keys """
         self.bind_all('<Key>', self.keyPressed)

         """Play"""
         self.run()

    def build_board(self):
        global size

        self.canvas = Tkinter.Canvas(self, width=size, height=size, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 5
        self.columns = 5
        self.cellwidth = 15
        self.cellheight = 15

        self.rect = {}
        for column in range(self.s):
            for row in range(self.s):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill=self.board_color, tags="rect")

    def check_crash(self,head):
        # check_crash into a wall
        if head[0] > self.s - 1 or head[1] > self.s - 1 or head[0] < 0 or head[1] < 0:
            tkMessageBox.showinfo(title="Game over", message = "Score = " + str(len(self.snake)))
            time.sleep(2)
            self.quit()
        for x in self.snake:
            if x[0] == head[0] and x[1] == head[1]:
                tkMessageBox.showinfo("Game over", message = "Score = " + str(len(self.snake)))
                time.sleep(2)
                self.quit()

    def move(self):
        if self.direction[0]:
            head = [self.snake[0][0],self.snake[0][1]-1]
        elif self.direction[1]:
            head = [self.snake[0][0],self.snake[0][1]+1]
        elif self.direction[2]:
            head = [self.snake[0][0]-1,self.snake[0][1]]
        elif self.direction[3]:
            head = [self.snake[0][0]+1,self.snake[0][1]]
        self.check_crash(head)
        self.update_snake(head)
        self.run()

    def keyPressed(self,event):
        if event.keysym == 'Escape':
            root.destroy()
        elif event.keysym == 'Right':
            head = [self.snake[0][0]+1,self.snake[0][1]]
            self.direction = [False,False,False,True]
        elif event.keysym == 'Left':
            head = [self.snake[0][0]-1,self.snake[0][1]]
            self.direction = [False,False,True,False]
        elif event.keysym == 'Up':
            head = [self.snake[0][0],self.snake[0][1]-1]
            self.direction = [True,False,False,False]
        elif event.keysym == 'Down':
            head = [self.snake[0][0],self.snake[0][1]+1]
            self.direction = [False,True,False,False]
        else:
            return
        self.check_crash(head)
        self.update_snake(head)

    def update_snake(self,head):
        global app
        self.snake = [head] + self.snake

        if self.snake[0][1] == self.food[0] and self.snake[0][0] == self.food[1]:
            app.title("Snake - Score: " + str(len(self.snake)))

            while [self.food[1],self.food[0]] in self.snake:
                self.food[0] = random.randint(0,self.s - 1)
                self.food[1] = random.randint(0,self.s - 1)

            self.canvas.itemconfig(self.rect[self.food[0],self.food[1]],fill=self.food_color)

        else:
            self.canvas.itemconfig(self.rect[self.snake[-1][1],self.snake[-1][0]],fill=self.board_color)
            self.snake.pop(len(self.snake)-1)

        for i in range(len(self.snake)):
            self.canvas.itemconfig(self.rect[self.snake[i][1],self.snake[i][0]],fill=self.snake_color)
