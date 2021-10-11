rat2py
===============================
A solution for reading custom objects in ROOT files included by RAT-PAC.
This code is a modified version of the sibyl code found on the WM github page. 


Installation
------------
To install, first make sure you source ROOT and RAT-PAC

    $ source <root_install>/bin/thisroot.sh
    $ source <ratpac_install>/bin/ratpac.sh

then continue using pip

    $ git clone https://github.com/gmwendel/rat2py
    $ cd rat2py
    $ pip install -e .

Usage
-----

After installing, a python package is generated called snake that provides 
functions to read the data with.  See examples 

```
from rat2py import snake
```

Check snake.py and fastrat.cpp for details.  An example for converting MC
data into the format HITMAN uses is included inside examples/


Dependencies
------------
### Required
- Python3
- rat-pac (compiled with ROOT-6)

TODO
----
- [ ] Add particle type
- [ ] Add absolute event time
- [ ] Add better examples
