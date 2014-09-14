from Tkinter import *
import game, study, dictionaries

class Main(object):
    # This class handles the main stuff, like timerFired and etc.
    # It also displays the main screen.
    def studyButtonPressed(self):
        # go to study instructions
        global canvas # for the button. not bad style!
        self.canvas.current = study.Study(self.root, self.canvas)
        self.canvas.current.instruction()

    def gameButtonPressed(self):
        # go to game instructions
        global canvas # for the button. not bad style!
        self.canvas.current = game.Game(self.root, self.canvas)
        self.canvas.current.instruction()

    def timerFired(self):
        if self.canvas.current != self:
            self.canvas.current.timerFired()
        def f():
            self.timerFired()
        self.canvas.after(self.canvas.timerDelay, f)

    def mousePressed(self,event):
        if self.canvas.current != self:
            self.canvas.current.mousePressed(event)

    def keyPressed(self,event):
        if self.canvas.current != self:
            self.canvas.current.keyPressed(event)

    def redrawAll(self):
        self.canvas.delete(ALL)
        # draw buttons in window
        gb = self.canvas.data["gameButton"]
        self.canvas.create_window(self.canvas.width*4/5, self.canvas.height*7/9,
                                  window=gb)
        sb = self.canvas.data["studyButton"]
        self.canvas.create_window(self.canvas.width*4/5, self.canvas.height/2,
                                  window=sb)
        self.canvas.create_image(0, 0, anchor = NW,
                                 image=self.canvas.data["mainscreen"])

    def init(self, root, canvas):
        self.canvas = canvas
        self.root = root
        self.canvas.width = self.canvas.winfo_reqwidth() - 4
        self.canvas.height = self.canvas.winfo_reqheight() - 4
        self.isGameOver = False
        self.canvas.data["mainscreen"] = PhotoImage(file = "Graphics/mainscreen.gif")
        button = PhotoImage(file = "Graphics/flash_yellow.gif")
        # make buttons. they have fun cursors!
        gameButton = Button(self.canvas, image=button, width=185, height=170,
                            compound = CENTER, cursor = 'trek',
                            text="Game Time", font = "Helvetica 25 bold",
                            overrelief=RIDGE, bd=0,
                            command=self.gameButtonPressed)
        studyButton = Button(self.canvas, image=button, width=185, height=170,
                             compound = CENTER, cursor = 'star',
                            text = "Study It Up!",font = "Helvetica 25 bold",
                            overrelief=RIDGE, bd=0,
                            command=self.studyButtonPressed)
        gameButton.image = button # save image from garbage collector (needed!)
        studyButton.image = button # save image from garbage collector (needed!)
        self.canvas.data["gameButton"] = gameButton
        self.canvas.data["studyButton"] = studyButton
        # ### # #### #### #### #### #### #### #### #### #### #### #### #### ####
        # Game and Study Stuff
        # #### #### #### #### #### #### #### #### #### #### #### #### #### ####
        # background images
        self.canvas.data["gameBackground"] = PhotoImage(file =
                                            "Graphics/gameBackground.gif")
        self.canvas.data["studyBackground"] = PhotoImage(file =
                                        "Graphics/study_screen.gif")
        self.canvas.data["playBackground"] = PhotoImage(file =
                                        "Graphics/play_screen.gif")
        # buttons
        self.canvas.data["Mbutton"] = PhotoImage(file =
                        "Graphics/menubutton.gif").subsample(3,3)
        self.canvas.data["pausebutton"] = PhotoImage(file =
                        "Graphics/pause.gif").subsample(4,4)
        self.canvas.data["playbutton"] = PhotoImage(file =
                        "Graphics/play.gif").subsample(4,4)
        # 4 character colors
        self.canvas.data["charY"] = PhotoImage(file = "Graphics/char_yellow.gif")
        self.canvas.data["charG"] = PhotoImage(file = "Graphics/char_green.gif")
        self.canvas.data["charB"] = PhotoImage(file = "Graphics/char_blue.gif")
        self.canvas.data["charD"] = PhotoImage(file = "Graphics/char_dead.gif")
        # 3 lasers
        self.canvas.data["lasY"] = PhotoImage(file = "Graphics/laser_yellow.gif")
        self.canvas.data["lasG"] = PhotoImage(file = "Graphics/laser_green.gif")
        self.canvas.data["lasB"] = PhotoImage(file = "Graphics/laser_blue.gif")
        # flashcards of 3 different colors and different sizes for game
        self.canvas.data["flashY0"] = PhotoImage(file =
                        "Graphics/flash_yellow.gif").zoom(3,3).subsample(7,7)
        self.canvas.data["flashG0"] = PhotoImage(file =
                        "Graphics/flash_green.gif").zoom(3,3).subsample(7,7)
        self.canvas.data["flashB0"] = PhotoImage(file =
                        "Graphics/flash_blue.gif").zoom(3,3).subsample(7,7)
        self.canvas.data["flashY"] = PhotoImage(file =
                        "Graphics/flash_yellow2.gif").zoom(3,3).subsample(7,7)
        self.canvas.data["flashG"] = PhotoImage(file =
                        "Graphics/flash_green2.gif").zoom(3,3).subsample(7,7)
        self.canvas.data["flashB"] = PhotoImage(file =
                        "Graphics/flash_blue2.gif").zoom(3,3).subsample(7,7)
        # flashcards for study
        self.canvas.data["flashfront"] = PhotoImage(file =
            "Graphics/flashcard.gif").zoom(3,3).subsample(5,5)
        self.canvas.data["flashback"] = PhotoImage(file =
            "Graphics/flashcard_back.gif").zoom(3,3).subsample(5,5)
        self.canvas.data["flashYay"] = PhotoImage(file =
            "Graphics/flash_yellow.gif").zoom(3,3).subsample(11,11)
        self.canvas.data["flashNay"] = PhotoImage(file =
            "Graphics/flash_green.gif").zoom(3,3).subsample(11,11)
        self.canvas.data["flashMeh"] = PhotoImage(file =
            "Graphics/flash_blue.gif").zoom(3,3).subsample(11,11)
        # other graphics
        self.canvas.data["life"] = PhotoImage(file =
                            "Graphics/heart.gif").zoom(3,3).subsample(30,30)
        self.canvas.data["check"] = PhotoImage(file =
                            "Graphics/check.gif").subsample(5,5)
        self.canvas.data["x"] = PhotoImage(file =
                            "Graphics/x.gif").subsample(5,5)
        # moved canvas packing to here (before button packing!)
        self.canvas.pack()
        self.redrawAll()

    def run(self):
        # create the root and the canvas
        root = Tk()
        self.root=root
        global canvas # make canvas global for button functions
        self.root.resizable(width=FALSE, height=FALSE)
        self.canvas = Canvas(root, width=1000, height=700)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.current = self.canvas.main = self
        # Store canvas in root and in canvas itself for callbacks
        self.root.canvas = self.canvas.canvas = self.canvas
        # Set up canvas data and call init
        self.canvas.data = { }
        self.init(self.root, self.canvas)
        # set up events
        root.bind("<Button-1>", lambda event: self.mousePressed(event))
        root.bind("<Key>", lambda event: self.keyPressed(event))
        self.canvas.timerDelay = 250 # milliseconds
        self.timerFired()
        self.root.minsize(204,104) # 4 extra pixels for frame boundaries
        # and launch the app! Weeee
        self.root.mainloop()

if __name__ == "__main__":
    app = Main()
    app.run()