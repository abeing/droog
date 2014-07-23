class Actor(object):
    """The Actor class manages action points and acting in turn order."""

    def __init__(self, ap, ap_max):
        self.ap = ap
        self.ap_max = ap_max 
        self.act_func = None

    def act(self):
        self.ap -= self.act_func()
        return self.ap

    def refill(self):
        self.ap += self.ap_max
        
