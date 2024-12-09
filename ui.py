import tkinter as tk
# from tkinter import ttk  # Import ttk for Combobox
from invoice_utils import create_invoice, add_description_entry
from datetime import datetime, timedelta


def setup_ui(root):
    # Create UI elements for client and invoice details
    # Add an entry for the client's email address
    tk.Label(root, text="Client Email (optional):").grid(row=0, column=0)
    entry_client_email = tk.Entry(root)
    entry_client_email.grid(row=0, column=1)

    tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=1, column=0)
    entry_date = tk.Entry(root)
    entry_date.grid(row=1, column=1)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Set current date as default

    tk.Label(root, text="Buyer Name").grid(row=2, column=0)
    entry_buyer_name = tk.Entry(root)
    entry_buyer_name.grid(row=2, column=1)

    tk.Label(root, text="Client Address").grid(row=3, column=0)
    entry_client_address = tk.Entry(root)
    entry_client_address.grid(row=3, column=1)

    tk.Label(root, text="Registration Code").grid(row=4, column=0)
    entry_reg_code = tk.Entry(root)
    entry_reg_code.grid(row=4, column=1)

    # Set due date to be 14 days after the invoice date
    tk.Label(root, text="Due Date (YYYY-MM-DD)").grid(row=5, column=0)
    due_date = datetime.now() + timedelta(days=14)
    entry_due_date = tk.Entry(root)
    entry_due_date.grid(row=5, column=1)
    entry_due_date.insert(0, due_date.strftime("%Y-%m-%d"))  # Prefill due date

    # Add a Checkbox for the "Paid" status in UI code
    is_paid_var = tk.BooleanVar()  # Create a BooleanVar to hold the state of the checkbox

    def update_due_date():
        if is_paid_var.get():  # If "Paid" checkbox is ticked
            entry_due_date.delete(0, tk.END)  # Clear the existing due date
            entry_due_date.insert(0, entry_date.get())  # Set due date to be the same as the invoice date
        else:
            due_date = datetime.now() + timedelta(days=14)  # Reset to 14 days after invoice date
            entry_due_date.delete(0, tk.END)
            entry_due_date.insert(0, due_date.strftime("%Y-%m-%d"))  # Refill with calculated due date

    paid_checkbox = tk.Checkbutton(root, text="Mark as Paid", variable=is_paid_var, command=update_due_date)
    paid_checkbox.grid(row=6, column=1)

    # Create labels for description, quantity, price, and total
    tk.Label(root, text="Teenus/kaup").grid(row=7, column=0)
    tk.Label(root, text="Ühiku hind").grid(row=7, column=1)
    tk.Label(root, text="Kogus/h").grid(row=7, column=2)
    tk.Label(root, text="Discount (%)").grid(row=7, column=3)  # New discount label
    tk.Label(root, text="Summa").grid(row=7, column=4)

    """   
    # List of available descriptions
    available_descriptions = ["LapaDuu komplekt", "Shipping Omniva", "Shipping Smartpost", "Shipping", "Other"]
    """

    # Create initial entries for description fields
    description_entries = []
    qty_entries = []
    price_entries = []
    discount_entries = []
    total_entries = []


    # Call the function to add initial description fields
    add_description_entry(root, description_entries, qty_entries, price_entries, discount_entries, total_entries)

    # Button to add more description fields
    btn_add_description = tk.Button(root, text="Add More Description",
                                    command=lambda: add_description_entry(root, description_entries, qty_entries,
                                                                          price_entries, discount_entries,
                                                                          total_entries))

    btn_add_description.grid(row=19, columnspan=2)

    # Button to generate the invoice
    btn_create_invoice = tk.Button(root, text="Create Invoice",
                                   command=lambda: create_invoice(entry_date, entry_buyer_name, entry_client_address,
                                                                  entry_reg_code, entry_due_date,
                                                                  description_entries, qty_entries, price_entries,
                                                                  discount_entries, total_entries,
                                                                  is_paid_var.get(),
                                                                  entry_client_email, root))

    btn_create_invoice.grid(row=20, columnspan=2)
