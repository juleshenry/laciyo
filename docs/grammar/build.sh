#!/bin/bash
cd "$(dirname "$0")" || exit 1

# MacTeX / BasicTeX usually puts binaries here:
export PATH="/Library/TeX/texbin:$PATH"

pdflatex grammar.tex