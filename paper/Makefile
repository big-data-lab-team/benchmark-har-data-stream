all:
	pdflatex paper.tex
	bibtex paper
	pdflatex paper.tex
	pdflatex paper.tex

fast:
	pdflatex paper.tex

clean:
	rm -f paper.aux paper.bbl paper.blg paper.log paper.pdf paper.out paper.toc
