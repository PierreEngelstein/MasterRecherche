#!/bin/bash
pdflatex -draftmode Memoire.tex
bibtex Memoire.aux
pdflatex -draftmode Memoire.tex
pdflatex Memoire.tex