import tkinter as tk
from tkinter import ttk, messagebox
import math

class SquareRooter:
    def __init__(self, root):
        self.root = root
        self.root.title("SquareRooter")
        self.root.geometry("750x700")  # Wider window for higher precision
        self.root.resizable(False, False)

        self.setup_ui()

    def setup_ui(self):
        # Main frame with a light background
        self.main_frame = tk.Frame(self.root, bg="#f5f5f5", padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)

        # Title
        tk.Label(self.main_frame, text="SquareRooter", font=("Arial", 18, "bold"), bg="#f5f5f5", fg="#333333").pack(pady=(0, 15))

        # Instructions
        tk.Label(self.main_frame, text="Enter a range to explore numbers, their squares, and square roots.\nPerfect squares are highlighted in green.", 
                 bg="#f5f5f5", fg="#555555", font=("Arial", 10), justify="center").pack(pady=(0, 20))

        # Input frame for start, end, and step
        input_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        input_frame.pack(fill="x", pady=10)

        tk.Label(input_frame, text="Start:", bg="#f5f5f5", fg="#555555", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.start_entry = tk.Entry(input_frame, width=10, font=("Arial", 10), fg="black", bg="white", insertbackground="black", borderwidth=2, relief="flat")
        self.start_entry.grid(row=0, column=1, padx=5)
        self.start_entry.insert(0, "1")

        tk.Label(input_frame, text="End:", bg="#f5f5f5", fg="#555555", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.end_entry = tk.Entry(input_frame, width=10, font=("Arial", 10), fg="black", bg="white", insertbackground="black", borderwidth=2, relief="flat")
        self.end_entry.grid(row=0, column=3, padx=5)
        self.end_entry.insert(0, "20")

        tk.Label(input_frame, text="Step:", bg="#f5f5f5", fg="#555555", font=("Arial", 10)).grid(row=0, column=4, padx=5)
        self.step_entry = tk.Entry(input_frame, width=10, font=("Arial", 10), fg="black", bg="white", insertbackground="black", borderwidth=2, relief="flat")
        self.step_entry.grid(row=0, column=5, padx=5)
        self.step_entry.insert(0, "1")

        # Generate button
        self.generate_button = ttk.Button(self.main_frame, text="Generate Table", command=self.generate_table)
        self.generate_button.pack(pady=20)
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 10), padding=5, background="#4CAF50", foreground="white")
        style.map("TButton", background=[("active", "#388E3C")], foreground=[("active", "white")])

        # Text area with scrollbar
        self.text_frame = tk.Frame(self.main_frame, bg="#f5f5f5")
        self.text_frame.pack(fill="both", expand=True)
        
        self.text_area = tk.Text(self.text_frame, height=20, width=80, font=("Courier", 11), bg="white", fg="black", wrap="none")
        self.text_area.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(self.text_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Explanation
        tk.Label(self.main_frame, text="Why it works: √x is the number that, when squared, gives x (e.g., √9 = 3 because 3² = 9).\nPerfect squares have whole-number roots.", 
                 bg="#f5f5f5", fg="#555555", font=("Arial", 9, "italic"), justify="center").pack(pady=(15, 0))

    def is_perfect_square(self, n):
        # Check if a number is a perfect square with very high precision
        root = math.isqrt(int(n * 100000000000000)) / 10000000  # Scale for 12 decimal places
        return abs(root * root - n) < 0.000000000001 and n >= 0

    def generate_table(self):
        try:
            start = float(self.start_entry.get())
            end = float(self.end_entry.get())
            step = float(self.step_entry.get())
            if start > end or step <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers: Start ≤ End, Step > 0")
            return

        # Clear previous content
        self.text_area.delete(1.0, tk.END)
        header = f"{'Number':>14} | {'Square':>16} | {'Square Root':>22}\n{'-'*14}-+-{'-'*16}-+-{'-'*22}"
        self.text_area.insert(tk.END, header + "\n")

        # Generate table with higher precision
        current = start
        while current <= end + 0.000000000001:  # Buffer for float precision
            square = current * current
            sqrt = math.sqrt(current)
            line = f"{current:>14.6f} | {square:>16.6f} | {sqrt:>22.12f}"
            self.text_area.insert(tk.END, line)
            if self.is_perfect_square(current):
                self.text_area.tag_add("perfect", f"{self.text_area.index(tk.END)} linestart", f"{self.text_area.index(tk.END)} lineend")
                self.text_area.tag_config("perfect", background="#c8e6c9")  # Light green highlight
            self.text_area.insert(tk.END, "\n")
            current += step

    def run(self):
        self.root.mainloop()

# Run the program
if __name__ == "__main__":
    root = tk.Tk()
    app = SquareRooter(root)
    app.run()