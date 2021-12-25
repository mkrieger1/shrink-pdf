import argparse
import subprocess
from os.path import basename, getsize, splitext


def call_gs(infile: str) -> bytes:
    return subprocess.check_output([
        'gs', '-dNOPAUSE', '-dBATCH',
        '-dSAFER', '-q', '-sOutputFile=-',
        '-sDEVICE=pdfwrite', '-dPDFSETTINGS=/ebook',
        infile
    ])


def write_result_if_smaller(
    infile: str, result: bytes, outfile: str, max_percent: float = 60,
    check_only: bool = False
) -> bool:
    """Write the output file if it is sufficiently small.

    :param infile: Path to input file (used to determine size)
    :param result: Data to write
    :param outfile: Path to output file
    :param max_percent:
        Write only if result is smaller than this percentage of the input
    :param check_only:
        Do not write, just print a message of the result size

    :return: True if output file was written, False otherwise
    """
    input_size = getsize(infile)
    max_size = int(input_size / 100 * max_percent)
    output_size = len(result)

    if output_size > max_size or check_only:
        print(
            f'{infile}: {input_size} -> {output_size} bytes '
            f'({output_size / input_size * 100:.0f} %)'
        )
        return False

    with open(outfile, 'wb') as f:
        f.write(result)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Rewrite a PDF file using GhostScript to make it smaller'
    )
    parser.add_argument('infile', metavar='input.pdf')
    parser.add_argument(
        '-o', dest='outfile', metavar='output.pdf',
        help=(
            'Path to output file '
            '(a filename in the working directory is chosen by default)'
        )
    )
    parser.add_argument(
        '-m', dest='max_percent', type=float, default=60,
        help=(
            'Write output file only if it would be smaller '
            'than this percentage of the input file size'
        )
    )
    parser.add_argument(
        '-c', dest='check_only', action='store_true',
        help='Just check the result size, do not write the file'
    )
    args = parser.parse_args()

    if not args.outfile:
        fullname = basename(args.infile)
        name, ext = splitext(fullname)
        if ext != '.pdf':
            name = fullname
        args.outfile = f'{name}.out.pdf'

    try:
        result = call_gs(args.infile)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e)
    write_result_if_smaller(
        args.infile, result, args.outfile,
        max_percent=args.max_percent, check_only=args.check_only
    )
