# Loop through new, renamed utility bills and process them to extract values.

cd /Users/dtork/Documents/Utilities/

files=(billdownload*)
for file in "${files[@]}";
do
	echo "$file"
	docker run --rm \
		--mount type=bind,src=/Users/dtork/Documents/Utilities,dst=/data \
		--mount type=bind,src=/Users/dtork/.billreader,dst=/run/config \
		halpoins/billreader \
		"$file"
done

	
