# Bill PDF Parser

Parse the PDF versions of utility bills for automated input to expenses spreadsheet.

## Development instructions
### Rebuilding Docker image
```bash
$ export GIT_HASH=$(git rev-parse HEAD)
$ docker build --build-arg GIT_HASH=${GIT_HASH::7} -t billreader .
```

### Test Docker image
```bash
$ docker run --rm billreader billsample
# should output the parsed values from two PDFs

$ docker run --rm billreader -h
# displays help
```

### Starting a shell in the container
Since an entrypoint is defined, you must redefine it:
```bash
$ docker run --rm -it --entrypoint=/bin/bash billreader
```

## Actual usage
```bash
$ docker run --rm --mount type=bind,src=/path/to/inputs/,dst=/common billreader utilitybill.pdf
# where utilitybill.pdf exists in /path/to/inputs on Docker host
```

## Resources
* [pdfminer.six](https://pdfminersix.readthedocs.io)
* [Yet Another Python Logging Setup](https://stackoverflow.com/questions/45287578/yet-another-python-logging-setup)
* [Simple logging demo](https://github.com/stevekm/logging-demo)
* [Practical Guide toUsing Setup.py](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)