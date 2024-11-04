from LSystem import LSystem
from MIDIWriter import MIDIWriter
from os import system


rules = {"L": "R P0.33 + + P0.33 - - P0.33 [ P0.5 -# P1 ]",
         "R": "P1 - S1 L P1 + P0.5 R"}

axiom = "R"

generations = 2


l_sys = LSystem(rules, axiom)
for i in range(generations):
    l_sys.update()
    print(f"gen {i}: {l_sys}")

writer = MIDIWriter(string=l_sys.string,
                    scale=0,
                    degree=0,
                    pitch=72,
                    filename='midi/test.midi'
                    )

writer.writeV2()

system('mscore -j job.json')
