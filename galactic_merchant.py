import sys
import re

class Merchant:

    def __init__(self):
        self.w = Warehouse()
        self.c = Converter()
        self.newNum = re.compile("^(\w+) is (\w)$")
        self.newItem = re.compile("^([\w\s]+) (\w+) is (\d+) Credits")
        self.convert = re.compile("^how much is (\w[\w\s]+) ?")
        self.price = re.compile("^how many Credits is ([\w\s]+) (\w+) ?")

    def process(self, line):
        nn = self.newNum.match(line)
        ni = self.newItem.match(line)
        co = self.convert.match(line)
        p = self.price.match(line)
        if nn:
            self.c.addSymbol(nn.group(1), nn.group(2))
        elif ni:
            self.w.addItem(ni.group(2), int(self.c.galacticToHA(ni.group(1))) / int(ni.group(3)))
        elif co:
            self.c.galacticToHA(co.group(1))
        elif p:
            self.w.cost(p.group(2), p.group(1))

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
                raise ValueError, "input is not a valid galactic numeral: %s" % galacticNum
        return roman

    def romanToHA(self, input):                                                         
        if not isinstance(input, type("")):                                       
            raise TypeError, "expected string, got %s" % type(input)              
        input = input.upper()                                                   
        nums = {'M':1000, 'D':500, 'C':100, 'L':50, 'X':10, 'V':5, 'I':1}         
        sum = 0                                                                   
        for i in range(len(input)):                                               
            try:                                                                  
                value = nums[input[i]]                                            
                # If the next place holds a larger number, this value is negative 
                if i+1 < len(input) and nums[input[i+1]] > value:                 
                    sum -= value                                                  
                else: sum += value                                                
            except KeyError:                                                      
                raise ValueError, 'input is not a valid Roman numeral: %s' % input
        return sum

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
