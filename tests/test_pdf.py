import os
import shutil
import sys
import unittest

from PyPDF2 import PdfFileWriter

# Configure system path.
TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import penguin.pdf as pdf

class TestPdf(unittest.TestCase):
    def setUp(self):
        """Create a sample directory with some Pdf files and text files."""
        # _sample/
        #     pdf1.pdf
        #     text.txt
        #     subdir/
        #         pdf2.pdf
        #         subdir2/
        #             subdir3/
        #                 pdf3.pdf
        #

        os.makedirs(os.path.join(TEST_ROOT, '_sample'))
        pdf1 = PdfFileWriter()
        pdf1.addBlankPage(1, 1)
        with open(os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf'), 'wb') as o1:
            pdf1.write(o1)

        with open(os.path.join(TEST_ROOT, '_sample', 'text.txt'), 'w') as o2:
            o2.write('all good penguins write unittests')

        os.makedirs(os.path.join(TEST_ROOT, '_sample', 'subdir'))
        pdf2 = PdfFileWriter()
        pdf2.addBlankPage(1, 1)
        with open(os.path.join(TEST_ROOT, '_sample', 'subdir', 'pdf2.pdf'), 'wb') as o3:
            pdf2.write(o3)

        os.makedirs(os.path.join(TEST_ROOT, '_sample', 'subdir', 'subdir2'))
        os.makedirs(os.path.join(TEST_ROOT, '_sample', 'subdir', 'subdir2', 'subdir3'))
        pdf3 = PdfFileWriter()
        pdf3.addBlankPage(1, 1)
        with open(os.path.join(TEST_ROOT, '_sample', 'subdir', 'subdir2', 'subdir3', 'pdf3.pdf'), 'wb') as o4:
            pdf3.write(o4)

        os.makedirs(os.path.join(TEST_ROOT, '_sample', 'subdir4'))
        pdf4 = PdfFileWriter()
        pdf4.addBlankPage(1, 1)
        with open(os.path.join(TEST_ROOT, '_sample', 'subdir4', 'pdf4.pdf'), 'wb') as o5:
            pdf4.write(o5)

    def tearDown(self):
        """Delete the _sample directory created in the setUp."""
        shutil.rmtree(os.path.join(TEST_ROOT, '_sample'))
