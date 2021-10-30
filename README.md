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

$ docker run --rm billreader billreader -h
# displays help
```

## Resources
* [pdfminer.six](https://pdfminersix.readthedocs.io)
