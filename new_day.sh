# Create a new day folder and copy the template files into it
YEAR=2023

# Get the day number from the command line
DAY=$1

# Create the folder
mkdir $YEAR/day$DAY

# Copy the template files into the folder
cp day_template/day0.py $YEAR/day$DAY/day$DAY.py
cp day_template/day0.ipynb $YEAR/day$DAY/day$DAY.ipynb
