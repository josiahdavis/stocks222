# Download and unzip the data
curl -0 http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/48_Industry_Portfolios_daily_CSV.zip > ../data/48_Industry_Portfolios_daily.zip
unzip -p ../data/48_Industry_Portfolios_daily.zip > ../data/48_Industry_Portfolios_daily.csv

# Put the top 100 rows in a spreadsheet for visual inspection
head -n 100 ../data/48_Industry_Portfolios_daily.csv > ../data/subset_48_Industry_Portfolios_daily.csv
