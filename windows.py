import curses

WIN_FRAMED = 1
WIN_TITLEBAR = 2
WIN_NOCREATE = 256

class Window:
    def __init__(self, title: str, x: int, y:int, w:int, h:int, options=0) -> None:
        self.title = title
        self.left = x
        self.top = y
        self.width = w
        self.height = h
        self.options = options
        self.client_offset_x = 0
        self.client_offset_y = 0
        self.doUpdate = False

        self.hasFocus = False

        if not (self.options & WIN_NOCREATE):
            self.handle = self.Create()
            self.doUpdate = True
        
    def __str__(self):
        return f"Window {self.title} @ ({self.left}, {self.top})"
    

    def Handle(self):
        return self.handle()

    def Create(self):
        self.handle = curses.newwin(self.height, self.width, self.top, self.left)
        self.handle.clear()
        self.SetTitle(self.title)
        return self.handle

    def Destroy(self):
        pass

    def DrawFrame(self):
        if self.options & WIN_FRAMED:
            self.handle.box()
            if self.options & WIN_TITLEBAR:    
                self.handle.addstr(0, 2, self.titlebar, curses.A_REVERSE)

    def Invalidate(self):
        self.doUpdate = True
        
    def BeginUpdate(self):
        self.handle.clear()
        self.DrawFrame()

    def EndUpdate(self):
        self.handle.refresh()
        self.doUpdate = False

    def Render(self):
        pass

    def Update(self):
        self.BeginUpdate()
        self.Render()
        self.EndUpdate()

    def SetTitle(self, newTitle: str):
        self.title = newTitle
        self.titlebar = f"[ {self.title} ]"
        self.doUpdate = True

    def SetFocus(self, takeFocus = True):
        self.hasFocus = takeFocus

    def HandleKeyInput(self):
        ch = -1
        if True:
            ch = self.handle.getch()
        return chr(ch)
        
