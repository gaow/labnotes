## A tool that I built and use to manage pieces of notes since 2011

Please checkout the sample [input](https://github.com/gaow/labnotes/blob/master/vignette/example.notes) and [output](http://bioinformatics.org/labnotes) first, then come back here for installation instructions if you are interested to give it a go. This software was designed and built for personal use. It served me well over the years but your mileage may vary.

## Installation

To use this program with Debian Jessie the following packages for LaTeX should be installed:
```
sudo apt-get install texlive texlive-xetex texlive-latex-extra texlive-fonts-extra texlive-extra-utils texlive-font-utils latex-beamer pgf latexmk latex-xcolor texlive-pstricks 
```
For MacOS, you can install [MacTex](http://tug.org/mactex/).

In order to use `bookdown` with `labnotes bind`, you have to install `pandoc`. On Debian:
```
sudo apt-get install libcurl4-openssl-dev libssl-dev pandoc pandoc pandoc-citeproc
```

`labnotes` requires Python 3.4 or newer. If you have it, then you are ready to download and install `labnotes`:

```
git clone https://github.com/gaow/labnotes.git
cd labnotes
python setup.py install
```

If you do not have Python 3 on your system it is strongly recommended that you install Python 3 from `conda`.

Conda for Linux:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Conda for MacOS:
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```
