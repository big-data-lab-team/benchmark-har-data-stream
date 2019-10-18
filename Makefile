all:
	pdflatex exam.tex
	bibtex exam
	pdflatex exam.tex
	pdflatex exam.tex

clean:
	rm -f exam.aux exam.bbl exam.blg exam.log exam.pdf exam.out exam.toc
