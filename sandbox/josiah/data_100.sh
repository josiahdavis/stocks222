# Download and unzip the data
curl -0 http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/100_Portfolios_10x10_CSV.zip > ../data/100_Portfolios_10x10_CSV.zip
unzip -p ../data/100_Portfolios_10x10_CSV.zip > ../data/100_Portfolios_10x10_CSV.csv

# Put the top 100 rows in a spreadsheet for visual inspection
head -n 100 ../data/100_Portfolios_10x10_CSV.csv > ../data/subset_100_Portfolios_10x10_CSV.csv
