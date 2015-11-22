# cython-builder

The cython-builder script is an example setup.py script that turns all of your Python files into compiled C code using [Cython](http://cython.org).

This is an example project; only the setup.py file is live code here. Feel free to use it in your own projects!

## Usage

Run `python setup.py compile` to compile all `.py` and `.pyx` files in the current working tree into compiled libraries.
If you want, you can also pass the `--inplace` argument, which will create the compiled output in the same working tree.

To clean out your compiled code, run `python setup.py clean`.
