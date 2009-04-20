FILES=design_report.tex
INCL_FILES=sub_datap.tex
TEX=pdflatex
index=makeindex
all: ${INCL_FILES}
	${TEX} ${FILES}
	bibtex ${FILES:.tex=}
	${TEX} ${FILES}
	${TEX} ${FILES}
	
clean: 
	rm -f *.aux *.log design_report.pdf *.toc *.idx *.ind

index: ${INCL_FILES}
	${TEX} ${FILES}
	${index} ${FILES:.tex=.idx}
	${TEX} ${FILES}
