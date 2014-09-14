from Tkinter import *
import random, copy
import main, dictionaries

class Study(object):
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.canvas.width = 1000
        self.canvas.height = 700
        # initial Counts
        self.countY = 0
        self.countG = 0
        self.countB = 0
        # Flashcard initially quesiton-side up
        self.currentFlash = True
        # go Button
        goButton = Button(self.canvas, compound = CENTER, bg="#deff00", bd = 3,                    text = "     C'mon Let's Play!         ", cursor = 'star',
                    font = "Helvetica 15",
                    overrelief=RIDGE, command=self.goButtonPressed)
        self.goButton = goButton

    def timerFired(self):
        # no timer needed to study
        pass

    def mousePressed(self,event):
        if self.isGameOver == False:
            if ((event.x >=260 and event.x<=740) and
                (event.y>=26 and event.y<445)):
                self.flipCard()
                self.redrawAll()
            if ((event.x >=50 and event.x<=202) and
                (event.y>=322 and event.y<=381)):
                self.buttonMPressed()
            if ((event.x >=58 and event.x<=277) and
                (event.y>=490 and event.y<=680)):
                self.buttonYPressed()
            if ((event.x >=392 and event.x<=610) and
                (event.y>=490 and event.y<=680)):
                self.buttonGPressed()
            if ((event.x >=726 and event.x<=942) and
                (event.y>=490 and event.y<680)):
                self.buttonBPressed()

    def keyPressed(self,event):
        if self.isGameOver == False:
            if (event.keysym == "space"):
                self.flipCard()
            elif (event.keysym == "Left"):
                self.buttonYPressed()
            elif (event.keysym == "Down"):
                self.buttonGPressed()
            elif (event.keysym == "Right"):
                self.buttonBPressed()
            self.redrawAll()

    def flipCard(self):
        if self.currentFlash == True:
            self.currentFlash = False
        else: self.currentFlash = True
        self.drawFlashcard()

    def getNewCard(self):
        #for question, answer in self.M.iterkeys:
        if self.M == {}:
            self.Q = ''
            self.A = ''
            self.currentFlash = None
        for question, answer in self.M.iteritems():
            self.Q = question
            self.A = answer
            break

    def drawFlashcard(self):
        if self.currentFlash == True:
            # draw front of flashcard
            self.canvas.create_image(self.canvas.width/2, self.canvas.height/2 - 115,
                                 image=self.canvas.data["flashfront"])
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 - 115,
                    width = 260, text=str(self.Q), font = "Helvetia 25 bold")
        elif self.currentFlash == False:
            # draw back
            self.canvas.create_image(self.canvas.width/2, self.canvas.height/2 - 115,
                                 image=self.canvas.data["flashback"])
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 - 115,
                    width = 260, text=str(self.A), font = "Helvetia 25 bold")
        else:
            # draw blank flashcard
            self.canvas.create_image(self.canvas.width/2, self.canvas.height/2 - 115,
                                 image=self.canvas.data["flashfront"])

    def buttonMPressed(self):
        #return to main menu
        self.canvas.current = self.canvas.main
        self.canvas.current.init(self.root, self.canvas)

    #these 3 functions are almost the exact same thing
    def buttonYPressed(self):
        if self.Q != '':
            self.countY += 1
            self.Y[self.Q] = self.A
        self.M.pop(self.Q, self.A)
        if self.count == 0 and self.currentFlash == None:
            self.count = self.countY
            self.countY = 0
            self.M.clear()
            self.M = copy.deepcopy(self.Y)
            self.Y.clear()
        self.currentFlash = True
        self.getNewCard()
        self.redrawAll()
    def buttonGPressed(self):
        if self.Q != '':
            self.countG += 1
            self.G[self.Q] = self.A
        self.M.pop(self.Q, self.A)
        if self.count == 0 and self.currentFlash == None:
            self.count = self.countG
            self.countG = 0
            self.M.clear()
            self.M = copy.deepcopy(self.G)
            self.G.clear()
        self.currentFlash = True
        self.getNewCard()
        self.redrawAll()
    def buttonBPressed(self):
        if self.Q != '':
            self.countB += 1
            self.B[self.Q] = self.A
        self.M.pop(self.Q, self.A)
        if self.count == 0 and self.currentFlash == None:
            self.count = self.countB
            self.countB = 0
            self.M.clear()
            self.M = copy.deepcopy(self.B)
            self.B.clear()
        self.currentFlash = True
        self.getNewCard()
        self.redrawAll()

    def redrawAll(self):
        self.canvas.delete(ALL)
        self.canvas.create_image(-1620, 0, anchor = NW,
                                 image=self.canvas.data["gameBackground"])
        #draw Buttons
        self.canvas.create_image(self.canvas.width/6, self.canvas.height*5/6,
                                  image=self.canvas.data["flashYay"])
        self.canvas.create_image(self.canvas.width/2, self.canvas.height*5/6,
                                 image=self.canvas.data["flashNay"])
        self.canvas.create_image(self.canvas.width*5/6, self.canvas.height*5/6,
                                 image=self.canvas.data["flashMeh"])
        self.canvas.create_image(self.canvas.width*1/8, self.canvas.height*5/10,
                                image=self.canvas.data["Mbutton"])
        #draw button text
        self.canvas.create_text(self.canvas.width/6, self.canvas.height*5/6,
                                text="Yay \n " + str(self.countY), font = "Helvetica 25 bold")
        self.canvas.create_text(self.canvas.width/2, self.canvas.height*5/6,
                                text="Nay \n " + str(self.countG), font = "Helvetica 25 bold")
        self.canvas.create_text(self.canvas.width*5/6, self.canvas.height*5/6,
                                text="Meh \n " + str(self.countB), font = "Helvetica 25 bold")
        self.canvas.create_text(self.canvas.width*1/8, self.canvas.height*5/10,
                                text="Main Menu", font = "Helvetica 20 bold")
        # draw flashcards
        self.drawFlashcard()
        # card Count
        self.count = len(self.M)
        self.canvas.create_text(self.canvas.width*7/8, self.canvas.height/17,
            text="Cards Left: " + str(self.count),
            fill="black", font="Helvetica 25 bold")
        # keybard instructions
        self.canvas.create_text(self.canvas.width*1/8, self.canvas.height/3,
            text="Space Bar = Flip Card \n Left Arrow = Yay \n" +
            "Down Arrow = Nay \n Right Arrow = Meh",
            fill="black", font="Helvetica 20")
        # yay, all cards are in Yay pile
        if self.countY == len(self.currentDict):
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 - 130,
                                 text="YAY!", font = "Helvetia 45 bold")
            self.canvas.create_text(self.canvas.width/2, self.canvas.height/2 - 80,
                                 text="You Smarty Pants", font = "Helvetia 45 bold")

    def init(self):
        # initialize some stuff
        self.Y = dict()
        self.G = dict()
        self.B = dict()
        self.isGameOver = False
        self.redrawAll()

    #below here is for instruction screen
    def instruction(self):
        self.canvas.delete(ALL)
        self.isGameOver = True
        self.canvas.create_image(0, 0, anchor = NW,
                                 image=self.canvas.data["studyBackground"])
        # text
        self.canvas.create_text(self.canvas.width/2,200,text=
                    '''Flip the main flashcard by clicking it or pressing the
                    Spacebar''',
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,250, text=
                    '''Sort the main flashcard by putting it into one of
                    3 piles: Yay, Nay, or Meh''',
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,300, text=
                    '''To do this, press the pile you want the card to go into,
                    or use the arrow keys.''',
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,350,text=
                    '''There will be a card counter on the top right. When there
                    are no cards left, ''',
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,375,text=
                    "press one of the piles"+
                    "(or use the corresponding arrow key)",
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,400,text=
                    " to study the cards in that pile",
                    font = 'Helvetica 20')
        self.canvas.create_text(self.canvas.width/2,450, text=
                                "Choose the flashcards you want to study!",
                                font = 'Helvetica 20')
        # draw Radio Button
        self.v = StringVar()
        buttonOptions = []
        for flashcards in dictionaries.dictList:
            buttonOptions += [(flashcards,'dictionaries.'+flashcards)]
        self.i = 0
        self.radio = [0,1,2,3,4,5,6]
        for (txt, val) in buttonOptions:
            self.radio[self.i] = Radiobutton(self.canvas, text=txt,
                    relief= SUNKEN, width = 20, padx = 20,
                    variable=self.v, value=val, bg="#deff00", bd = 10)
            self.i +=1
        self.v.set('dictionaries.Sample')  # initializing the choice
        for index in xrange(self.i):
            self.canvas.create_window(self.canvas.width/2,
                                    self.canvas.height*3/4 + index*20,
                                    window=self.radio[index])
        # go Button
        window = self.goButton
        self.canvas.create_window(self.canvas.width/2, 4 +
                                  self.canvas.height*3/4 + self.i*20,
                                  window=window)

    def goButtonPressed(self):
        global canvas # for button!
        self.getCurrentDictionary()
        # destroy radio buttons >:[]
        for i in xrange(self.i):
            self.radio[i].destroy()
        self.init()

    def getCurrentDictionary(self):
        '''sets self.M to the selected dictionary'''
        self.v.get()
        self.currentDict = eval(self.v.get())
        self.M = copy.deepcopy(self.currentDict)
        self.getNewCard()
