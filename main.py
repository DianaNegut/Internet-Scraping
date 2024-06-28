import customtkinter as ctk
from tkinter import messagebox, Toplevel, Text, Scrollbar, RIGHT, Y
from scraper_emag import get_price_emag, get_search_url
from scraper_altex import AltexScraper
from ui import create_input_frame, create_products_frame, add_product_frame, create_welcome_frame, create_email_notification_page, remove_product
import smtplib
from email.mime.text import MIMEText
import schedule
import threading
import time
import pyperclip 
import json
import os

sent_emails = {} 

price_history_file = "price_history.json"

def save_price_history(product_name, price, source):
    try:
        # deschid fisierul cu istoricul de preturi
        if os.path.exists(price_history_file):
            with open(price_history_file, "r") as f:
                price_history = json.load(f)
        else:
            price_history = {}
    except FileNotFoundError:
        price_history = {}
    # trebuie sa caut produsul meu in lista de produse care exista deja in fisier
    if product_name not in price_history:
        price_history[product_name] = []

    price_history[product_name].append({"price": price, "source": source, "timestamp": time.time()})

    # aici salvez
    with open(price_history_file, "w") as f:
        json.dump(price_history, f)

def load_price_history():
    try:
        with open(price_history_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# am nevoie sa formatez afisarea sa nu fie ca un json
def format_price_history(history):
    formatted_history = ""
    for product, entries in history.items():
        formatted_history += f"Produs: {product}\n"
        for entry in entries:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry['timestamp']))
            formatted_history += f"  • Preț: {entry['price']} lei, Sursa: {entry['source']}, Data: {timestamp}\n"
        formatted_history += "\n"
    return formatted_history

def show_price_history():
    # citesc fisierul
    history = load_price_history()
    if history:
        # formatez
        formatted_history = format_price_history(history)
        
        # copil fereastra principala
        history_window = Toplevel(root)
        history_window.title("Istoricul Prețurilor")
        history_window.geometry("600x500")
        
        text_widget = Text(history_window, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        text_widget.pack(side="left", fill="both", expand=True)
        
        scrollbar = Scrollbar(history_window, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        text_widget.config(yscrollcommand=scrollbar.set)
        

        lines = formatted_history.split("\n")
        for line in lines:
            if line.startswith("Produs:"):
                text_widget.insert("end", line + "\n", "product")
            elif line.startswith("  • Preț:"):
                text_widget.insert("end", line + "\n", "entry")
            else:
                text_widget.insert("end", line + "\n")

    
        text_widget.tag_configure("product", font=("Arial", 12, "bold"), foreground="#004d99", spacing3=10)
        text_widget.tag_configure("entry", font=("Arial", 12), foreground="#006600", spacing3=5)

        text_widget.configure(state="disabled")

        # Adaugă un buton pentru a arăta cel mai mic preț
        button_show_lowest_prices = ctk.CTkButton(history_window, text="Arată cel mai mic preț", command=show_lowest_prices, font=("Arial", 12))
        button_show_lowest_prices.pack(pady=10)
    else:
        messagebox.showinfo("Istoricul Prețurilor", "Nu există istoric de prețuri.")

def show_lowest_prices():
    history = load_price_history()
    if history:
        lowest_prices = ""
        for product, entries in history.items():
            # pretul minim
            min_price_entry = min(entries, key=lambda x: x['price'])
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(min_price_entry['timestamp']))
            lowest_prices += f"Produs: {product}\n"
            lowest_prices += f"  • Cel mai mic preț: {min_price_entry['price']} lei, Sursa: {min_price_entry['source']}, Data: {timestamp}\n\n"

       
        lowest_window = Toplevel(root)
        lowest_window.title("Cele mai mici prețuri")
        lowest_window.geometry("600x400")

        
        text_widget = Text(lowest_window, wrap="word", font=("Arial", 12), bg="#f0f0f0", fg="#333333", padx=10, pady=10)
        text_widget.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(lowest_window, command=text_widget.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_widget.config(yscrollcommand=scrollbar.set)

       
        lines = lowest_prices.split("\n")
        for line in lines:
            if line.startswith("Produs:"):
                text_widget.insert("end", line + "\n", "product")
            elif line.startswith("  • Cel mai mic preț:"):
                text_widget.insert("end", line + "\n", "entry")
            else:
                text_widget.insert("end", line + "\n")

       
        text_widget.tag_configure("product", font=("Arial", 12, "bold"), foreground="#004d99", spacing3=10)
        text_widget.tag_configure("entry", font=("Arial", 12), foreground="#ff6600", spacing3=5)

        text_widget.configure(state="disabled")
    else:
        messagebox.showinfo("Cele mai mici prețuri", "Nu există istoric de prețuri.")

def send_email(email, subject, body):
    sender_email = "preturi.alerta@gmail.com"
    sender_password = "twcj qmgg ourc ncdh"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        print(f"Email trimis cu succes către {email}!")
    except Exception as e:
        print(f"Eroare la trimiterea emailului: {e}")

def check_price(product_name, target_price, headers, listbox, email=None):
    # eMAG
    emag_search_url = get_search_url(product_name)
    emag_result = get_price_emag(emag_search_url, headers)

    # Altex
    altex_scraper = AltexScraper()
    altex_result = altex_scraper.get_price_and_name(product_name)

    prices = {}
    names = {}
    links = {}
    if emag_result is not None:
        prices['eMAG'] = emag_result['price']
        names['eMAG'] = emag_result['name']
        links['eMAG'] = emag_result['link']
    if altex_result is not None:
        prices['Altex'] = altex_result['price']
        names['Altex'] = altex_result['name']
        links['Altex'] = altex_result['link']

    if prices:
        min_price_source = min(prices, key=prices.get)
        min_price = prices[min_price_source]
        product_name = names[min_price_source]
        product_link = links[min_price_source]

        listbox.insert("end", f"{product_name} - Preț curent: {min_price} lei ({min_price_source}) - Link: {product_link}")

        # salvez preturile
        save_price_history(product_name, min_price, min_price_source)

        if min_price < target_price:
            if email and (email, product_name) not in sent_emails:
                send_email(email, "Alertă preț", f"Prețul pentru {product_name} a scăzut sub {target_price} lei! Preț curent: {min_price} lei ({min_price_source}). Link: {product_link}")
                sent_emails[(email, product_name)] = True
            messagebox.showinfo("Alertă!", f"Prețul pentru {product_name} a scăzut sub {target_price} lei! Preț curent: {min_price} lei ({min_price_source}). Link: {product_link}")
    else:
        messagebox.showerror("Eroare", f"Nu s-a putut obține prețul pentru {product_name} de la niciun retailer.")
    return product_link

def add_product():
    global headers
    product_name = entry_product_name.get()
    try:
        target_price = float(entry_target_price.get())
    except ValueError:
        messagebox.showerror("Eroare", "Te rog introdu o valoare numerică pentru prețul țintă.")
        return
    
    if not product_name:
        messagebox.showerror("Eroare", "Te rog introdu un nume de produs.")
        return

    email = entry_email.get() if 'entry_email' in globals() and entry_email.get() else None
    
    product_link = check_price(product_name, target_price, headers, listbox_products, email)
    
    
    frame_product = add_product_frame(frame_products, product_name, target_price, headers, listbox_products, lambda: check_price(product_name, target_price, headers, listbox_products, email), product_link)
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
        button_sort_name.pack(pady=10)
        button_sort_price.pack(pady=10)
    else:
        button_remove_product.pack_forget()
        button_sort_name.pack_forget()
        button_sort_price.pack_forget()

def show_main_screen():
    frame_welcome.pack_forget()
    if 'frame_email_notification' in globals():
        frame_email_notification.pack_forget()
    frame_input.pack(padx=10, pady=10, fill="x")
    frame_products.pack(padx=10, pady=10, fill="both", expand=True)

    update_remove_button_visibility()

def show_email_notification_page():
    frame_welcome.pack_forget()
    global frame_email_notification, entry_email
    frame_email_notification, entry_email = create_email_notification_page(root, show_main_screen)
    frame_email_notification.pack(padx=10, pady=10, fill="both", expand=True)

def sort_products_by_name():
    # extrag toate produsele 
    products = listbox_products.get(0, "end")
    sorted_products = sorted(products, key=lambda x: x.split(" - ")[0])
    # sterg produsele care erau deja
    listbox_products.delete(0, "end")
    # repopulez lista de produse
    for product in sorted_products:
        listbox_products.insert("end", product)

def sort_products_by_price():
    products = listbox_products.get(0, "end")

    def extract_price(product):
        try:
            price_section = product.split(" - ")[2].split()[0]
            return float(price_section.replace('lei', '').replace(',', '').strip())
        except (IndexError, ValueError):
            return float('inf')  # return un pret foarte mare pentru elementele care nu se potrivesc

    sorted_products = sorted(products, key=extract_price)
    listbox_products.delete(0, "end")
    for product in sorted_products:
        listbox_products.insert("end", product)

def schedule_price_check():
    for frame in products_frames:
        product_name = frame['product_name']
        target_price = frame['target_price']
        email = frame['email']
        check_price(product_name, target_price, headers, listbox_products, email)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def copy_link_function(listbox):
    selected_index = listbox.curselection()
    if selected_index:
        index = selected_index[0]
        item_text = listbox.get(index)
        link_start = item_text.find("Link: ") + len("Link: ")
        link = item_text[link_start:]
        pyperclip.copy(link)
        messagebox.showinfo("Link Copiat", "Link-ul a fost copiat în clipboard.")

root = ctk.CTk()
root.title("Monitor de prețuri eMAG și Altex")
root.geometry("600x400")

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

frame_welcome = create_welcome_frame(root, show_main_screen, show_email_notification_page)
frame_input, entry_product_name, entry_target_price = create_input_frame(root, add_product, show_price_history)
frame_products, listbox_products, products_frames = create_products_frame(root, remove_product_wrapper)

button_remove_product = ctk.CTkButton(root, text="Șterge produs", command=remove_product_wrapper, font=("Arial", 12))
button_sort_name = ctk.CTkButton(root, text="Sortează după Nume", command=sort_products_by_name, font=("Arial", 12))
button_sort_price = ctk.CTkButton(root, text="Sortează după Preț", command=sort_products_by_price, font=("Arial", 12))

# Butoanele de sortare și de ștergere trebuie să fie gestionate în funcțiile de afișare
def manage_buttons_visibility():
    if listbox_products.size() > 0:
        button_sort_name.pack(pady=10)
        button_sort_price.pack(pady=10)
        button_remove_product.pack(pady=10)
    else:
        button_sort_name.pack_forget()
        button_sort_price.pack_forget()
        button_remove_product.pack_forget()

manage_buttons_visibility()

# se reactualizeaza la fiecare ora
schedule.every().hour.do(schedule_price_check)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

root.mainloop()
