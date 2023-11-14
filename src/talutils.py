class Player:

    def __init__(self, nick : str, lp : int):
        assert lp >= 100
        self.nick = nick
        self.lp = lp
        self.timer = -1

    def getPlayerName(self):
        return self.nick

    def setPlayerName(self, nme : str):
        self.nick = nme

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

class Settings:

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


class Tournament:
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

class Calculator:

    def __init__(self, ope = 0):
        assert 0 <= ope <= 4

        self.ope = 0

    def getOpe(self):
        return self.ope

    def getFormatedOpe(self):
        match(self.ope):
            case 0:
                return "+"
            case 1:
                return "-"
            case 2:
                return "*"
            case 3:
                return "/"
            case 4:
                return "→"


    def setOpe(self, ope : int):
        assert 0 <= ope <= 4
        self.ope = ope

    def calculate(self,value1 : int, value2 : int):
        match(self.ope):
            case 0:
                return value1 + value2
            case 1:
                res = value1 - value2
                if(res < 0):
                    return 0
                return res
            case 2:
                return value1 * value2
            case 3:
                if(value2 == 0):
                    return 0
                return value1 // value2
            case 4:
                return value2
