#!/bin/bash

################################################################################
# Contents of the automator terminal script:
	# shell: /bin/zsh
	# input given as: arguments
# 
# ~/Documents/billreader/folder_action_ingest.sh $1
# 
# --------------------------------------------------
# 
# Upon a new file being dropped in ~/tmp/bill_dropbox, a folder action runs an
# Automator script which takes the full path of that file and passes it to a 
# shell. That shell runs a single command (to keep the Automator script as simple
# as possible) which is a call to this shell script. 

# This shell script calls a python script which renames the file, adding its 
# modification timestamp to the filename, and returns the new filename. With
# the new filename, this script proceeds to make a backup copy of the file and
# move the original to object storage.
# 
################################################################################
# Set output file for output log
logfile=~/tmp/billreader_automator.log
touch $logfile

# Define locations
ingest_dir=~/OneDrive/Documents/Utilities_drop/
staging_dir=~/OneDrive/Documents/Utilities_staging/
bucket_dest='ibm/utilitybillreader/raw/'

ingest_rename () {
	newfile="$(python3 ~/Documents/Python/bill-pdfs/ingest_rename.py "$1")"
	if [ $? -eq 0 ]; then
		mv "$newfile" "$staging_dir"
	fi
}

cd $ingest_dir || exit  # if cd fails, exit
for raw_file in *.pdf; do
  if [ -f "$raw_file" ]; then
    ingest_rename "$raw_file"
  fi
done

mc cp "$staging_dir/*" "$bucket_dest"
if [ $? -eq 0 ]; then
  rm "$staging_dir/*"
fi
