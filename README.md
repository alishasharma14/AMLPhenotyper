# AML Phenotyper

## Overview
AML Phenotyper is a GUI-based Python application designed to automate flow cytometry data analysis for acute myeloid leukemia (AML) research. The tool converts FCS files to CSV format, applies user-defined parameter thresholds, and generates phenotype classifications and frequency reports, reducing manual data processing for researchers.

This project focuses on usability, data automation, and translating biomedical research workflows into a functional software tool.

---

## Features
- Converts FCS files to CSV for downstream analysis
- Interactive graphical user interface built with Tkinter
- User-defined parameter selection and thresholding
- Automated phenotype classification
- Generates structured output reports for analysis and review

---

## Tech Stack
- Python  
- Tkinter (GUI)
- Pandas (data processing)
- fcsparser (FCS file parsing)
- ReportLab (report generation)
- webbrowser (output file access)

---

## Output Files
The application generates the following files:
- **Converted CSV Files** – CSV files converted from FCS format
- **Phenotyped CSV Files** – CSV files containing phenotype assignments
- **Parameter Threshold CSV** – Records threshold values for each parameter
- **Phenotype Frequency CSV** – Summary of phenotype counts and frequencies

---

## Usage

### Running the Application
Run the main Python file to launch the GUI.

### Converting FCS Files to CSV
1. Open the application
2. Navigate to **File → FCS to CSV**
3. Select one or more `.fcs` files
4. Converted CSV files will open automatically and be saved in the CSV output directory
5. Download the CSV files for phenotyping

### Configuring Phenotypes
1. Navigate to **File → Select File**
2. Select a valid CSV file
3. Choose parameters to include in phenotyping  
   - Double-click a parameter to remove it
4. Click **Finish Selection**
5. Enter threshold values for each parameter
6. The application generates:
   - Phenotyped CSV file
   - Phenotype frequency CSV file
   - Threshold configuration CSV file
7. Open the generated files in file explorer to review results

---

## Notes
This project demonstrates applied data analysis, GUI design, and automation in a biomedical research context. It highlights the ability to convert domain-specific requirements into a usable software application.
