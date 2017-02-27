import os
from collections import deque

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


def subdirs(root):
    """Return a list of subdirectories for the given root folder."""
    return [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]


def pdffiles(root):
    """Return a list of subdirectories for the given root folder."""
    return [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))
            and f.lower().endswith('.pdf')]


def bookmark_tree(root, writer=PdfFileWriter(), bm_queue=None, bm_stack=None):
    """Combine Pdf files within a root directory.

    The Pdf files are combined by traversing the root directory in a top-down
    manner. Bookmarks are nested according to the directory structure (e.g. if
    the directory is structured as root/subdir/pdf.pdf, the output Pdf would have
    the following bookmark hierarchy:
    root
        subdir
            pdf
    ).

    :param root: The root directory containing the Pdf files to combine.
    :param writer: The PdfFileWriter object contining the combined Pdf.
    :param bm_queue: A queue containing bookmark names
    :param bm_stack: A stack containing our bookmark objects.

    """
    if bm_queue is None:
        bm_queue = deque()
        bm_queue.append(os.path.basename(root))

    if bm_stack is None:
        bm_stack = []

    # Add each Pdf file to the writer object. The only way to do this
    # is to create a reader object and to copy each page.
    for pdf in pdffiles(root):
        current_page = writer.getNumPages()
        # Create the PdfFileReader object.
        reader = PdfFileReader(os.path.join(root, pdf))
        # Add each page. Presently, removing blank pages is not supported using
        # the bookmark_tree.
        append(writer, reader, rmblanks=False)
        # Clear the bookmark queue and add the bookmarks to the bookmark stack.
        # This is essential for directories that do not contain any Pdf files,
        # however they may contain subdirectories which do have Pdf files.
        while bm_queue:
            label = bm_queue.popleft()
            try:
                parent = bm_stack[-1]
            except IndexError:
                parent = None
            finally:
                bm_stack.append(writer.addBookmark(label, current_page, parent))

        # Add the bookmark for the Pdf file.
        label = os.path.splitext(pdf)[0]
        writer.addBookmark(label, current_page, parent=bm_stack[-1])
        current_page += reader.getNumPages()

    for subdir in subdirs(root):
        current_page = writer.getNumPages()
        # Add the directory to the bookmark queue
        bm_queue.append(subdir)
        # Call bookmark queue on subdirectory
        bookmark_tree(os.path.join(root, subdir), writer, bm_queue=bm_queue,
                      bm_stack=bm_stack)
        # pop the directory from the stack.
        bm_stack.pop()

    return writer
