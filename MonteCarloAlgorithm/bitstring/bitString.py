import math
import numpy as np
class BitString:
    """
    Simple class to implement a string of bits
    """

    def __init__(self, string):
        self.string = np.array(string)

    def __len__(self):
        return len(self.string)

    def __str__(self):
        return str(self.string)

    def set_string(self, string):
        self.string = np.array(string);

    def flip(self, index):
        self.string[index] = 1 - self.string[index]

    def on(self):
        return np.sum(self.string == 1)

    def off(self):
        return np.sum(self.string == 0)

    def int(self):
        num = 0;
        for n, x in enumerate(np.flip(self.string)):
            num += 2 ** (n) * x;
        return num;

    def set_int(self, decimal, digits=20):
        newString = np.zeros(digits).astype(int);
        index = digits - 1
        while (decimal > 0):
            assert index >= 0, "not enough binary digits to convert decimal"
            if (2 ** index <= decimal):
                newString[index] = 1;
                decimal -= 2 ** index;
            index -= 1;
        self.string = np.flip(newString);

    def __eq__(self, obj):
        return np.array_equal(self.string, obj.string)

