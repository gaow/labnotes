notes := example.notes
slides := example.snotes
PDF := l1 l2 b1
MD := md1
objects := $(addsuffix .pdf, $(PDF)) $(addsuffix .rmd, $(MD)) labnotes/index.html
all: $(objects)

l1.pdf: $(notes)
	labnotes doc $(notes) --author "J. Doe" \
		--title "Example documentation" --lite --output l1

l2.pdf: $(notes)
	labnotes doc $(notes) --author "J. Doe" \
		--title "Example documentation" --footnote --output l2

b1.pdf: $(slides)
	labnotes slides $(slides) --author "J. Doe" \
		--title "Example documentation" --output b1

md1.rmd: $(notes)
	labnotes markdown $(notes) -o md1 --suffix rmd

labnotes/index.html:
	labnotes admin --md md1.rmd --pdf $(notes) -o labnotes \
		-a "Gao T. Wang" -t "My Text Processor" --description \
		"This is a tool that I built and use to manage pieces of notes since 2011. It compiles formatted notes into various types publishable documents."

clean:
	rm -f $(objects)
