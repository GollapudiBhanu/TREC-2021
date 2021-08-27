
'''
This file is used to generate list of Random float numbers.
'''
class GenerateRandomFloat:

    def __init__(self):
        pass

    '''
        Generate 1000 float numbers
    '''
    def genereate1000FloatNumbers(self):
        out_put = [(1000-p)/1000 for p in range(0,1000)]
        return out_put

    def genereateFloatNumbers(self, number):
        out_put = [(number-p)/number for p in range(0,number)]
        return out_put