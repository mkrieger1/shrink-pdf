import subprocess
import sys
from os.path import basename, splitext


def call_gs(infile: str) -> bytes:
    return subprocess.check_output([
        'gs', '-dNOPAUSE', '-dBATCH',
        '-dSAFER', '-q', '-sOutputFile=-',
        '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/ebook',
        infile
    ])


def write_result(result: bytes, outfile: str) -> None:
    with open(outfile, 'wb') as f:
        f.write(result)


def main() -> None:
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

    try:
        result = call_gs(infile)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e)
    write_result(result, outfile)
