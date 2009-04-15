FILES=design_report.tex
INCL_FILES=sub_datap.tex
TEX=pdflatex
index=makeindex
all: ${INCL_FILES}
	${TEX} ${FILES}
	${TEX} ${FILES}
clean: 
	rm -f *.aux *.log *.pdf *.toc

index: ${INCL_FILES}
	${TEX} ${FILES}
	${index} ${FILES:.tex=.idx}
	${TEX} ${FILES}
