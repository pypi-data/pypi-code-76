import unittest
from pandas import DataFrame
from abdesign.core.igobject import IgObject
import abdesign.util.annotation as anno

class TestAnnotation(unittest.TestCase):
    def test_annotation(self):
        # Test if attributes set correctly
        sequence = "SCKASGYTFTSYGISWVRQAPGQGLEMGWISVYNGYYDTNYAQNLQGRVTYTDTSTSTAYMELRNLRSDDYYAVYYCARAPGYCSSCYRGDDYWGQGTLVTVSS"
        ig_object = anno.create_annotation(sequence)
        self.assertAlmostEqual(ig_object.sequence,"SCKASGYTFTSYGISWVRQAPGQGLEMGWISVYNGYYDTNYAQNLQGRVTYTDTSTSTAYMELRNLRSDDYYAVYYCARAPGYCSSCYRGDDYWGQGTLVTVSS")
        self.assertAlmostEqual(ig_object.chain_type,"H")
        self.assertAlmostEqual(ig_object.species,"human")
    
    def test_values(self):
        # Test if value_error handling works correctly
        self.assertRaises(ValueError, anno.create_annotation,"ZSCKASGYTFTSYGISWVRQAPGQGLEMGWISVYNGYYDTNYAQNLQGRVTYTDTSTSTAYMELRNLRSDDYYAVYYCARAPGYCSSCYRGDDYWGQGTLVTVSS")
        self.assertRaises(ValueError,anno.create_annotation,"CKASGYTFTSYGISW")
        self.assertRaises(ValueError,anno.create_annotation,"")
    
    def test_types(self):
        # Test if type_error handling works correctly
        self.assertRaises(TypeError, anno.create_annotation,2)
        self.assertRaises(TypeError, anno.create_annotation,{})
        self.assertRaises(TypeError, anno.create_annotation,[])
        self.assertRaises(TypeError, anno.create_annotation, DataFrame)
        self.assertRaises(TypeError, anno.create_annotation, True)
        self.assertRaises(TypeError, anno.create_annotation, 2+5j)
