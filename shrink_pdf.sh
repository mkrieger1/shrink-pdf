#!/bin/sh

# Rewrite a PDF using GhostScript to hopefully make it smaller
# (works well with PDFs created by Microsoft Print to PDF).
#
# Source:
# https://stackoverflow.com/questions/10450120/optimize-pdf-files-with-ghostscript-or-other

# This part is based on pdf2ps.
if [ $# -eq 2 ]
then
    outfile=$2
elif [ $# -eq 1 ]
then
    outfile=`basename "$1" \.pdf`.out.pdf
else
    echo "Usage: `basename \"$0\"` input.pdf [output.pdf]" 1>&2
    exit 1
fi

gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH -sOutputFile="$outfile" "$1"
