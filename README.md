# pyfintech

A library consists of some technical analysis methods for trading.

All technical analysis methods in this library assume that an array of "Rate" class instances is ready to be analysed.

As an example, European Central Bank foreign exchange rates are used which are served for free on their web site in XML file format. These values are stored in MongoDB for later use.

Output of example is going to be created as PNG file by seaborn library.

Whole example code can be found on main file.


Included technical analysis methods:
------------------------------------
* RSI - Relative Strength Index
* Three Line Break