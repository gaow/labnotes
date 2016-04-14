notes := example.notes
slides := example.snotes
PDF := latex1 latex2 beamer1
MD := md1
objects := $(addsuffix .pdf, $(PDF)) $(addsuffix .rmd, $(MD)) labnotes/index.html
all: $(objects)

latex1.pdf: $(notes)
	tigernotes doc $(notes) --author "J. Doe" \
		--title "Example documentation" -f --lite --output latex1

latex2.pdf: $(notes)
	tigernotes doc $(notes) --author "J. Doe" \
		--title "Example documentation" -f --output latex2

beamer1.pdf: $(slides)
	tigernotes slides $(slides) --author "J. Doe" \
		--title "Example documentation" -f --output beamer1

md1.rmd: $(notes)
	tigernotes markdown $(notes) -o md1 --suffix rmd

labnotes/index.html:
	tigernotes admin --md md1.rmd --pdf $(notes) -o labnotes

clean:
	rm -f $(objects)
