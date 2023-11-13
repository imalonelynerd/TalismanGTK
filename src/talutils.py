class Player(object):

    def __init__(self, nick : str, lp : int):
        assert lp >= 100

        if nick == "" :
            self.nick = "Player"
        else:
            self.nick = nick
        self.lp = lp
        self.timer = -1

    def getPlayerName(self):
        return self.nick

    def getLP(self):
        return self.lp

    def getFormatedLP(self):
        return f"<span size='40000'>{self.lp}</span>"

    def getTimer(self):
        return self.timer

    def setLP(self, val : int):
        assert 0 <= self.lp
        self.lp = val

    def scaleLP(self, val: int):
        assert self.lp + val >= 0
        self.lp += val

    def setTimer(self, val : int):
        assert self.timer + val >= 0
        self.timer = val

    def tickDown(self):
        assert self.timer > 0
        self.timer -= 1

class Settings(object):

    def __init__(self, timertype : int, params : list):
        assert 0 <= timertype <= 2
        assert len(params) == 3

        self.timertype = timertype
        self.params = params

    def getTimerType(self):
        return self.timertype

    def getTimerName(self):
        match(self.timertype):
            case 0:
                return "Chronometer"
            case 1:
                return "Countdown"
            case 2:
                return "Nexus-like"
            case _:
                return "INVSTATE"

    def getCountdown(self):
        assert self.timertype == 1
        return self.params[0]

    def getPlayerTime(self):
        assert self.timertype == 2
        return self.params[1]

    def getAddedTime(self):
        assert self.timertype == 2
        return self.params[2]


class Tournament(object):
    def __init__(self,p1 : Player, p2 : Player, settings : Settings):
        assert p1 != None
        assert p2 != None
        assert settings != None

        self.p1 = p1
        self.p2 = p2
        self.settings = settings
        self.timer = 0
        if(self.settings.getTimerType() == 1):
            self.timer = self.settings.getCountdown()
        if(self.settings.getTimerType() == 2):
            self.p1.setTimer(self.settings.getPlayerTime())
            self.p2.setTimer(self.settings.getPlayerTime())
