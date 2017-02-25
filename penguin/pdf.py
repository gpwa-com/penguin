import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from .utils import src_as_files


def append(writer, reader, rmblanks):
    for i in range(reader.getNumPages()):
        page = reader.getPage(i)

        # If the page has content, or we do not want to remove blank pages, add
        # the page to the document.
        if page.getContents() or not rmblanks:
            writer.addPage(page)


def combine(src, bookmark, rmblanks):
    writer = PdfFileWriter()

    for pdf in src_as_files(src):
        # Counter to track position current page number in the writer object.
        # this is used for bookmarking.
        iwriter = writer.getNumPages()

        reader = PdfFileReader(pdf)
        append(writer, reader, rmblanks)

        if bookmark:
            label, _ = os.path.splitext(os.path.basename(pdf))
            writer.addBookmark(label, iwriter)

    return writer
