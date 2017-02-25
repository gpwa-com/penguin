import os
import shutil
import sys
import unittest

from PyPDF2 import PdfFileWriter

# Configure system path.
TEST_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_ROOT)
sys.path.insert(0, PROJECT_ROOT)

import penguin.utils as utils

class TestUtils(unittest.TestCase):
    def setUp(self):
        """Create a sample directory with some Pdf files and text files."""
        # _sample/
        #    pdf1.pdf
        #    text.txt
        #    subdir/
        #        pdf2.pdf

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

    def test_src_as_files_single_file(self):
        """Test src_as_files with a single Pdf argument."""
        src = [os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')]
        output = list(utils.src_as_files(src))
        expencted_output = [os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')]
        self.assertEqual(output, expencted_output)

    def test_src_as_files_list_of_files(self):
        """Test src_as_files with a list of Pdf argument."""
        pdf1 = os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')
        pdf2 = os.path.join(TEST_ROOT, '_sample', 'subdir', 'pdf2.pdf')
        src = [pdf1, pdf2]
        output = list(utils.src_as_files(src))
        expencted_output = [pdf1, pdf2]
        self.assertEqual(output, expencted_output)

    def test_src_as_files_single_dir(self):
        """Test src_as_files single directory passed."""
        src_dir = os.path.join(TEST_ROOT, '_sample')
        src = [src_dir]
        output = list(utils.src_as_files(src))
        expencted_output = [os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')]
        self.assertEqual(output, expencted_output)

    def test_src_as_files_list_of_dirs(self):
        """Test src_as_files with a list of directory arguments."""
        pdf1 = os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')
        src_dir1 = os.path.join(TEST_ROOT, '_sample', 'subdir')
        src = [pdf1, src_dir1]
        pdf1 = os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')
        pdf2 = os.path.join(TEST_ROOT, '_sample', 'subdir', 'pdf2.pdf')
        output = list(utils.src_as_files(src))
        expencted_output = [pdf1, pdf2]
        self.assertEqual(output, expencted_output)

    def test_src_as_files_files_and_dirs(self):
        """Test src_as_files with a both files and directory arguments."""
        src_dir1 = os.path.join(TEST_ROOT, '_sample')
        src_dir2 = os.path.join(TEST_ROOT, '_sample', 'subdir')
        src = [src_dir1, src_dir2]
        pdf1 = os.path.join(TEST_ROOT, '_sample', 'pdf1.pdf')
        pdf2 = os.path.join(TEST_ROOT, '_sample', 'subdir', 'pdf2.pdf')
        output = list(utils.src_as_files(src))
        expencted_output = [pdf1, pdf2]
        self.assertEqual(output, expencted_output)

    def tearDown(self):
        """Delete the _sample directory created in the setUp."""
        shutil.rmtree(os.path.join(TEST_ROOT, '_sample'))
