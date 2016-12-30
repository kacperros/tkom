from Engine.Engine import Engine

parsed_file = open('program.txt')
engine = Engine('2016.05.11', '2016.05.15', parsed_file)
engine.invest()