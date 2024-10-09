import tkinter as tk
from ui import setup_ui
from email_sender import send_invoice
from invoice_utils import create_invoice

# Create the main application window
root = tk.Tk()
root.title("Invoice Generator")
root.geometry("1200x1200")  # Set an initial window size

# Call the setup_ui function to create the UI
setup_ui(root)


# Define a function to send the invoice email
def on_invoice_created(entry_date, entry_buyer_name, entry_client_address, entry_reg_code, entry_due_date,
                       description_entries, qty_entries, price_entries, discount_entries, total_entries,
                       is_paid, entry_client_email, root):
    # Call the create_invoice function to create and save the invoice PDF
    invoice_file_path = create_invoice(entry_date, entry_buyer_name, entry_client_address, entry_reg_code,
                                       entry_due_date, description_entries, qty_entries, price_entries,
                                       discount_entries, total_entries, is_paid, entry_client_email, root)

    if invoice_file_path:
        # Pass the invoice_file_path to the send_invoice function, along with the email
        client_email = entry_client_email.get().strip()
        print(client_email)
        if client_email:  # Only send if email is provided
            send_invoice(client_email, invoice_file_path)


# Start the main loop of the application
root.mainloop()
