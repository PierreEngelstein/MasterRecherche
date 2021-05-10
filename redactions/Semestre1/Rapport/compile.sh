#!/bin/bash
pdflatex -draftmode Rapport.tex
bibtex Rapport.aux
pdflatex -draftmode Rapport.tex
pdflatex Rapport.tex