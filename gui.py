import tkinter as tk
from server import START_SERVER, connect_clients, stop_server
from tkinter import messagebox
import threading

log = []
server_running = False

def RUN_GUI():  
    def on_start_stop():
        global server_running
        if not server_running:
                
            threading.Thread(target=START_SERVER, daemon=True).start()
            server_running = True
            start_btn.config(text="Stop FTP Server")
            update_clients()
        else:
            stop_server()
            server_running = False
            start_btn.config(text="Start FTP Server")
    def update_clients():
        if server_running:
            client_listbox.delete(0, tk.END)
            for client in connect_clients:
                client_listbox.insert(tk.END, client)
            root.after(1000, update_clients)
    def kick_client():
        try:
            selected = client_listbox.get(client_listbox.curselection())
            handler = connect_clients.get(selected)
            if handler:
                handler.close_connection()
                log.append(f"Kicked: {selected}")
                messagebox.showinfo("info", f"kicked: {selected}")
        except:
            messagebox.showwarning("Warning", "Select a client first.")
    def show_log():
        log_text = "\n".join(log) or "No logs yet."
        messagebox.showinfo("Log", log_text)
            
    root = tk.Tk()
    root.title("FTP Server")
    
    start_btn = tk.Button(root, text="Start Server", command=on_start_stop)
    start_btn.pack()
    
    client_listbox = tk.Listbox(root)
    client_listbox.pack()
    
    kick_btn = tk.Button(root, text="Kick Selected Cliet", command=kick_client)
    kick_btn.pack()
    
    log_btn = tk.Button(root, text="Show Log", command=show_log)
    log_btn.pack()
    
    
    root.mainloop()