import customtkinter as ctk
from tkinter import messagebox
from ui import create_welcome_frame, create_input_frame, create_products_frame, add_product_frame, create_email_notification_page, remove_product

def add_product():
    product_name = entry_product_name.get()
    try:
        target_price = float(entry_target_price.get())
    except ValueError:
        messagebox.showerror("Eroare", "Te rog introdu o valoare numerică pentru prețul țintă.")
        return
    
    if not product_name:
        messagebox.showerror("Eroare", "Te rog introdu un nume de produs.")
        return

    frame_product = add_product_frame(frame_products, product_name, target_price, listbox_products)
    products_frames.append(frame_product)

    update_remove_button_visibility()

def remove_product_wrapper():
    selected_index = listbox_products.curselection()
    if selected_index:
        index = selected_index[0]
        listbox_products.delete(index)
        products_frames[index].destroy()
        del products_frames[index]

        update_remove_button_visibility()

def update_remove_button_visibility():
    if listbox_products.size() > 0:
        button_remove_product.pack(pady=10)
    else:
        button_remove_product.pack_forget()

def show_main_screen():
    frame_welcome.pack_forget()
    frame_input.pack(padx=10, pady=10, fill="x")
    frame_products.pack(padx=10, pady=10, fill="both", expand=True)
    update_remove_button_visibility()

def show_email_notification_page():
    frame_welcome.pack_forget()
    global frame_email_notification, entry_email
    frame_email_notification, entry_email = create_email_notification_page(root, show_main_screen)
    frame_email_notification.pack(padx=10, pady=10, fill="both", expand=True)

root = ctk.CTk()
root.title("Monitor de prețuri eMAG")
root.geometry("600x400")

frame_welcome = create_welcome_frame(root, show_main_screen, show_email_notification_page)
frame_input, entry_product_name, entry_target_price = create_input_frame(root, add_product)
frame_products, listbox_products, products_frames = create_products_frame(root, remove_product_wrapper)

button_remove_product = ctk.CTkButton(root, text="Șterge produs", command=remove_product_wrapper, font=("Arial", 12))

root.mainloop()
