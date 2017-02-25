import click
import os

from gpw.pdf import combine
from gpw.utils import is_valid_source


@click.group()
def gpw():
    pass

@gpw.command()
@click.argument('src', nargs=-1)
@click.argument('dst')
@click.option('--bookmark', 'bookmark', flag_value='include-bookmarks',
              default=True)
@click.option('--remove-blank-pages', 'rmblanks', flag_value='remove-blanks-pages',
              default=False)
def combinepdfs(src, dst, bookmark, rmblanks):
    """Combine Pdf files from the source provided into the destination file.

    :param src: The source Pdf file(s). src can either be a list of individual
        files or directories containing Pdf files.
    :param dst: The output file destination.
    :param bookmark: True if the combined Pdf should include bookmarks.
    :param rm_blanks: True if blank pages should be removed from the combined Pdf.

    """

    if not all((map(is_valid_source, src))):
        raise click.BadParameter("src arguments must be either a valid directory"
                                 " or pdf file.")

    combined_pdf = combine(src, bookmark, rmblanks)

    with open(dst, 'wb') as f:
        combined_pdf.write(f)

if __name__ == '__main__':
    gpw()
