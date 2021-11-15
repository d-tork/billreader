docker run \
  --rm \
  --mount type=bind,src="$(pwd)"/output,dst=/bill-pdfs/output \
  billreader ~/Documents/Utilities/power_2021-01-11.pdf
