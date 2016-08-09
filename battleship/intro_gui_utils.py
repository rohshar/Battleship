from graphics import *
import tkinter as tk


class InputApp(tk.Tk):
    """
    Creates a window that allows the user to input all of his choices to create the game.
    """
    def __init__(self):
        """
        Creates the window where the user will input his or her choices
        :return:
        """
        tk.Tk.__init__(self)
        self.wm_title("Input Stage")
        self.label1 = tk.Label(self, text='How large do you want the BattleShip window to be? (from 150-550 px)')
        self.label1.pack()
        self.entry1 = tk.Entry(self)
        self.entry1.pack()

        self.label2 = tk.Label(self, text='Do you wanna play: player vs. player (1), player vs. CPU (2), CPU vs. CPU (3)')
        self.label2.pack()
        self.entry2 = tk.Entry(self)
        self.entry2.pack()

        self.label3 = tk.Label(self, text='What CPU level do you want? (1: very easy, 2: easy, 3: medium, 4: hard, 5: very hard)')
        self.label3.pack()
        self.entry3 = tk.Entry(self)
        self.entry3.pack()

        self.button = tk.Button(self, text="Start playing", command=self.on_button)
        self.button.pack()

    def on_button(self):
        """
        Gets the user's input and makes sure it is valid
        :return:
        """
        size = int(self.entry1.get())
        option = int(self.entry2.get())
        diff = None
        if self.entry2.get():
            diff = int(self.entry3.get())
        if (150 <= size <= 550):
            if (option == 1) or (option == 2) or (option == 3):
                if (option == 2) or (option == 3):
                    if (1 <= diff <= 5):
                        self.destroy()
                        self.size = size
                        self.option = option
                        self.diff = diff
                        self.quit()
                elif (option == 1):
                    self.destroy()
                    self.size = size
                    self.option = option
                    self.diff = diff
                    self.quit()

        print("You must input appropriate choices!")
        self.destroy()
        app = InputApp()
        app.mainloop()


def instruct():
    """
    Creates a window that displays all of the instructions.
    """
    helper=GraphWin("Instructions", 500, 500)
    helper.setBackground('Pink')
    helper.setCoords(0, 0, 10, 10)
    instructions=Text(Point(5, 5), "Welcome to Battleship!\n \nIn this game, "
                      "you will pick points on\n a 10x10 grid to choose where"
                      " your five\n ships will be placed. You will have one \n"
                      "ship of length five, one ship of \nlength four, two ships "
                      "of length three, and\n one ship of length two. Then, you\n"
                      "will proceed to choose points on the\n computer's grid and"
                      " check whether the shot\n was a hit or a miss. A red dot is a\n"
                      "hit and a white dot is a miss. The computer\n"
                      "will then do the same. When all \n"
                      "spaces for a given ship are hit,\n that ship sinks. When"
                      " a player sinks all\n of his or her opponent's ships, the \n"
                      "player wins. \n\n Click the window to go back!")
    instructions.setSize(20)
    instructions.draw(helper)
    helper.getMouse()
    helper.close()

def start():
    """
    Creates a window GUI display that allows the user to choose whether to proceed or get instructions.
    """
    p = Point(0, 0)
    img = Image(p, "battle1.gif")
    width = img.getWidth()
    height = img.getHeight()
    img.move(width / 2, height / 2)

    intro = GraphWin("Intro Page", width, height)
    img.draw(intro)
    btext = Text(Point(250, 75), "Battleship")
    btext.setSize(20)
    btext.setStyle('bold italic')
    btext.draw(intro)
    srec = Rectangle(Point(200,150), Point(300, 200))
    srec.setFill("coral")
    srec.draw(intro)
    stext = Text(Point(250, 175), "Start")
    stext.setFill("black")
    stext.draw(intro)
    irec = Rectangle(Point(200, 250), Point(300, 300))
    irec.setFill("coral")
    irec.draw(intro)
    itext = Text(Point(250, 275), "Instructions")
    itext.setFill("black")
    itext.draw(intro)

    while True:
        p = intro.getMouse()
        x = p.getX()
        y = p.getY()
        if 200 < x < 300 and 150 < y < 200:
            intro.close()
            return True
        if 200 < x < 300 and 250 < y < 300:
            intro.close()
            return False
