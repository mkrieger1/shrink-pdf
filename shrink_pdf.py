import subprocess
import sys
from os.path import basename, splitext

def main():
    if len(sys.argv) == 3:
        infile = sys.argv[1]
        outfile = sys.argv[2]
    elif len(sys.argv) == 2:
        infile = sys.argv[1]
        fullname = basename(infile)
        name, ext = splitext(fullname)
        if ext != '.pdf':
            name = fullname
        outfile = f'{name}.out.pdf'
    else:
        raise SystemExit(
            f"Usage: {basename(sys.argv[0])} input.pdf [output.pdf]")

    subprocess.check_call([
        'gs', '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/ebook',
        '-dNOPAUSE', '-dBATCH', f'-sOutputFile={outfile}', infile
    ])
