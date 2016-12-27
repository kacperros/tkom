from Model.World import World
from Model.Investor import Investor
from Engine.EventWorldAdapter import EventWorldAdapter


class RealityController:
    def __init__(self):
        self.world = World()
        self.investor = Investor()
        self.event_world_adapter = EventWorldAdapter(self.world)
