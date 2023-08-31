#import pandas as pd
#df = pd.read_csv(r'data/nutrition.csv')
#ostane = '0123456789.'
#test = df.itertuples()
#for row in df.itertuples():
#    for i in range(2, 78):
#        pociscen_podatek = ''
#        for j in range(len(row[i])):
#            if row[i][j] in ostane:
#                pociscen_podatek += row[i][j]
#        row[i] = pociscen_podatek
#df.to_csv('test.csv')


import csv
import pandas as pd

# Read the CSV file into a dataframe
df = pd.read_csv(r'data/nutrition.csv')

met = []
for col in df.columns:
    met.append(col) #met vsebuje imena stolpcev, dolzina je 77
met_ime = met[:2]
met = met[2:]
# Get the headings from the dataframe
headings = met_ime[1:] + met

# Create an empty list to store the modified rows
modified_rows = []
ostane = '0123456789.'
# Iterate over the rows in the dataframe
for index, row in df.iterrows():
    # Create a new row with the modified values
    new_row = [row[met_ime[1]]]
    for el in met:
        modified_value = ''
        str_row = str(row[el])
        if str_row == 'nan':
            str_row = '0'
        for znak in str_row:
            if znak in ostane:
                modified_value += znak
        new_row.append(modified_value)
    # Add the modified row to the list
    modified_rows.append(new_row)

# Write the headings and modified rows to the new CSV file
with open('data/modified.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headings)
    writer.writerows(modified_rows)