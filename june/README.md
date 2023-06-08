## Install

The project uses Poetry, a package and virtual environment manager for Python.  
Installation instructions for poetry are [here](https://python-poetry.org/docs/). 
A TLDR is to do 

```
curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2
```

and then add `$HOME/.local/bin` to the Path. 
```
export PATH="$HOME/.poetry/bin:$PATH"
```

Check for installation using `poetry --version` and make sure it shows `1.4.2`.

Once you have Poetry setup, you can simply go to the root of the directory and do

```
make install
```

## Tests

The project has static checks, which checks for formatting and typing and unit tests.

Invoke static checks using

```
make check
```

and tests using

```
make test
```


## Run

The game can be run by doing

```
make run
```

Game play instructions are prompted on the screen.