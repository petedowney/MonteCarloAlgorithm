import math
import numpy as np
class BitString:
    """
    Simple class to implement a string of bits
    """

    def __init__(self, string):
        """
        creats an np array of bits
        Parameters
        ----------
        string an int array of 1 and 0
        """
        self.string = np.array(string)

    def __len__(self):
        """
        Returns
        -------
        length of of array
        """
        return len(self.string)

    def __str__(self):
        """
        Returns
        -------
        string version of bitstring
        """
        return str(self.string)

    def set_string(self, string):
        """
        change the bitstrings string
        Parameters
        ----------
        string new np array
        """
        self.string = np.array(string);

    def flip(self, index):
        """
        flip a bit at specified index
        Parameters
        ----------
        index


        """
        self.string[index] = 1 - self.string[index]

    def on(self):
        """
        Returns
        -------
        how many of the bits are 1s
        """
        return np.sum(self.string == 1)

    def off(self):
        """
        how many of the bits are 0s
        Returns
        -------

        """
        return np.sum(self.string == 0)

    def int(self):
        """
        Returns
        -------
        decimal representation of bitstring
        """
        num = 0;
        for n, x in enumerate(np.flip(self.string)):
            num += 2 ** (n) * x;
        return num;

    def set_int(self, decimal, digits=20):
        """
        sets the bitstring using decimal representation input
        Parameters
        ----------
        decimal int number
        digits how long the bitstring should be

        """
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
        """

        Parameters
        ----------
        obj another bitstring

        Returns
        -------
        if the bitstring equals another
        """
        return np.array_equal(self.string, obj.string)

