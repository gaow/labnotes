## A tool that I built and use to manage pieces of notes since 2011

Please checkout the sample [input](https://github.com/gaow/labnotes/blob/master/vignette/example.notes) and [output]() first, then come back here for installation instructions if you are interested to give it a go. This software was designed and built for personal use. It served me well over the years but your mileage may vary.

## Installation

`labnotes` requires Python 3. If you do not have Python 3 on your system it is strongly recommended that you install Python 3 from `conda`.

### Download for Linux
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

### For MacOS
```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
bash Miniconda3-latest-MacOSX-x86_64.sh
```

Follow the prompt to install it (use `ctrl+F` to quickly jump to the end of the Licenses if you have read them before). Be sure to add the installation path to your shell environment (the installation script will ask if you'd like this be configured automatically: say Yes unless you know what you are doing).

After the program is installed, you have to reload your `bash` profile. If you do not know what this means, just exit the current terminal and open up a new one.

The you are ready to download and install `labnotes`:

```
git clone https://github.com/gaow/labnotes.git
cd labnotes
python setup.py install
```