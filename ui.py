import customtkinter as ctk
from tkinter import Listbox, Scrollbar, messagebox, LEFT
import pyperclip 

def copy_link_function(frame):
    link = frame.product_link
    if link:
        pyperclip.copy(link)
        messagebox.showinfo("Link Copiat", "Link-ul a fost copiat în clipboard.")
    else:
        messagebox.showerror("Eroare", "Nu s-a găsit niciun link pentru acest produs.")

def add_product_frame(parent, product_name, target_price, headers, listbox_products, verify_command, product_link):
    frame = ctk.CTkFrame(parent)
    frame.pack(padx=10, pady=5, fill="x")

    label_product = ctk.CTkLabel(frame, text=f"{product_name} - {target_price} Lei", anchor="w")
    label_product.pack(side=LEFT, padx=10)

    button_verify = ctk.CTkButton(frame, text="Verifică", command=verify_command, font=("Arial", 10))
    button_verify.pack(side=LEFT, padx=5)

    button_copy_link = ctk.CTkButton(frame, text="Copiază link", command=lambda: copy_link_function(frame), font=("Arial", 10))
    button_copy_link.pack(side=LEFT, padx=5)

    frame.pack(fill="x")

    
    frame.product_name = product_name
    frame.target_price = target_price
    frame.email = headers
    frame.product_link = product_link

    return frame
def create_welcome_frame(root, show_main_screen_callback, show_email_notification_page_callback):
    frame_welcome = ctk.CTkFrame(root, corner_radius=10)
    frame_welcome.pack(padx=10, pady=10, fill="both", expand=True)

    frame_welcome.grid_rowconfigure(0, weight=1)
    frame_welcome.grid_columnconfigure(0, weight=1)

    text_frame = ctk.CTkFrame(frame_welcome, corner_radius=10, fg_color="light blue")
    text_frame.grid(row=0, column=0, padx=20, pady=20)

    label_welcome = ctk.CTkLabel(text_frame, text="", font=("Arial", 20, "italic"), text_color="black")
    label_welcome.pack(padx=20, pady=20)

    text = "Welcome!"

    def animate_text(index=0):
        if index < len(text):
            label_welcome.configure(text=label_welcome.cget("text") + text[index])
            frame_welcome.after(100, animate_text, index + 1)
        else:
            button_email_notification = ctk.CTkButton(frame_welcome, text="Vreau să primesc notificare prin Email", command=show_email_notification_page_callback, font=("Arial", 12))
            button_email_notification.grid(row=1, column=0, pady=10)

            button_continue_local = ctk.CTkButton(frame_welcome, text="Continuă local", command=show_main_screen_callback, font=("Arial", 12))
            button_continue_local.grid(row=2, column=0, pady=10)

    animate_text()
    return frame_welcome

def create_input_frame(root, add_product_callback, show_price_history_callback):
    frame_input = ctk.CTkFrame(root, corner_radius=10)
    
    label_product_name = ctk.CTkLabel(frame_input, text="Nume produs:", font=("Arial", 15))
    label_product_name.grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entry_product_name = ctk.CTkEntry(frame_input, width=300, font=("Arial", 12))
    entry_product_name.grid(row=0, column=1, padx=5, pady=5)

    label_target_price = ctk.CTkLabel(frame_input, text="Preț țintă (lei):", font=("Arial", 15))
    label_target_price.grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entry_target_price = ctk.CTkEntry(frame_input, width=100, font=("Arial", 12))
    entry_target_price.grid(row=1, column=1, padx=5, pady=5)

    button_add_product = ctk.CTkButton(frame_input, text="Adaugă produs", command=add_product_callback, font=("Arial", 12))
    button_add_product.grid(row=2, columnspan=2, pady=10)

    button_show_history = ctk.CTkButton(frame_input, text="Istoric Prețuri", command=show_price_history_callback, font=("Arial", 12))
    button_show_history.grid(row=3, columnspan=2, pady=10)

    return frame_input, entry_product_name, entry_target_price



def create_products_frame(root, remove_product_callback):
    frame_products = ctk.CTkFrame(root, corner_radius=10)
    
    listbox_products = Listbox(frame_products, height=10, bg="#2a2d2e", fg="white", selectbackground="#1f538d", selectforeground="white", font=("Arial", 12))
    listbox_products.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    scrollbar_products = Scrollbar(frame_products, orient="vertical", command=listbox_products.yview)
    scrollbar_products.pack(side="right", fill="y")

    listbox_products.config(yscrollcommand=scrollbar_products.set)

    return frame_products, listbox_products, []

def create_email_notification_page(root, show_main_screen_callback):
    frame_email_notification = ctk.CTkFrame(root, corner_radius=10)
    frame_email_notification.pack(padx=10, pady=10, fill="both", expand=True)

    label_email = ctk.CTkLabel(frame_email_notification, text="Introduceți adresa de email:", font=("Arial", 15))
    label_email.pack(pady=20)

    entry_email = ctk.CTkEntry(frame_email_notification, width=300)
    entry_email.pack(padx=20, pady=10)

    entry_email.bind("<Return>", lambda event: show_main_screen_callback())  # Go to main screen on pressing Enter

    return frame_email_notification, entry_email

def remove_product(listbox_products):
    selected_index = listbox_products.curselection()
    if selected_index:
        listbox_products.delete(selected_index)
    else:
        messagebox.showwarning("Alegere necesară", "Te rog selectează un produs pentru a-l șterge.")
