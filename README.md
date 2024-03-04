**AML Phenotyper**

**Prerequisites**: 
  Python 3.x installed
    **Required Python libraries:**
    tkinter
    pandas
    fcsparser
    reportlab
    webbrowser
    
**The application generates the following output files:**
Converted CSV Files: CSV files converted from FCS format.
Phenotyped CSV Files: CSV files containing phenotypes based on user-defined thresholds.
Parameter Threshold CSV File: CSV file containing the thresholds set for each parameter.
Phenotype Frequency CSV File: CSV file containing the frequency of each phenotype generated.

**Usage:**
Run Main to start 

  Converting FCS Files to CSV: 
  * hover over "file" in the top left corner and select "FCS to CSV" 
  * select the file(s) from file explorer that are to be converted
  * the converted files will open on your computer and will also be in the CSV file directory
  * download the csv files in order to use them for phenotyping 

  Configuring Phenotypes, Phenotype Frequency, etc.: 
  * hover over "file" in the top left corner and select "Select File"
  * select a csv file from file explorer (if a .csv file is not selected, or the file is in improper format, parameters from the file will not be shown)
  * select the parameters from the box to be considered (double click a chosen parameter in the second box to remove)
  * after selecting all parameters, click "Finish Selection" at the bottom of the screen
  * enter thresholds for each parameter in the appearing textboxes
  * after thresholds are entered, three csv files will be in the CSV Files directory (phenotypes, frequency, and threshold files)
  * open the files in explorer to view 
