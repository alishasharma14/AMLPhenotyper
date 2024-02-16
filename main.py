from tkinter import Tk
import fcsparser
import pandas as pd
import os
from gui import MyApp


def main():
    # Create the main window
    root = Tk()

    # Create an instance of your application
    app = MyApp(root)

    # Set the window size
    root.geometry("1500x700")

    # Start the main event loop
    root.mainloop()





if __name__ == "__main__":
    main()
