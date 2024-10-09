import os
import re
import json
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from tkinter import messagebox
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image
from reportlab.lib.colors import blue  # Import the color blue
from email_sender import send_invoice
import sys


def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# Function to initialize the invoice number JSON file
def initialize_invoice_number():
    if not os.path.exists("invoice_number.json"):
        # Create the file and set the initial invoice number to 1
        with open("invoice_number.json", "w") as f:
            json.dump({"invoice_number": 1}, f)  # Start at 1


# Function to load the last invoice number
def load_invoice_number():
    if os.path.exists("invoice_number.json"):
        with open("invoice_number.json", "r") as f:
            return json.load(f).get("invoice_number", 0)
    return 0


# Function to save the last invoice number
def save_invoice_number(invoice_number):
    with open("invoice_number.json", "w") as f:
        json.dump({"invoice_number": invoice_number}, f)


# Function to reset the form after an invoice is created
def reset_form(root, description_entries, qty_entries, price_entries, discount_entries, total_entries,
               entry_buyer_name, entry_client_address, entry_reg_code, add_description_func, entry_client_email):
    entry_buyer_name.delete(0, tk.END)
    entry_client_address.delete(0, tk.END)
    entry_reg_code.delete(0, tk.END)
    entry_client_email.delete(0, tk.END)

    # Clear description, quantity, price, discount, and total entries
    for entry in description_entries + qty_entries + price_entries + discount_entries + total_entries:
        if isinstance(entry, tk.Entry):
            entry.delete(0, tk.END)  # Clear Entry widgets
        elif isinstance(entry, tk.Text):
            entry.delete("1.0", tk.END)  # Clear Text widgets

    # Hide and clear the grid for the entries
    for widget in description_entries + qty_entries + price_entries + discount_entries + total_entries:
        widget.grid_forget()
    description_entries.clear()
    qty_entries.clear()
    price_entries.clear()
    discount_entries.clear()  # Clear discount entries
    total_entries.clear()

    # Add a new description entry
    add_description_func(root, description_entries, qty_entries, price_entries, discount_entries, total_entries)


# Main application logic
if __name__ == "__main__":
    # Initialize the invoice number file if it doesn't exist
    initialize_invoice_number()

    # Load the current invoice number
    current_invoice_number = load_invoice_number()


# Function to add a footer with a separating line
def add_footer(canvas, _doc):
    canvas.saveState()
    width, height = letter
    line_position = inch  # Set line position from the bottom

    # Draw a solid line above the footer
    canvas.setLineWidth(1)
    canvas.line(0.75 * inch, line_position + 0.2 * inch, width - 0.75 * inch, line_position + 0.2 * inch)

    # Set font for the footer
    canvas.setFont("Helvetica", 9)

    # Footer contents
    footer_part1 = [
        ("LapaDuu OÜ", 0.75 * inch),  # Name
        ("Reg.nr 14842122", 3.2 * inch),  # Registration number
        ("Swedbank: EE122200221072678443", 5.5 * inch)  # Bank info
    ]

    footer_part2 = [
        ("Luha 16-79, Tallinn", 0.75 * inch),  # Address
        ("Tel: +372 53702287", 3.2 * inch),  # Phone number
    ]

    footer_part3 = [
        ("Harjumaa, 10129", 0.75 * inch),  # County and postal code
        ("email: lapaduu@lapaduu.ee", 3.2 * inch)  # Email
    ]

    # Draw footer contents
    for text, x_position in footer_part1:
        canvas.drawString(x_position, line_position - 10, text)

    for text, x_position in footer_part2:
        canvas.drawString(x_position, line_position - 25, text)

    for text, x_position in footer_part3:
        canvas.drawString(x_position, line_position - 40, text)

    # Set color to blue for the email link
    canvas.setFillColor(blue)

    # Draw the email text
    email_x = 3.2 * inch  # Same position as the email text
    email_y = line_position - 40  # Corresponding y position
    canvas.drawString(email_x, email_y, "email: lapaduu@lapaduu.ee")

    # Draw an underline for the email
    email_text_width = canvas.stringWidth("email: lapaduu@lapaduu.ee", "Helvetica", 9)
    canvas.setLineWidth(0.5)  # Set line width for underline
    canvas.line(email_x, email_y - 2, email_x + email_text_width, email_y - 2)  # Draw the underline

    # Create a clickable email link
    canvas.linkURL("mailto:lapaduu@lapaduu.ee", (email_x, email_y - 5, email_x + 100, email_y + 5), relative=1)

    # Restore the canvas state
    canvas.restoreState()


# Function to create the invoice PDF
def create_invoice(entry_date, entry_buyer_name, entry_client_address, entry_reg_code, entry_due_date,
                   description_entries, qty_entries, price_entries, discount_entries, total_entries,
                   is_paid, entry_client_email, root):
    date = entry_date.get().strip()
    buyer_name = entry_buyer_name.get().strip()
    client_address = entry_client_address.get().strip()
    reg_code = entry_reg_code.get().strip()
    due_date = entry_due_date.get().strip()
    # client_email = entry_client_email.get().strip()  # Get client email
    descriptions = [desc.get("1.0", tk.END).strip() for desc in description_entries]  # Get text from Text widget
    qtys = [qty.get() for qty in qty_entries]
    prices = [price.get() for price in price_entries]
    discounts = [discount.get() for discount in discount_entries]  # Extract discount
    totals = [total.get() for total in total_entries]

    # Validate input fields
    if not (date and buyer_name and client_address and reg_code and due_date):
        messagebox.showerror("Error", "Buyer name, Client Address and Registration code are mandatory"
                                      " Required fields must be filled!")
        return

    # Validate email if provided
    client_email = entry_client_email.get().strip()
    if client_email and not is_valid_email(client_email):
        messagebox.showerror("Error", "Invalid email format.")
        return

    # Create folder path on desktop
    today = datetime.now().strftime("%Y-%m-%d")
    folder_path = os.path.join(os.path.expanduser("~/Desktop"), today)
    os.makedirs(folder_path, exist_ok=True)

    # Increment invoice number
    invoice_number = load_invoice_number() + 1
    save_invoice_number(invoice_number)

    pdf_filename = os.path.join(folder_path, f"Invoice_{invoice_number}.pdf")
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    elements = []

    # Load and add logo
    logo_path = resource_path("logo.png")  # Use the resource_path function
    logo = Image(logo_path)  # Now this will work correctly
    logo_width = 100  # Adjust the width as needed
    logo_height = 85  # Adjust the height as needed
    logo.drawHeight = logo_height
    logo.drawWidth = logo_width

    # Create a table for logo and title
    title_table = Table([[logo, Paragraph("LapaDuu OÜ", getSampleStyleSheet()['Title'])]], colWidths=[logo_width, None])
    title_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (0, 0), (1, 0), 'LEFT')
    ]))
    elements.append(title_table)

    # Add "PAID" label if invoice is marked as paid
    if is_paid:
        paid_label_style = getSampleStyleSheet()['Title']
        paid_label_style.textColor = 'green'  # Set text color to green
        paid_label = Paragraph("<b>MAKSTUD</b>", paid_label_style)
        elements.append(paid_label)

    # Left and right aligned table for client and invoice details
    left_text = f"Klient: {buyer_name}\n Address: {client_address}\n Reg kood: {reg_code}"
    left_lines = left_text.split('\n')

    left_aligned_table = Table([[Paragraph(line, getSampleStyleSheet()['Normal'])] for line in left_lines],
                               colWidths=[250])  # Adjust column width if necessary

    left_aligned_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-2, -2), 'LEFT'),
        ('VALIGN', (0, 0), (0, -1), 'TOP')
    ]))

    # Right align invoice details
    right_text = f"Arve nr: {invoice_number}\nArve kuupäev: {date}\nMakse tähtaeg: {due_date}\nViivis: 0,15% päevas"
    right_lines = right_text.split('\n')

    # Create a separate table for right-aligned invoice details
    right_aligned_table = Table([[Paragraph(line, getSampleStyleSheet()['Normal'])] for line in right_lines],
                                colWidths=[250])  # Adjust column width if necessary
    right_aligned_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (0, -1), 'TOP')
    ]))

    client_details = Table([[left_aligned_table, right_aligned_table]], colWidths=[250, 250])
    elements.append(client_details)

    # Add some space
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    # Add the services/products table
    data = [['Teenus/kaup', 'Ühiku hind', 'Kogus/h', 'Discount (%)', 'Summa']]
    for i in range(len(descriptions)):
        if descriptions[i]:  # Check if the description is present
            # Prepare values
            qty_value = qtys[i] if qtys[i] else ' '  # Default to ' ' space, if empty
            formatted_price = f"{float(prices[i]):.2f}" if prices[i] else ' '  # Default to ' ' space, if empty
            formatted_total = f"{float(totals[i]):.2f}" if totals[i] else ' '  # Default to ' ' space, if empty
            data.append([
                Paragraph(descriptions[i], getSampleStyleSheet()['Normal']),  # Multi-line description
                formatted_price,  # Use formatted price
                qty_value,  # Show qty or default to ' '
                discounts[i] if discounts[i] else ' ',  # Default to ' ' if empty
                formatted_total  # Use formatted total
            ])

    table = Table(data, colWidths=[200, 100, 100, 100, 100])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, 'black'),
        ('BACKGROUND', (0, 0), (-1, 0), 'grey'),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align desc text to the top
        ('VALIGN', (1, 1), (-1, -1), 'MIDDLE')  # Center align for other columns

    ]))
    elements.append(table)
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    right_align_style = ParagraphStyle(name='RightAlign', parent=getSampleStyleSheet()['Normal'], alignment=TA_RIGHT)
    total_amount = sum(float(entry) for entry in totals if entry)
    elements.append(Paragraph("Käibemaks: Ei ole KM kohuslane", right_align_style))
    elements.append(
        Paragraph(f"<b>Arve summa kokku (EUR): {total_amount:.2f}</b>", right_align_style))  # Make total bold

    # Add some space
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))
    elements.append(Paragraph("<br/><br/>", getSampleStyleSheet()['Normal']))

    left_align_style = ParagraphStyle(name='LeftAlign', parent=getSampleStyleSheet()['Normal'], alignment=TA_LEFT)
    elements.append(Paragraph("Palume arve tasumisel märkida selgitusse arve number.", left_align_style))
    elements.append(Paragraph("LapaDuu OÜ ei ole käibemaksukohuslane.", left_align_style))

    doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
    # messagebox.showinfo("Success", f"Invoice created successfully: {pdf_filename}")

    # Call reset_form with all the necessary arguments
    reset_form(root, description_entries, qty_entries, price_entries, discount_entries,
               total_entries, entry_buyer_name, entry_client_address, entry_reg_code,
               add_description_entry, entry_client_email)

    # If client email is provided, send the invoice via email
    client_email = entry_client_email.get()
    print(client_email)
    if client_email:
        try:
            send_invoice(client_email, pdf_filename)
            messagebox.showinfo("Success", f"Invoice created and sent successfully: {pdf_filename}")
        except Exception as e:
            print(f"Error sending email: {e}")  # Capture and print any errors
            messagebox.showerror("Error", "Failed to send email.")
    else:
        messagebox.showinfo("Success", f"Invoice created successfully: {pdf_filename}")

    return pdf_filename


def calculate_total(qty_entry, price_entry, discount_entry, total_entry):
    try:
        qty = float(qty_entry.get()) if qty_entry.get() else 0
        price = float(price_entry.get()) if price_entry.get() else 0
        discount = float(discount_entry.get()) if discount_entry.get() else 0

        # Calculate total considering discount
        total = qty * price * (1 - discount / 100)

        # Update total entry
        total_entry.delete(0, tk.END)
        total_entry.insert(0, f"{total:.2f}")
    except ValueError:
        # Handle any invalid input (non-numeric values)
        total_entry.delete(0, tk.END)
        total_entry.insert(0, "0.00")


def add_description_entry(root, description_entries, qty_entries, price_entries, discount_entries, total_entries):
    row = len(description_entries) + 8

    # Description entry (using a Text widget)
    desc_entry = tk.Text(root, height=2, width=30)  # Set height and width as needed
    desc_entry.grid(row=row, column=0)
    description_entries.append(desc_entry)

    # Quantity entry
    qty_entry = tk.Entry(root)
    qty_entry.grid(row=row, column=1)
    qty_entries.append(qty_entry)

    # Price entry
    price_entry = tk.Entry(root)
    price_entry.grid(row=row, column=2)
    price_entries.append(price_entry)

    # Discount entry
    discount_entry = tk.Entry(root)
    discount_entry.grid(row=row, column=3)
    discount_entries.append(discount_entry)  # New discount entry added

    # Total entry
    total_entry = tk.Entry(root)
    total_entry.grid(row=row, column=4)
    total_entries.append(total_entry)

    # Bind calculation function to quantity, price, and discount
    qty_entry.bind("<KeyRelease>", lambda event: calculate_total(qty_entry, price_entry, discount_entry, total_entry))
    price_entry.bind("<KeyRelease>", lambda event: calculate_total(qty_entry, price_entry, discount_entry, total_entry))
    discount_entry.bind("<KeyRelease>",
                        lambda event: calculate_total(qty_entry, price_entry, discount_entry, total_entry))
