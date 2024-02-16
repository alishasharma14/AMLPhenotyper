import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import fcsparser
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import webbrowser

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AML Phenotyper")

        # Initialize the selected_file_path and text_widget attributes
        self.selected_file_path = None
        self.text_widget = None

        # Dictionary to store thresholds for each parameter
        self.thresholds = {}

        # Create main frames or widgets
        self.create_menu_bar()
        self.create_main_content()

    def create_menu_bar(self):
        # Create and configure a menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Create File menu with an Exit command
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select File", command=self.parameters)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="fcstocsv", command=self.convert_and_download)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_separator()
        menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_separator()
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_separator()
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_main_content(self):
        self.text_widget = tk.Text(self.root, wrap="word", width=40, height=10)
        self.text_widget.grid(row=1, column=0, sticky="nsew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Listbox to display parameters in a column at the top
        self.parameters_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, exportselection=False)
        self.parameters_listbox.grid(row=0, column=0, sticky="nsew", columnspan=2)

        # Scrollbar for the Listbox
        scrollbar = tk.Scrollbar(self.root, command=self.parameters_listbox.yview)
        scrollbar.grid(row=0, column=2, sticky="nsew")
        self.parameters_listbox.config(yscrollcommand=scrollbar.set)

        selected_params_label = tk.Label(self.root, text="Selected Parameters:")
        selected_params_label.grid(row=2, column=0, sticky="w")

        self.selected_params_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.selected_params_listbox.grid(row=3, column=0, sticky="nsew")

        # Bind a function to handle parameter selection
        self.parameters_listbox.bind("<ButtonRelease-1>", self.select_parameter)

        # Scrollbar for selected params
        scrollbar2 = tk.Scrollbar(self.root, command=self.selected_params_listbox.yview)
        scrollbar2.grid(row=0, column=2, sticky="nsew")
        self.selected_params_listbox.config(yscrollcommand=scrollbar2.set)

        # Button to indicate when finished selecting parameters
        finish_button = tk.Button(self.root, text="Finish Selection", command=self.enter_threshold)
        finish_button.grid(row=4, column=0, sticky="nsew")



    def open_file_explorer(self):
        # Open a file dialog and store the selected file path
        file_path = filedialog.askopenfilename(title="Open File")
        if file_path:
            print("Selected file:", file_path)
            self.selected_file_path = file_path  # Set instance variable directly
            print("Updated selected file:", self.selected_file_path)

            self.parameters()  # Call parameters method after setting the selected file path
            self.fcs_to_csv(file_path)  # Pass the selected file path to fcs_to_csv

    def save_file(self):
        print("Save action triggered")

    def fcs_to_csv(self, filepath=""):
        # Check if filepath is provided
        if not filepath:
            messagebox.showerror("Error", "No file selected.")
            return

        # Create the "CSV_Files" directory if it doesn't exist
        output_directory = "CSV_Files"
        os.makedirs(output_directory, exist_ok=True)

        # File locations
        output_csv_file = os.path.join(output_directory, f'converted_{os.path.basename(filepath)}.csv')

        try:
            # Parse the FCS file
            metadata, data = fcsparser.parse(filepath, reformat_meta=True)

            # Check if the '$PAR' key is present in metadata
            if '$PAR' not in metadata:
                messagebox.showerror("Error", "Invalid FCS file. '$PAR' key not found in metadata.")
                return

            # Convert to Pandas DataFrame
            df = pd.DataFrame(data)

            # Save DataFrame to CSV file
            df.to_csv(output_csv_file, index=False)

            # Inform the user about the conversion
            messagebox.showinfo("Conversion Complete", f"FCS file converted and saved as {output_csv_file}")

            # Automatically open the converted CSV file
            webbrowser.open(output_csv_file)

        except Exception as e:
            messagebox.showerror("Error", f"Error during conversion: {str(e)}")

    def convert_and_download(self):
        if self.selected_file_path:
            # Use the existing CSV file path
            print("Using existing CSV file path:", self.selected_file_path)
            self.configure_phenotypes(0)  # 0 is a placeholder for tvalue, adjust as needed
        else:
            # Trigger file explorer to select an FCS file
            self.open_file_explorer()
            print("After convert and download - selected file path: ", self.selected_file_path)

    def parameters(self):
        # Open a file dialog and store the selected CSV file path
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # Read the CSV file and extract the header (parameter names)
            try:
                df = pd.read_csv(file_path, nrows=1)  # Read only the first row
                parameters = df.columns.tolist()

                # Update the Listbox to display parameters in a column
                self.parameters_listbox.delete(0, tk.END)  # Clear existing items
                for parameter in parameters:
                    self.parameters_listbox.insert(tk.END, parameter)

                # Update the selected_file_path
                self.selected_file_path = file_path
                print("Parameters - selected_file_path:", self.selected_file_path)

                # Prompt user to enter threshold for each selected parameter
                for param in parameters:
                    if param in self.selected_params_listbox.get(0, tk.END):
                        threshold = simpledialog.askinteger("Threshold", f"Enter Threshold Value for {param}: ")
                        if threshold is not None:
                            self.thresholds[param] = threshold
                        else:
                            print(f"No threshold entered for {param}")

            except Exception as e:
                messagebox.showerror("Error", f"Error reading CSV file: {str(e)}")

    def select_parameter(self, event):
        selected_index = self.parameters_listbox.curselection()
        if selected_index:
            selected_param = self.parameters_listbox.get(selected_index)

            # Check if the parameter is already in the selected_params_listbox
            if selected_param not in self.selected_params_listbox.get(0, tk.END):
                self.selected_params_listbox.insert(tk.END, selected_param)
            else:
                messagebox.showinfo("Info", f"{selected_param} already selected.")

    def enter_threshold(self):
        # Get the selected parameters
        selected_parameters = self.selected_params_listbox.get(0, tk.END)

        # Check if parameters are selected
        if not selected_parameters:
            messagebox.showwarning("Warning", "Please select parameters.")
            return

        # Prompt user to enter threshold for selected parameters
        for param in selected_parameters:
            threshold = simpledialog.askinteger("Threshold", f"Enter Threshold Value for {param}: ")
            if threshold is not None:
                self.thresholds[param] = threshold
            else:
                print(f"No threshold entered for {param}")

        # After entering thresholds, call configure_phenotypes
        self.configure_phenotypes()



    def configure_phenotypes(self):
        # Get the selected parameters
        selected_parameters = self.selected_params_listbox.get(0, tk.END)

        # Check if parameters are selected
        if not selected_parameters:
            messagebox.showwarning("Warning", "Please select parameters.")
            return

        # Check if thresholds are entered for all selected parameters
        for param in selected_parameters:
            if param not in self.thresholds:
                messagebox.showwarning("Warning", f"Please enter threshold for parameter {param}.")
                return

        # Print the selected file path for debugging
        print("configure_phenotypes - Selected file path:", self.selected_file_path)

        # Read the entire CSV file, considering only the selected parameters
        try:
            df = pd.read_csv(self.selected_file_path, usecols=selected_parameters)
            print("configure_phenotypes - DataFrame:")
            print(df)  # Add this line to print the DataFrame for debugging

            # Determine phenotypes for each row based on threshold and parameters
            phenotypes = ""
            for index, row in df.iterrows():
                phenotype = ""
                for param in selected_parameters:
                    value = row[param]
                    if value < self.thresholds[param]:
                        phenotype += "N"
                    elif value > self.thresholds[param]:
                        phenotype += "P"
                    else:
                        phenotype += "0"
                phenotypes += phenotype + "\n"

            # Print all phenotypes to the console
            print("All Phenotypes:")
            print(phenotypes)

            self.create_csv_with_phenotypes(selected_parameters, phenotypes)

        except Exception as e:
            # Print the error for debugging
            print("configure_phenotypes - Error reading CSV file:", str(e))
            messagebox.showerror("Error", f"Error reading CSV file: {str(e)}")

    def process_data_in_chunks(self, file_path, selected_parameters, phenotypes):
        chunk_size = 1000  # Adjust the chunk size as needed
        reader = pd.read_csv(file_path, usecols=selected_parameters, chunksize=chunk_size)

        output_chunks = []

        for chunk in reader:
            # Process each chunk
            chunk["Phenotypes"] = phenotypes[:len(chunk)]
            output_chunks.append(chunk)

        return pd.concat(output_chunks)

    def create_csv_with_phenotypes(self, selected_parameters, phenotypes):
        if not self.selected_file_path:
            messagebox.showwarning("Warning", "No file selected.")
            return

        try:
            # Process data in chunks
            modified_df = self.process_data_in_chunks(self.selected_file_path, selected_parameters, phenotypes)

            # Determine the output CSV file path
            output_directory = "CSV_Files"
            os.makedirs(output_directory, exist_ok=True)
            output_csv_file = os.path.join(output_directory, f'phenotyped_{os.path.basename(self.selected_file_path)}')

            # Save the modified DataFrame to a new CSV file
            modified_df.to_csv(output_csv_file, index=False)

            # Inform the user about the creation of the new CSV file
            messagebox.showinfo("CSV Created", f"CSV file with phenotypes created: {output_csv_file}")

            phenotype_frequency = self.count_phenotype_frequency(output_csv_file)

        # Print phenotype frequency
            self.print_phenotype_frequency(phenotype_frequency)

        except Exception as e:
            messagebox.showerror("Error", f"Error creating CSV with phenotypes: {str(e)}")

    def count_phenotype_frequency(self, file_path):
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)

            # Get the last column which contains phenotypes
            phenotypes = df.iloc[:, -1]

            # Count the frequency of each phenotype
            phenotype_frequency = {}
            for phenotype in phenotypes:
                phenotype = phenotype.strip()  # Remove any leading/trailing whitespace
                if phenotype in phenotype_frequency:
                    phenotype_frequency[phenotype] += 1
                else:
                    phenotype_frequency[phenotype] = 1

            return phenotype_frequency

        except Exception as e:
            print("Error counting phenotype frequency:", e)
            return None

    def print_phenotype_frequency(self, phenotype_frequency):
        try:
            # Print the phenotype frequency
            print("Phenotype Frequency:")
            seen_phenotypes = set()
            for phenotype, frequency in phenotype_frequency.items():
                if phenotype not in seen_phenotypes:
                    print(f"{phenotype}: {frequency}")
                    seen_phenotypes.add(phenotype)

        except Exception as e:
            print("Error printing phenotype frequency:", e)



def main():
    # Create the main window
    root = tk.Tk()

    # Create an instance of your application
    app = MyApp(root)

    # Set the window size
    root.geometry("600x400")

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
