import sys
import re

class Merchant:

    def __init__(self):
        self.w = Warehouse()
        self.c = Converter()
        self.newNum = re.compile("^(\w+) is (\w)$")
        self.newItem = re.compile("^([\w\s]+) (\w+) is (\d+) Credits")
        self.convert = re.compile("^how much is ([\w\s]+\w) ?")
        self.price = re.compile("^how many Credits is ([\w\s]+) (\w+) ?")

    # Check to see if line matches a known pattern, and if so take appropriate
    # action
    def process(self, line):
        knownLine = False
        for patt in (self.newNum, self.newItem, self.convert, self.price):
           m = patt.match(line)
           if m:
               if patt == self.newNum:
                   self.c.addSymbol(m.group(1), m.group(2))

               elif patt == self.newItem:
                   self.w.addItem(m.group(2), int(m.group(3))
                       / float(self.c.galacticToHA(m.group(1))))

               elif patt == self.convert:
                   print m.group(1) + " is " + str(self.c.galacticToHA(m.group(1)))

               elif patt == self.price:
                   totalCost = str(self.w.cost(m.group(2),
                       float(self.c.galacticToHA(m.group(1)))))
                   print m.group(1) + " " + m.group(2) + " is " + totalCost + \
                       " Credits"

               knownLine = True
               break

        # The line didn't match any of the patterns, so we don't know what
        # they are talking about
        if not knownLine:
           print "I have no idea what you are talking about"

class Warehouse:

    def __init__(self):
        self.items = {}

    def addItem(self, item, cost):
        self.items[item.upper()] = cost

    def cost(self, item, ammount):
        try:
           cost = self.items[item.upper()]
        except KeyError:
           raise ValueError, "no such item: %s" % item

        return cost * ammount

    def show(self):
        ret = ""
        for key in self.items:
           ret += key + "=>" + str(self.items[key]) + ","
        return ret

# Used to keep track of the current numeral alphabet, as well as convert
# between galactic, roman and hindu-arabic number systems.
class Converter:

    def __init__(self):
        self.numerals = {}

    def addSymbol(self, galactic, roman):
        self.numerals[galactic.upper()] = roman

    def galacticToRoman(self, galacticNum):
        gn = galacticNum.split(" ")
        roman = ""
        for g in gn:
            try:
                roman += self.numerals[g.upper()]
            except KeyError:
                raise ValueError, "input is not a valid galactic numeral: %s" % g
        return roman

    def romanToHA(self, toConvert):
        toConvert = toConvert.upper()
        nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}
        sum = 0
        for i in range(len(toConvert)):
            try:
                value = nums[toConvert[i]]
                # If the next place holds a larger number, this value is negative
                if i+1 < len(toConvert) and nums[toConvert[i+1]] > value:
                    sum -= value
                else: sum += value
            # An invalid character was used in the given roman numeral
            except KeyError:
                raise ValueError, "given value contains invalid character: %s" % toConvert[i]

        if self.HAToRoman(sum) == toConvert:
            return sum
        else:
            raise ValueError, "given value is not a valid Roman numeral: %s" % toConvert

    # This function is only used as a way to verify the romanToHA function.
    # Refer to design.txt for explaination why
    def HAToRoman(self, toConvert):
        ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
        nums = ("M",  "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")
        res = ""
        # Numbers >= 4000 cannot be represented, since we cannot repeat M more than 3 times
        if toConvert >= 4000:
           raise ValueError, "given value is too large: %s" % toConvert

        for i in range(len(nums)):
            count = int(toConvert / ints[i])
            res += nums[i] * count
            toConvert -= ints[i] * count
        return res

    def galacticToHA(self, galacticNum):
        return self.romanToHA(self.galacticToRoman(galacticNum))

    def show(self):
        ret = ""
        for key in self.numerals:
           ret += key + "=>" + self.numerals[key] + ","
        return ret

def main():
    m = Merchant()
    with open(sys.argv[1]) as f:
       for line in f.readlines():
          m.process(line)

if __name__ == '__main__':
    main()
