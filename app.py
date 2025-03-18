import tkinter as tk
import subprocess
import sys

# Function to run another Python file and close the GUI after execution
def run_script():
    process = subprocess.Popen(['python', 'krishna\krishna_2.py'])
    process.communicate()  # Wait for the process to finish
    root.quit()  # Close the GUI window after the script ends

# Set up the main window
root = tk.Tk()
root.title("Krishna")

# Set the window size
root.geometry("300x150")

# Create the start button
start_button = tk.Button(root, text="Start", command=run_script)
start_button.pack(pady=20)

# Run the main loop
root.mainloop()

# Exit the program when the GUI is closed
sys.exit()
