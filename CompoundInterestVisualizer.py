import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_total_contributing_monthly(initial_investment, monthly_contribution, years, avg_interest_rate):
    total = initial_investment
    monthly_rate = avg_interest_rate / 100 / 12  # Convert annual rate to monthly
    yearly_totals = [initial_investment]  # Start with initial investment
    
    for month in range(1, years * 12 + 1):  # Start from 1, go to years*12
        total = total * (1 + monthly_rate) + monthly_contribution
        if month % 12 == 0:  # At the end of each year
            yearly_totals.append(total)
   
    return total, yearly_totals

def calculate_total_contributing_yearly(initial_investment, yearly_contribution, years, avg_interest_rate):
    return calculate_total_contributing_monthly(initial_investment, yearly_contribution / 12, years, avg_interest_rate)

def calculate_total_alternate_contributions_monthly(years_to_switch, monthly_contributions_per_range, initial_investment, total_years, avg_interest_rate):
    # Years to switch is each year at which the contribution is switched.
    # contributions_per_range is the monthly contribution for each year between when you switch
    # For example, years_to_switch = [5, 10] and contributions_per_range = [10, 100, 1000]
    # Then for the first 5 years you contribute 10 monthly and then on year 6 (1 + 5), until year 10 it is 100 monthly 
    # and finally from year 11 to total years it is 1000 monthly
    years_to_switch = years_to_switch.copy()  # Create a copy so we don't modify the original
    years_to_switch.append(total_years)

    total = initial_investment
    overall_yearly_totals = [initial_investment]  # Start with just the initial investment

    index = 0
    for switch_year in years_to_switch:
        previous_year = 0
        if index != 0:
            previous_year = years_to_switch[index - 1]
        
        year_range = switch_year - previous_year
        # Calculate for this range, but don't use the returned yearly_totals directly
        monthly_rate = avg_interest_rate / 100 / 12
        contribution = monthly_contributions_per_range[index]
        
        # Manually calculate for each month in this range
        for month in range(1, year_range * 12 + 1):
            total = total * (1 + monthly_rate) + contribution
            if month % 12 == 0:  # At the end of each year
                overall_yearly_totals.append(total)
        
        index += 1

    return total, overall_yearly_totals

# Generated with Claude
class InvestmentCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Investment Calculator with Alternate Contributions")
        self.root.geometry("900x650")
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create main input frame
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Inputs")
        
        # Create results frame
        self.results_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.results_frame, text="Results")
        
        # Set up variables
        self.initial_investment_var = tk.DoubleVar(value=10000)
        self.interest_rate_var = tk.DoubleVar(value=6.0)
        self.total_years_var = tk.IntVar(value=30)
        
        # List to store contribution change entries
        self.contribution_entries = []
        
        # Set up the UI elements
        self.setup_main_ui()
        self.setup_results_ui()
        
    def setup_main_ui(self):
        # Basic input frame
        basic_frame = ttk.LabelFrame(self.main_frame, text="Basic Information")
        basic_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Initial investment
        ttk.Label(basic_frame, text="Initial Investment ($)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(basic_frame, textvariable=self.initial_investment_var, width=15).grid(row=0, column=1, padx=5, pady=5)
        
        # Interest rate
        ttk.Label(basic_frame, text="Annual Interest Rate (%)").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(basic_frame, textvariable=self.interest_rate_var, width=15).grid(row=1, column=1, padx=5, pady=5)
        
        # Total years
        ttk.Label(basic_frame, text="Total Years").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(basic_frame, textvariable=self.total_years_var, width=15).grid(row=2, column=1, padx=5, pady=5)
        
        # Contribution changes frame
        self.changes_frame = ttk.LabelFrame(self.main_frame, text="Contribution Changes")
        self.changes_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        
        # Initial contribution row
        ttk.Label(self.changes_frame, text="Initial Monthly Contribution ($)").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        initial_contribution_entry = ttk.Entry(self.changes_frame, width=15)
        initial_contribution_entry.grid(row=0, column=1, padx=5, pady=5)
        initial_contribution_entry.insert(0, "100")
        self.contribution_entries.append((0, initial_contribution_entry))
        
        # Buttons frame
        buttons_frame = ttk.Frame(self.main_frame)
        buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        
        # Add change button
        ttk.Button(buttons_frame, text="Add Contribution Change", command=self.add_contribution_change).grid(row=0, column=0, padx=5, pady=5)

        # Remove change button
        ttk.Button(buttons_frame, text="Remove Contribution Change", command=self.remove_contribution_change).grid(row=0, column=1, padx=5, pady=5)
        
        # Calculate button
        ttk.Button(buttons_frame, text="Calculate", command=self.calculate).grid(row=0, column=2, padx=5, pady=5)
            
    def setup_results_ui(self):
        # Create frames for the three tables
        table_frame1 = ttk.LabelFrame(self.results_frame, text="Yearly Results - 1% Interest")
        table_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        table_frame2 = ttk.LabelFrame(self.results_frame, text="Yearly Results")
        table_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        table_frame3 = ttk.LabelFrame(self.results_frame, text="Yearly Results + 1% Interest")
        table_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        # Create scrollable areas for each table
        # Table 1 (+ 1% Interest)
        self.results_canvas1 = tk.Canvas(table_frame1)
        scrollbar1 = ttk.Scrollbar(table_frame1, orient="vertical", command=self.results_canvas1.yview)
        self.scrollable_frame1 = ttk.Frame(self.results_canvas1)
        
        self.scrollable_frame1.bind(
            "<Configure>",
            lambda e: self.results_canvas1.configure(
                scrollregion=self.results_canvas1.bbox("all")
            )
        )
        
        self.results_canvas1.create_window((0, 0), window=self.scrollable_frame1, anchor="nw")
        self.results_canvas1.configure(yscrollcommand=scrollbar1.set)
        
        self.results_canvas1.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="right", fill="y")
        
        # Table 2 (Base Interest)
        self.results_canvas2 = tk.Canvas(table_frame2)
        scrollbar2 = ttk.Scrollbar(table_frame2, orient="vertical", command=self.results_canvas2.yview)
        self.scrollable_frame2 = ttk.Frame(self.results_canvas2)
        
        self.scrollable_frame2.bind(
            "<Configure>",
            lambda e: self.results_canvas2.configure(
                scrollregion=self.results_canvas2.bbox("all")
            )
        )
        
        self.results_canvas2.create_window((0, 0), window=self.scrollable_frame2, anchor="nw")
        self.results_canvas2.configure(yscrollcommand=scrollbar2.set)
        
        self.results_canvas2.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="right", fill="y")
        
        # Table 3 (- 1% Interest)
        self.results_canvas3 = tk.Canvas(table_frame3)
        scrollbar3 = ttk.Scrollbar(table_frame3, orient="vertical", command=self.results_canvas3.yview)
        self.scrollable_frame3 = ttk.Frame(self.results_canvas3)
        
        self.scrollable_frame3.bind(
            "<Configure>",
            lambda e: self.results_canvas3.configure(
                scrollregion=self.results_canvas3.bbox("all")
            )
        )
        
        self.results_canvas3.create_window((0, 0), window=self.scrollable_frame3, anchor="nw")
        self.results_canvas3.configure(yscrollcommand=scrollbar3.set)
        
        self.results_canvas3.pack(side="left", fill="both", expand=True)
        scrollbar3.pack(side="right", fill="y")
        
        # Graph frame
        graph_frame = ttk.LabelFrame(self.results_frame, text="Investment Growth")
        graph_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Create the figure for the plot
        self.fig = Figure(figsize=(12, 5), dpi=100)
        self.plot = self.fig.add_subplot(111)
        
        # Create canvas for the figure
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights for all columns
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=1)
        self.results_frame.columnconfigure(2, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        self.results_frame.rowconfigure(1, weight=1)
        
    def add_contribution_change(self):
        # Get the current number of entries
        row_count = len(self.contribution_entries)
        
        # Create new entry row
        ttk.Label(self.changes_frame, text=f"Change at Year").grid(row=row_count, column=0, padx=5, pady=5, sticky="w")
        year_entry = ttk.Entry(self.changes_frame, width=5)
        year_entry.grid(row=row_count, column=1, padx=5, pady=5)
        
        ttk.Label(self.changes_frame, text=f"New Monthly Contribution ($)").grid(row=row_count, column=2, padx=5, pady=5, sticky="w")
        contribution_entry = ttk.Entry(self.changes_frame, width=15)
        contribution_entry.grid(row=row_count, column=3, padx=5, pady=5)
        
        # Add to our entry list (year entry, contribution entry)
        self.contribution_entries.append((year_entry, contribution_entry))

    def remove_contribution_change(self):
        # Make sure there's at least one entry after the initial contribution
        if len(self.contribution_entries) <= 1:
            messagebox.showinfo("Information", "Cannot remove initial contribution.")
            return
        
        # Get the last entry's widgets
        last_index = len(self.contribution_entries) - 1
        year_entry, contribution_entry = self.contribution_entries[last_index]
        
        # Remove the widgets from the UI
        # We need to remove the labels too, which are not stored in contribution_entries
        # Find all grid slaves in the last row
        for widget in self.changes_frame.grid_slaves(row=last_index):
            widget.destroy()
        self.contribution_entries.pop()
    
    def validate_inputs(self):
        try:
            # Check basic inputs
            initial_investment = self.initial_investment_var.get()
            interest_rate = self.interest_rate_var.get()
            total_years = self.total_years_var.get()
            
            if total_years <= 0:
                messagebox.showerror("Input Error", "Total years must be greater than 0.")
                return False
                
            if interest_rate < 0:
                messagebox.showerror("Input Error", "Interest rate cannot be negative.")
                return False
            
            # Validate contribution entries
            years_to_switch = []
            contributions = []
            
            # First entry is initial contribution
            try:
                initial_contribution = float(self.contribution_entries[0][1].get())
                if initial_contribution < 0:
                    messagebox.showerror("Input Error", "Contributions cannot be negative.")
                    return False
                contributions.append(initial_contribution)
            except ValueError:
                messagebox.showerror("Input Error", "Initial contribution must be a number.")
                return False
            
            # Process other contribution changes
            for i in range(1, len(self.contribution_entries)):
                try:
                    year = int(self.contribution_entries[i][0].get())
                    if year <= 0 or year >= total_years:
                        messagebox.showerror("Input Error", f"Year must be between 1 and {total_years-1}.")
                        return False
                    years_to_switch.append(year)
                except ValueError:
                    messagebox.showerror("Input Error", "Year must be a whole number.")
                    return False
                
                try:
                    contribution = float(self.contribution_entries[i][1].get())
                    if contribution < 0:
                        messagebox.showerror("Input Error", "Contributions cannot be negative.")
                        return False
                    contributions.append(contribution)
                except ValueError:
                    messagebox.showerror("Input Error", "Contribution must be a number.")
                    return False
            
            # Check if years are in ascending order
            if len(years_to_switch) > 1:
                if sorted(years_to_switch) != years_to_switch:
                    messagebox.showerror("Input Error", "Years must be in ascending order.")
                    return False
            
            return True
        except Exception as e:
            messagebox.showerror("Input Error", f"Invalid input: {str(e)}")
            return False
        
    def calculate(self):
        if not self.validate_inputs():
            return
        
        # Get the values from the input fields
        initial_investment = self.initial_investment_var.get()
        interest_rate = self.interest_rate_var.get()
        total_years = self.total_years_var.get()
        
        # Get contribution changes
        years_to_switch = []
        contributions = []
        
        # First entry is initial contribution
        contributions.append(float(self.contribution_entries[0][1].get()))
        
        # Process other contribution changes
        for i in range(1, len(self.contribution_entries)):
            years_to_switch.append(int(self.contribution_entries[i][0].get()))
            contributions.append(float(self.contribution_entries[i][1].get()))
        
        # Calculate results
        totalNormal, yearly_totals = calculate_total_alternate_contributions_monthly(
            years_to_switch, 
            contributions, 
            initial_investment, 
            total_years, 
            interest_rate
        )
        
        # Clear previous results
        for widget in self.scrollable_frame1.winfo_children():
            widget.destroy()
        for widget in self.scrollable_frame2.winfo_children():
            widget.destroy()
        for widget in self.scrollable_frame3.winfo_children():
            widget.destroy()
        
        # Fill in the middle scrollable frame with the normal results
        # Create headers
        headers = ["Year", "Balance"]
        for i, header in enumerate(headers):
            ttk.Label(self.scrollable_frame2, text=header, font=('Helvetica', 10, 'bold')).grid(
                row=0, column=i, padx=5, pady=5, sticky="w"
            )
        
        # Fill in results
        for i, total in enumerate(yearly_totals):
            ttk.Label(self.scrollable_frame2, text=str(i)).grid(
                row=i+1, column=0, padx=5, pady=2, sticky="w"
            )
            ttk.Label(self.scrollable_frame2, text=f"${total:,.2f}").grid(
                row=i+1, column=1, padx=5, pady=2, sticky="w"
            )
        
        # Prepare to plot the results
        self.plot.clear()
        years = list(range(len(yearly_totals)))

        # Plot with a interest rate 1% Higher and fill in table
        totalPlus1, yearly_totalsPlus1 = calculate_total_alternate_contributions_monthly(
            years_to_switch, 
            contributions, 
            initial_investment, 
            total_years, 
            interest_rate + 1
        )

        self.plot.plot(years, yearly_totalsPlus1, marker='o', color='green', label=f"{interest_rate + 1}% Interest Rate")

        for i, header in enumerate(headers):
            ttk.Label(self.scrollable_frame3, text=header, font=('Helvetica', 10, 'bold')).grid(
                row=0, column=i, padx=5, pady=5, sticky="w"
            )
        
        # Fill in results
        for i, total in enumerate(yearly_totalsPlus1):
            ttk.Label(self.scrollable_frame3, text=str(i)).grid(
                row=i+1, column=0, padx=5, pady=2, sticky="w"
            )
            ttk.Label(self.scrollable_frame3, text=f"${total:,.2f}").grid(
                row=i+1, column=1, padx=5, pady=2, sticky="w"
            )

        # Update the plot for the real intest rate
        self.plot.plot(years, yearly_totals, marker='o', color='orange', label=f"{interest_rate}% Interest Rate")

        # Plot with a interest rate 1% Lower and fill in table
        totalMinus1, yearly_totalsMinus1 = calculate_total_alternate_contributions_monthly(
            years_to_switch, 
            contributions, 
            initial_investment, 
            total_years, 
            interest_rate - 1
        )

        self.plot.plot(years, yearly_totalsMinus1, marker='o', color='purple', label=f"{interest_rate - 1}% Interest Rate")

        for i, header in enumerate(headers):
            ttk.Label(self.scrollable_frame1, text=header, font=('Helvetica', 10, 'bold')).grid(
                row=0, column=i, padx=5, pady=5, sticky="w"
            )
        
        # Fill in results
        for i, total in enumerate(yearly_totalsMinus1):
            ttk.Label(self.scrollable_frame1, text=str(i)).grid(
                row=i+1, column=0, padx=5, pady=2, sticky="w"
            )
            ttk.Label(self.scrollable_frame1, text=f"${total:,.2f}").grid(
                row=i+1, column=1, padx=5, pady=2, sticky="w"
            )

        # Plot the amounts contributed at each year
        total_contribution = initial_investment
        contributions_per_year = [initial_investment]  # Start with initial investment

        # Track which contribution rate applies to each year
        current_contribution_index = 0
        current_monthly_contribution = contributions[0]

        # For each year, calculate the total contribution
        for year in range(1, total_years + 1):
            # Check if we need to switch to a new contribution rate
            if current_contribution_index < len(years_to_switch) and year == years_to_switch[current_contribution_index]:
                current_contribution_index += 1
                current_monthly_contribution = contributions[current_contribution_index]
            
            # Add this year's contribution to the running total
            yearly_contribution = current_monthly_contribution * 12
            total_contribution += yearly_contribution
            contributions_per_year.append(total_contribution)

        # Plot the contributions
        self.plot.plot(years, contributions_per_year, marker='o', color='blue', label="Contributions")

        # Display the labels using the legend
        self.plot.legend()
        
        # Add vertical lines at contribution change years
        for year in years_to_switch:
            self.plot.axvline(x=year, color='r', linestyle='--', alpha=0.5)
        
        self.plot.set_xlabel('Years')
        self.plot.set_ylabel('Balance ($)')
        self.plot.set_title('Investment Growth Over Time')
        self.plot.grid(True)
        
        # Format y-axis as currency
        self.plot.get_yaxis().set_major_formatter(
            plt.FuncFormatter(lambda x, loc: f"${x:,.0f}")
        )
        
        self.canvas.draw()
        
        # Switch to results tab
        self.notebook.select(1)
        
        # Display summary information
        messagebox.showinfo("Calculation Complete", 
                           f"Final balance after {total_years} years: ${totalNormal:,.2f}\n"
                           f"Total invested (Including Initial Investment): ${contributions_per_year[-1]:,.2f}\n"
                           f"Interest earned: ${totalNormal - (contributions_per_year[-1]):,.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InvestmentCalculatorApp(root)
    root.mainloop()