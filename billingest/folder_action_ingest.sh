#!/bin/bash

################################################################################
# Contents of the automator terminal script:
	# shell: /bin/zsh
	# input given as: arguments
# 
# ~/Documents/Python/bill-pdfs/billingest/folder_action_ingest.sh
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
# Define cloud provider for uploads (one of s3 | gcs |ibm)
CLOUD_SERVICE=gcs

# Load the environment
export PATH=/usr/local/bin:$PATH

# Define locations
ingest_dir=~/OneDrive/Documents/Utilities_drop
staging_dir=~/OneDrive/Documents/Utilities_staging
bucket_dest="$CLOUD_SERVICE/utilitybillreader/raw/"

ingest_rename () {
	newfile="$(python3 ~/Documents/Python/bill-pdfs/billingest/ingest_rename.py "$1")"
	echo "$1 --renamed--> $newfile"
	if [ $? -eq 0 ]; then
		mv "$newfile" "$staging_dir"
	fi
}

cd $ingest_dir || exit  # if cd fails, exit

# Check each file exists first, then rename it and move to staging
for raw_file in *.pdf; do
  if [ -f "$raw_file" ]; then
    ingest_rename "$raw_file"
  fi
done

# Move all staged PDFs to cloud bucket with minio client
cp "$staging_dir/$newfile" "$HOME/Documents/Utilities/$newfile"
mc find $staging_dir --name "*.pdf" --exec "mc mv {} $bucket_dest"
