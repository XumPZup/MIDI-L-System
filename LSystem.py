class LSystem:
    '''
    This class is used to generate an L-System

     _----------_
    | Parameters |
     -__________-
    rules: dict {'symbol': 'production'}
        The rules of the L-System
    axiom: str
        The initial state of the system
    string: str
        The resulting after running the update function

     _-------_
    | Methods |
     -_______-
    update()
        updates the string applying the rules
    '''
    def __init__(self, rules: dict, axiom: str):
        '''
         -----------
        | Atributes |
         -----------
        rules: dict {'symbol': 'production'}
            The rules of the L-System
            example: { 'R': 'L P1 + P0.5 R', 'L': 'RL' }
        axiom: str
            The initial string of the system
        '''
        self.rules = rules
        self.axiom = axiom
        self.string = axiom


    def __str__(self):
        return self.string
    

    def update(self):
        '''
        Applies the rules to the string
        '''
        result = ''
        for char in self.string.split():
            if char in self.rules.keys():
                result += self.rules[char] + ' '
            else:
                result += char + ' '
        self.string = result
