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
# Upon a new file being dropped into `ingest_dir`, a folder action runs an
# Automator script which runs this shell script, to keep the Automator script
# as simple as possible.
# 
# This shell script loops through one or more new PDFs added to the 
# `ingest_dir`, calling a python script which renames the file (adding its 
# modification timestamp to the filename), and returns the new filename. With
# the new filename, this script proceeds to make a backup copy of the file and
# move the original to object storage.
#
# These paths are hard-coded for The Spine's folder structure because this
# flow is specifically intended for a OneDrive-synced environment. And it does
# not make use of any Docker containers for ingest because the Docker engine
# is not continually running on The Spine.
# 
# In the future, perhaps I can skip straight to moving raw downloads to a 
# cloud bucket, where the renaming will be handled by a container.
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

cd $ingest_dir || exit  # if cd fails, exit

ingest_rename () {
	newfile="$(python3 ~/Documents/Python/bill-pdfs/billingest/ingest_rename.py "$1")"
	echo "$1 --renamed--> $newfile"
	if [ $? -eq 0 ]; then
		mv "$newfile" "$staging_dir"
	fi
}

# Check each file exists first, then rename it, move to staging, make a copy
for raw_file in *.pdf; do
  if [ -f "$raw_file" ]; then
    ingest_rename "$raw_file"
	cp "$staging_dir/$newfile" "$HOME/Documents/Utilities/$newfile"
  fi
done

# Move all staged PDFs to cloud bucket with minio client
mc find $staging_dir --name "*.pdf" --exec "mc mv {} $bucket_dest"
