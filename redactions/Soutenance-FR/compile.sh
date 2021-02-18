#!/bin/bash
pdflatex -draftmode Soutenance.tex
bibtex Soutenance.aux
pdflatex -draftmode Soutenance.tex
pdflatex Soutenance.tex