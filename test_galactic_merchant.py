import unittest
import galactic_merchant as gm
import sys
from StringIO import StringIO


class MerchantTests(unittest.TestCase):
    def setUp(self):
        self.saved_stdout = sys.stdout
        self.out = StringIO()
        sys.stdout = self.out

        self.m = gm.Merchant()
        self.m.process("foo is I")
        self.m.process("goo is V")
        self.m.process("hoo is X")
        self.m.process("ioo is L")
        self.m.process("hoo foo hoo cat is 95 Credits")

    def tearDown(self):
        sys.stdout = self.saved_stdout

    def testAddGalactic(self):
        self.assertEqual(self.m.c.show(), "IOO=>L,HOO=>X,GOO=>V,FOO=>I,")

    def testAddItem(self):
        self.assertEqual(self.m.w.show(), "CAT=>5,")

    def testCostEnquiry(self):
        self.m.process("how many Credits is foo goo cat ?")
        self.assertEqual(self.out.getvalue(), "foo goo cat is 20 Credits\n")

    def testConvertEnquiry(self):
        self.m.process("how much is hoo ioo foo ?")
        self.assertEqual(self.out.getvalue(), "hoo ioo foo is 41\n")


class WarehouseTests(unittest.TestCase):
    def setUp(self):
        self.w = gm.Warehouse()
        self.w.addItem("silver", 5)

    def testCost(self):
        self.assertEqual(self.w.cost("silver", 3), 15)

    def testNoSuchItem(self):
        self.assertRaises(ValueError, self.w.cost, "beef", 5)


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

    def testInvalidGalacticToRoman(self):
        self.assertRaises(ValueError, self.c.galacticToHA, "hoo goo goo")

    def testGalacticToHA(self):
        self.assertEqual(self.c.galacticToHA("tegj pish prok glob glob glob"),
                         68)

    def test1903(self):
        self.assertEqual(self.c.romanToHA("MCMIII"), 1903)

    def test39(self):
        self.assertEqual(self.c.romanToHA("XXXIX"), 39)

    def test3successionI(self):
        self.assertRaises(ValueError, self.c.romanToHA, "I" * 4)

    def test3successionX(self):
        self.assertRaises(ValueError, self.c.romanToHA, "X" * 4)

    def test3successionC(self):
        self.assertRaises(ValueError, self.c.romanToHA, "C" * 4)

    def test3successionM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "M" * 4)

    def testRepeatD(self):
        self.assertRaises(ValueError, self.c.romanToHA, "D" * 2)

    def testRepeatL(self):
        self.assertRaises(ValueError, self.c.romanToHA, "L" * 3)

    def testRepeatV(self):
        self.assertRaises(ValueError, self.c.romanToHA, "V" * 2)

    def testSubIL(self):
        self.assertRaises(ValueError, self.c.romanToHA, "IL")

    def testSubIC(self):
        self.assertRaises(ValueError, self.c.romanToHA, "IC")
 
    def testSubID(self):
        self.assertRaises(ValueError, self.c.romanToHA, "ID")

    def testSubIM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "IM")

    def testSubXD(self):
        self.assertRaises(ValueError, self.c.romanToHA, "XD")

    def testSubXM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "XM")

    def testSubVM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "VM")

    def testSubVD(self):
        self.assertRaises(ValueError, self.c.romanToHA, "VD")
 
    def testSubVC(self):
        self.assertRaises(ValueError, self.c.romanToHA, "VC")

    def testSubVD(self):
        self.assertRaises(ValueError, self.c.romanToHA, "VD")

    def testSubVM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "VM")

    def testSubLC(self):
        self.assertRaises(ValueError, self.c.romanToHA, "LC")

    def testSubLD(self):
        self.assertRaises(ValueError, self.c.romanToHA, "LD")

    def testSubLM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "LM")

    def testSubDM(self):
        self.assertRaises(ValueError, self.c.romanToHA, "DM")

    def testSubIIX(self):
        self.assertRaises(ValueError, self.c.romanToHA, "IIX")


def main():
    unittest.main()

if __name__ == '__main__':
    main()
