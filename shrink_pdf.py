import subprocess
import sys
from os.path import basename, getsize, splitext


def call_gs(infile: str) -> bytes:
    return subprocess.check_output([
        'gs', '-dNOPAUSE', '-dBATCH',
        '-dSAFER', '-q', '-sOutputFile=-',
        '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/ebook',
        infile
    ])


def write_result_if_smaller(
    infile: str, result: bytes, outfile: str, max_percent: float = 60
) -> bool:
    """Write the output file if it is sufficiently small.

    :param infile: Path to input file (used to determine size)
    :param result: Data to write
    :param outfile: Path to output file
    :param max_percent:
        Write only if result is smaller than this percentage of the input

    :return: True if output file was written, False otherwise
    """
    input_size = getsize(infile)
    max_size = int(input_size / 100 * max_percent)
    output_size = len(result)

    if output_size > max_size:
        print(
            f'{infile}: {input_size} -> {output_size} bytes '
            f'({output_size / input_size * 100:.0f} %)'
        )
        return False

    with open(outfile, 'wb') as f:
        f.write(result)
    return True


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
    write_result_if_smaller(infile, result, outfile)
