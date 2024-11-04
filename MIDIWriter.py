from midiutil.MidiFile import MIDIFile


class MIDIWriter:
    '''
    This class is used to write the a MIDI file from a string that follows a grammar

     _---------_
    | Atributes |
     -_________-
    step: int
        This is the default step
    steps: list[int]
        This are the steps used in the major scale
    modes: list[str]
        Just the list of the seven modes
    string: str
        The string that generates the notes
    scale: int
        The mode used by writeV2()
    states: list[dict]
        The stack of stored states
    state: dict {'degree': int, 'pitch': int}
        Stores the current degree and pitch
    filename: str
        The name of the output file
    
     _-------_
    | Methods |
     -_______-
    write()
        Writes the notes in a midi file using the default step
    writeV2()
        Writes the notes in a midi files using the selected scales intervals
    '''
    step = 2 # Default step
    steps = [2, 2, 1, 2, 2, 2, 1]
    modes = ['Major', 'Dorian', 'Phrygian', 'Lydian', 'Mixolydian', 'Minor', 'Locrian']
    def __init__(self, string: str, scale: int, degree: int, pitch: int, filename: str):
        '''
         -----------
        | Atributes |
         -----------
        string: str
            The string that generates the notes. This string should follow the grammar
            G = {Pd, +a, -a, Sd, [, ]}
            Pd = play a note lasting duration = d where d is a decimal number or integer
                 P0.5 is an eigth note and P1 is a quarter note
            Sd = silence lasting duration d (same as Pd)
            '+' and '-' are used to pitch up or down the next note and can be added flats
            or sharps like so: +b or -# or +# or -b
            '[' and ']' push and pop state in the stack self.states
            All characters of the grammar have to be separated by spaces.
            Example1: "P0.5 + + P1 -b P0.25 +# P1"
            Example2: "L P0.5 +# R P1 L P0.5 + [ - P1 + P0.5 ] P0.5 -b
            The character that are not contained in G will be ignored
        scale: int
            selects the scale mode to be used by writeV2().
            0 Major
            1 Dorian
            ...
            ...
            5 Minor
            6 Locrian
        degree: int
            The degree of the scale at which the writer will be initialized
        pitch: int
            The note at which the writer will be initialized
        filename: str
            The name of the output file
        '''
        self.string = string
        self.scale = scale
        self.states = [] # Stack of saved states
        self.state = {'degree': degree, 'pitch': pitch, 'alteration': 0}
        self.filename = filename


    def write(self):
        '''
        Writes the MIDI file from the string using the default step
        '''
        mf = MIDIFile(1)
        track = 0 # The only track
        time = 0 # Start at the beginning
        channel = 0
        for char in self.string.split():
            if char == '[': # Save current state
                self.states.append(self.state)
            elif char == ']': # Return to previous state
                self.state = self.states.pop()
            
            elif 'P' in char or 'S' in char: # Play note character
                duration = float(char[1:])
                if 'P' in  char:
                    mf.addNote(track, channel, self.state['pitch'] + self.state['alteration'], time, duration, 100)
                    self.state['alteration'] = 0
                time += duration
                        
            else: # Pitch
                if char[1:]: # Flat or sharp
                    self.state['alteration'] = 1 if char[1] == '#' else -1
                self.state['pitch'] = self.state['pitch'] + self.step if char[0] == '+' else self.state['pitch'] - self.step

        with open(self.filename, 'wb') as f:
            mf.writeFile(f)


    def writeV2(self):
        '''
        Writes the notes following a scale degrees
        '''
        mf = MIDIFile(1)
        track = 0 # The only track
        time = 0 # Start at the beginning
        channel = 0
        self.state['alteration'] = 0
        for char in self.string.split():

            if char == '[': # Save current state
                self.states.append(self.state)
            elif char == ']': # Return to previous state
                self.state = self.states.pop()
            
            elif 'P' in char or 'S' in char: # Play note character
                duration = float(char[1:])
                if 'P' in  char:
                    mf.addNote(track, channel, self.state['pitch'] + self.state['alteration'], time, duration, 100)
                    self.state['alteration'] = 0
                time += duration
            else: # Pitch
                if char[1:]: # Flat or sharp
                    self.state['alteration'] = 1 if char[1] == '#' else -1
                if char[0] == '+':
                    step = self.steps[(self.scale + self.state['degree']) % 7]
                    self.state['degree'] = (self.state['degree'] + 1) % 7
                    self.state['pitch'] += step
                else:
                    self.state['degree'] = (self.state['degree'] - 1) % 7
                    step = self.steps[(self.scale + self.state['degree']) % 7]
                    self.state['pitch'] -= step

        with open(self.filename, 'wb') as f:
            mf.writeFile(f)
