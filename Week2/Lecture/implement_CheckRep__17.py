#
# Implement checkRep on this ZIPCode class
#
# Valid zip codes are 5 digits long, where each digit
# is between 0-9


class ZIPCode:
    # US Only

    def __init__(self, zip):
        self._zip = zip
        self.checkRep()

    def zip(self):
        return self._zip

    def checkRep(self):
        assert len(self.zip()) == 5
        assert self.zip().isdigit() and all([0 <= int(digit) <= 9 for digit in self.zip()])



if __name__ == '__main__':
    zipcode = ZIPCode('12345')
    zipcode = ZIPCode('hello')