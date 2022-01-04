# Bill PDF Parser

Parse the PDF versions of utility bills for automated input to expenses spreadsheet.

## Usage
```bash
$ docker run --rm --mount type=bind,src=/path/to/inputs/,dst=/common billreader utilitybill.pdf

$ docker run --rm billreader -h
# displays help
```
where `utilitybill.pdf` exists in `/path/to/inputs` on Docker host

### The Full Picture
Each month, download the PDF bill from each vendor and drop in `~/Documents/Utilities`. 

There is an Automator Folder Action workflow watching this folder (verify with 
<kbd>⌘</kbd>+<kbd>Space</kbd> "Folder Actions Setup") set up with the following tasks:
1. Get Selected Finder Items
2. Run Shell Script
   - Shell: `/bin/zsh`
   - Pass input: `as arguments`
```bash
# Make docker available to shell
export PATH=/usr/local/bin:$PATH

# Set output file for docker logs
outpath=~/Documents/Utilities/docker.log

docker run \
    --rm \
    --mount type=bind,src=/Users/dtork/Documents/Utilities,dst=/common \
    billreader $1 >> $outpath 2>&1
```
3. Display Notification (optional)
   - Title: Utility bill parsed
   - Message: File processed in watch folder.

## Development instructions
### Rebuilding Docker image
```bash
$ export GIT_HASH=$(git rev-parse HEAD)
$ docker build --build-arg GIT_HASH='${GIT_HASH::7}' -t billreader .
```

### Starting a shell in the container
Since an entrypoint is defined, you must redefine it:
```bash
$ docker run --rm -it --entrypoint=/bin/bash billreader
```

## Resources
* [pdfminer.six](https://pdfminersix.readthedocs.io)
* [Yet Another Python Logging Setup](https://stackoverflow.com/questions/45287578/yet-another-python-logging-setup)
* [Simple logging demo](https://github.com/stevekm/logging-demo)
* [Practical Guide toUsing Setup.py](https://godatadriven.com/blog/a-practical-guide-to-using-setup-py/)
