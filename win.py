import curses
import windows as WINDOWS
from curses import wrapper

RUNNING = True

COMMAND_NONE = "NONE"
COMMAND_NEWTABLE = "TABLE"
COMMAND_TABLE = "TABLE"
COMMAND_SETBUTTON = "BUTTON"
COMMAND_ADDPLAYER = "ADDPLAYER"
COMMAND_SHOWPLAYER = "SHOWPLAYER"
COMMNAD_REMOVEPLAYER = "REMOVEPLAYER"
COMMAND_CLOSETABLE = "CLOSETABLE"
COMMAND_PROMPT = "PROMPT"
COMMAND_QUIT = "QUIT"

WindowManager = []

class DebugWindow(WINDOWS.Window):
    def __init__(self):
        super().__init__("DEBUG", 0, curses.LINES-5, curses.COLS-1, 5, WINDOWS.WIN_FRAMED|WINDOWS.WIN_TITLEBAR)

        self.debug_str = ""

    def AddStr(self, msg: str):
        self.debug_str = msg

    def Update(self):
        super().BeginUpdate()
        self.handle.addstr(1,1, self.debug_str)
        super().EndUpdate()

class InputText(WINDOWS.Window):
    def __init__(self, prompt: str):
         super().__init__("PROMPT", 0, 0, curses.COLS-1, 1, WINDOWS.WIN_NOCREATE | WINDOWS.WIN_FRAMED | WINDOWS.WIN_TITLEBAR)
         self.label = prompt
         self.response = ""
         self.valid_responses = []

         curses.echo(True)

    def Destroy(self):
        curses.echo(False)
        self = None
    
    def ValidateResponse():
        pass

    def HandleKeyInput(self):
        return super().HandleKeyInput()
    
class WindowTable(WINDOWS.Window):
    def __init__(self):
        super().__init__("Table", 0, 4, 22, 11, WINDOWS.WIN_FRAMED | WINDOWS.WIN_TITLEBAR)

        self.seats = [ "mse22", "Player1", "Player2", "", "Player4", "Player5", "Player6", "Player7"]
        self.player_data = {
            "mse22": { "Hands": 45 }
        }
        self.button_position = 1
        self.num_of_seats = 8
        
    def Update(self):
        super().BeginUpdate()

        seat = 1
        while seat <= self.num_of_seats:
            if self.button_position == seat:
                line = "*"
            else:
                line = " "
            line += f"{seat} {self.seats[seat-1]} "
            self.handle.addstr(seat, 1, line)
            seat += 1
        super().EndUpdate()


    def AddPlayer(self, seat: int, name: str, data=None):
        self.seats[seat-1] = name

    def RemovePlayer(self, seat: int):
        self.seats[seat-1] = ""
        self.player_data.pop( self.seats[seat-1])

    def SetButtonPosition(self, pos = -1):
        if pos == -1:
            self.button_position += 1
        else:
            self.button_position = pos
        self.button_position % self.num_of_seats
        return self.button_position

class WindowMenuBar(WINDOWS.Window):

    MENUS = {
        "NONE" : "New Table|Quit",
        "TABLE": "Button|Add Player|Remove Player|New Table|Close Table|Quit",
        "BUTTON": "Position?",
        "ADDPLAYER": "Name?",
        "SHOWPLAYER": "Position?",
        "REMOVEPLAYER": "Position?",
        "CLOSETABLE": "Are you Sure?",
        "QUIT": "Are you Sure?"
    }

    def __init__(self):
        super().__init__("Command", 0, 0, curses.COLS-1, 1)

        self.state = COMMAND_NONE
        self.prompt = ""
        self.prompt_valid_responses = []
        self.prompt_response = ""

    def Update(self):
        super().BeginUpdate()

        menus = WindowMenuBar.MENUS[self.state].split("|")
        menuStr = ""
        for m in menus:
            if m.find('?') != -1:
                m = m[:-1]
                self.state = "PROMPT"
            menuStr += "(" + m[:1] + ")" + m[1:] + ", "
        menuStr = menuStr[:-2] + "?"
        self.handle.addstr(0, 0, menuStr)
        
        super().EndUpdate()

    def HandleKeyInput(self):
        global RUNNING

        #ch =  super().HandleKeyInput()    
        c = self.handle.getch()
        if c == 27:
            if not self.state == "NONE":
                self.state == "TABLE"
        else:
            ch = chr(c)

            if ch in ['Q', 'q']:
                RUNNING = False
                self.state = "QUIT"
            else:
                if ch in ['N', 'n']:
                    self.state = "TABLE"
                if ch in ['B', 'b']:
                    self.state = "BUTTON"
                if ch in ['A' , 'a']:
                    self.state = "ADDPLAYER"
                if ch in ['R','r','X','x']:
                    self.state = "REMOVEPLAYER"
                if ch in ['C','c']:
                    self.state = "NONE"
                if ch in '123456789':
                    pass


def main(stdscr):
    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()

    cmd = WindowMenuBar()
    cmd.Update()
    cmd.SetFocus()

    DEBUG_WINDOW = DebugWindow()
    DEBUG_WINDOW.Update()

    win2 = WindowTable()
    win2.Update()
    
    while RUNNING:
        cmd.HandleKeyInput()
        cmd.Update()
        win2.Update()
        DEBUG_WINDOW.Update()

        # ch = stdscr.getch()
        

wrapper(main)