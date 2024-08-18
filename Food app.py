#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox

# Sample user data (username: password)
user_data = {"user": "password"}

foodMenu = {
    "Starters": {
        "Baby Corn Manchurian": 160,
        "Gobi Manchurian": 150,
        "Paneer 65": 180,
        "Paneer Manchurian": 180,
        "Paneer Tikka": 200,
        "Spring Rolls": 150,
        "Soups": 100,
        "Chilli Paneer": 220
    },
    "Indian Breads": {
        "Naan": 40,
        "Butter Naan": 60,
        "Kulcha": 40,
        "Butter Kulcha": 60,
        "Roti": 40,
        "Garlic Naan": 80,
        "stuffed Naan": 80,
        "Tandoori Roti": 70
    },
    "Curries": {
        "Aloo Gobi": 180,
        "Dal Makhani": 180,
        "Malai Kofta": 220,
        "Palak Paneer": 200,
        "Paneer Butter Masala": 230,
        "Vegetable Curry": 200,
        "Kaju Masala": 220,
        "Kadai Paneer": 210
    },
    "Rice": {
        "Ghee Rice": 140,
        "Jeera Rice": 140,
        "Peas Pulav": 160,
        "Paneer Biryani": 180,
        "Veg Biryani": 200,
        "Curd Rice": 120,
        "Fried Rice": 160,
        "Schezwan Fried Rice": 220
    },
    "Desserts": {
        "Gulab Jamun": 85,
        "Jalebi": 60,
        "Kheer": 60,
        "Rasgulla": 80,
        "Rasmalai": 80,
        "Ice Cream": 80,
        "Fruit Salad": 100,
        "Fruit Salad with Icecream": 120
    }
}

def ask_for_location(root):
    dialog = LocationDialog(root)
    root.wait_window(dialog.top)
    return dialog.location

def display_payment_options(location):
    if not location:
        messagebox.showerror("Error", "Please enter your location first.")
        return

    payment_window = tk.Toplevel()
    payment_window.title("Payment Options")

    payment_frame = tk.Frame(payment_window)
    payment_frame.pack(padx=10, pady=10)

    tk.Label(payment_frame, text=f"Location: {location}", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, padx=5, pady=(10, 5))

    tk.Label(payment_frame, text="Select Payment Method:", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, padx=5, pady=(10, 5))

    payment_option = tk.StringVar()
    payment_option.set("Online Payment")  # Default payment method

    payment_methods = ["Online Payment", "Cash on Delivery"]

    for i, method in enumerate(payment_methods):
        tk.Radiobutton(payment_frame, text=method, variable=payment_option, value=method).grid(row=i + 2, column=0, columnspan=2, padx=5, pady=5)

    confirm_payment_button = tk.Button(payment_frame, text="Confirm Payment", command=lambda: confirm_payment(payment_option.get(), location))
    confirm_payment_button.grid(row=len(payment_methods) + 2, column=0, pady=10, padx=(0, 5))

    cancel_button = tk.Button(payment_frame, text="Cancel", command=payment_window.destroy)
    cancel_button.grid(row=len(payment_methods) + 2, column=1, pady=10, padx=(5, 0))

def confirm_payment(payment_method, location):
    global selected_items  # Add global declaration
    if not payment_method:
        messagebox.showerror("Error", "Please select a payment method.")
        return

    food_price = sum(qty[0] * qty[1] for qty in selected_items.values())
    total_with_delivery = food_price + 30  # Adding delivery charges

    bill_text = f"Location: {location}\n\nSelected Items:\n" + "\n".join([f"{item}   x{qty[0]}   -   ₹{qty[0] * qty[1]}" for item, qty in selected_items.items()]) + f"\n\nFood Total: ₹{food_price}\nDelivery Charges: ₹30\nTotal Amount: ₹{total_with_delivery}\n\nPayment Method: {payment_method}"

    messagebox.showinfo("Payment Confirmation", bill_text)

    # Show the full bill
    view_full_bill(bill_text)

def view_full_bill(bill_text):
    full_bill_window = tk.Toplevel()
    full_bill_window.title("Full Bill")

    # Split the bill_text into lines
    lines = bill_text.split('\n')
    
    # Display each line in the full bill window
    for line in lines:
        tk.Label(full_bill_window, text=line, font=("Arial", 12)).pack(padx=10, pady=5)

    # Close button
    close_button = tk.Button(full_bill_window, text="Close", command=lambda: [full_bill_window.destroy(), display_rating_window()])
    close_button.pack(pady=10)

class LocationDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Location")
        self.top.geometry("300x100")
        self.location = None

        self.label = tk.Label(self.top, text="Please enter your location:")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.top)
        self.entry.pack(pady=5)

        self.confirm_button = tk.Button(self.top, text="Confirm", command=self.confirm_location)
        self.confirm_button.pack(pady=5)

    def confirm_location(self):
        self.location = self.entry.get()
        if not self.location:
            messagebox.showerror("Error", "Please enter your location.")
        else:
            self.top.destroy()

def display_menu_gui():
    global selected_items  # Add global declaration
    root = tk.Tk()
    root.title("Food Menu")

    menu_header = " ########## FOOD MENU ########## "

    column_index = 0
    item_number = 1
    max_name_length = max(len(item) for items in foodMenu.values() for item in items.keys())

    selected_items = {}  # Dictionary to store selected items

    def select_item(item_name, price):
        if item_name in selected_items:
            selected_items[item_name][0] += 1
        else:
            selected_items[item_name] = [1, price]  # Quantity, Price
        update_selection_label()

    def update_selection_label():
        food_price = sum(qty[0] * qty[1] for qty in selected_items.values())
        total_with_delivery = food_price + 30  # Adding delivery charges
        selection_label.config(text="Selected Items:\n\n" + "\n".join([f"{item}   x{qty[0]}   -   ₹{qty[0] * qty[1]}" for item, qty in selected_items.items()]) +
                                             f"\n\nFood Total: ₹{food_price}\nDelivery Charges: ₹30\nTotal Amount: ₹{total_with_delivery}", fg="red")

    def reset_selection():
        if not selected_items:
            messagebox.showinfo("Reset", "No food items selected.")
        selected_items.clear()
        update_selection_label()

    def submit_order():
        if not selected_items:
            messagebox.showerror("Error", "Please select at least one food item.")
            return

        location = ask_for_location(root)  # Get user's location
        if location:
            display_payment_options(location)  # Display payment options

    for category, items in foodMenu.items():
        tk.Label(root, text=category, font=("Arial", 14, "bold"), fg="red").grid(row=1, column=column_index, padx=10, pady=(10, 5))

        row_index = 2
        for item, price in items.items():
            item_var = tk.BooleanVar()
            item_var.set(False)

            item_label = tk.Label(root, text=f"{item}\t{' ' * (20 - len(item))}", fg="blue")
            item_label.grid(row=row_index, column=column_index, sticky="w", padx=10, pady=2)

            select_button = tk.Button(root, text="Select", command=lambda i=item, p=price: select_item(i, p))
            select_button.grid(row=row_index, column=column_index + 1, sticky="w", padx=(0, 10), pady=2)

            tk.Label(root, text=f"₹ {price:<5}", fg="green").grid(row=row_index, column=column_index + 2, sticky="w", padx=(0, 10), pady=2)
            item_number += 1
            row_index += 1

        column_index += 3

    tk.Label(root, text=menu_header, font=("Arial", 12), fg="red").grid(row=0, column=0, columnspan=column_index, padx=10, pady=10)

    submit_reset_frame = tk.Frame(root)
    submit_reset_frame.grid(row=row_index + 1, column=0, columnspan=column_index, padx=10, pady=(20, 10))

    reset_button = tk.Button(submit_reset_frame, text="Reset Selection", command=reset_selection, font=("Arial", 12))
    reset_button.pack(side="left", padx=(0, 5))

    # Add a horizontal spacer
    spacer = tk.Label(submit_reset_frame, text="", font=("Arial", 12))
    spacer.pack(side="left", padx=5)

    submit_button = tk.Button(submit_reset_frame, text="Submit Order", command=submit_order, font=("Arial", 12))
    submit_button.pack(side="left", padx=(5, 0))

    selection_label = tk.Label(root, text="Selected Items:", font=("Arial", 12), fg="blue")
    selection_label.grid(row=row_index + 2, column=0, columnspan=column_index, padx=10, pady=10)

    root.mainloop()

# Rating window
def display_rating_window():
    rating_window = tk.Toplevel()
    rating_window.title("Rate Our Service")

    rating_label = tk.Label(rating_window, text="Please rate our service:", font=("Arial", 12))
    rating_label.pack(pady=10)

    rating_scale = tk.Scale(rating_window, from_=1, to=5, orient=tk.HORIZONTAL, length=200)
    rating_scale.pack(pady=10)

    submit_rating_button = tk.Button(rating_window, text="Submit Rating", command=lambda: submit_rating(rating_window, rating_scale.get()), font=("Arial", 12))
    submit_rating_button.pack(pady=10)

def submit_rating(window, rating):
    messagebox.showinfo("Rating Submitted", f"Thank you for your rating: {rating}/5")
    window.destroy()

# Login window
def authenticate():
    username = username_entry.get()
    password = password_entry.get()
    if username in user_data and user_data[username] == password:
        messagebox.showinfo("Login Successful!", f"Welcome back to Tasty Bite app, {username}!")
        root.destroy()  # Close the login window
        display_menu_gui()  # Open the menu window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

root = tk.Tk()
root.title("Login")

username_label = tk.Label(root, text="Username:", font=("Arial", 12))
username_label.grid(row=0, column=0, padx=10, pady=(20, 5))
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.grid(row=0, column=1, padx=10, pady=(20, 5))

password_label = tk.Label(root, text="Password:", font=("Arial", 12))
password_label.grid(row=1, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*", font=("Arial", 12))
password_entry.grid(row=1, column=1, padx=10, pady=5)

login_button = tk.Button(root, text="Login", command=authenticate, font=("Arial", 12))
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=(20, 10))

root.mainloop()


# In[ ]:




