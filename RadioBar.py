from tkinter import RADIOBUTTON, Frame, LEFT, W, IntVar, YES, Radiobutton, Label

class RadioBar(Frame):
    
    def __init__(self, parent = None, picks = [], group = "Title:", 
                side = LEFT, anchor = W):
        Frame.__init__(self, parent)
        Label(self, text = group).pack()
    
        self.v = IntVar()
        self.v.set(1)

        for text, mode in picks:
            rad = Radiobutton(self, text = text, variable = self.v, value = mode)
            rad.pack(side = side, anchor = anchor, expand = YES)
