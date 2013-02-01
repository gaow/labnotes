SRC=`pwd`/src/tigernotes
PYI2DIR=$@
python $PYI2DIR/pyinstaller.py -F $SRC 
mv dist/* .
rm -rf build dist *.spec
