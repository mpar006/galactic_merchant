import unittest
import galactic_merchant as gm

class MerchantTests(unittest.TestCase):
    def setUp(self):
        self.m = gm.Merchant()
        self.m.process("foo is I")
        self.m.process("goo is V")
        self.m.process("hoo is X")
        self.m.process("ioo is L")
        self.m.process("hoo foo hoo cat is 95 Credits")
        #self.m.process("how many Credits is foo goo cat ?") 

    def testAddGalactic(self):
        self.assertEqual(self.m.c.show(), "IOO=>L,HOO=>X,GOO=>V,FOO=>I,")

    def testAddItem(self):
        self.assertEqual(self.m.w.show(), "CAT=>5")

    #def testCost(self):
    #    self.assertEqual(self.m.w.itemCost("cat", 4), 20)

    #def testConvert(self):
    #    self.assertEqual(self.m.c.galacticToHA("hoo ioo foo", 41))

class WarehouseTests(unittest.TestCase):
    def setUp(self):
        self.w = gm.Warehouse()
        self.w.addItem("silver", 5)
        self.w.addItem("gold", 15)
        self.w.addItem("engine", 75)

    def testCost(self):
        self.assertEqual(self.w.cost("silver", 3), 15)

    #def testNoSuchItem(self):
    #    self.assertRaises(self.w.cost("beef", 5))

class convertTests(unittest.TestCase):
    def setUp(self):
        self.c = gm.Converter()
        self.c.addSymbol("glob", "I")
        self.c.addSymbol("prok", "V")
        self.c.addSymbol("pish", "X")
        self.c.addSymbol("tegj", "L")

    def testGalacticToRoman(self):
        self.assertEqual(self.c.galacticToRoman("pish tegj glob prok"), 
            "XLIV")

    def testGalacticToHA(self):
        self.assertEqual(self.c.galacticToHA("tegj pish prok glob glob glob"),
            68)

    def test1903(self):
        self.assertEqual(self.c.romanToHA("MCMIII"), 1903)

    def test39(self):
        self.assertEqual(self.c.romanToHA("XXXIX"), 39)

    def test3successionI(self):
        self.assertRaises(self.c.romanToHA("I" * 4))
    
    def test3successionX(self):
        self.assertRaises(self.c.romanToHA("X" * 4))

    def test3successionC(self):
        self.assertRaises(self.c.romanToHA("C" * 4))
    
    def test3successionM(self):
        self.assertRaises(self.c.romanToHA("M" * 4))

    def testRepeatD(self):
        self.assertRaises(self.c.romanToHA("D" * 2))

    def testRepeatL(self):
        self.assertRaises(self.c.romanToHA("L" * 3))
    
    def testRepeatV(self):
        self.assertRaises(self.c.romanToHA("V" * 2))

    def testSubI(self):
        self.assertRaises(self.c.romanToHA("IL"))
 
def main():
    unittest.main()

if __name__ == '__main__':
    main()
