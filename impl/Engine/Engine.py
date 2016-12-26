from Model.World import World
from Model.Investor import Investor


class Engine:
    def __init__(self):
        self.world = World()
        self.investor = Investor()
