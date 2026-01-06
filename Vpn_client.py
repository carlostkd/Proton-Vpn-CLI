import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import shlex

BASE_URL = "https://carlostkd.ch/proton"
ENDPOINTS = [
    "api.php?",
    "api_diff.php?",
    "api_location.php?",
    "api_ip.php?",
    "api_console.php?"
]
USER_AGENT = "CarlostkdProtonApp/1.0 (+https://carlostkd.ch)"

# color scheme
COLORS = {
    'bg': '#1a1a2e',
    'fg': '#ffffff',
    'accent': '#8b5cf6',
    'accent_hover': '#a78bfa',
    'card': '#16213e',
    'input_bg': '#0f3460',
    'border': '#533483',
    'text_muted': '#a0a0a0',
    'success': '#10b981',
    'error': '#ef4444'
}

def build_full_url():
    endpoint = endpoint_var.get()
    params = params_entry.get().strip()
    token = token_entry.get().strip()
    if token:
        if params:
            params = f"{params}&token={token}"
        else:
            params = f"token={token}"
    return f"{BASE_URL}/{endpoint}{params}"

def run_curl(url: str):
    cmd = f'curl -s -A "{USER_AGENT}" "{url}"'
    args = shlex.split(cmd)
    try:
        completed = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = completed.stdout + completed.stderr
        return output
    except Exception as e:
        return f"Error executing curl: {e}"

def update_url_display(*args):
    url = build_full_url()
    url_text.config(state='normal')
    url_text.delete(1.0, tk.END)
    url_text.insert(1.0, url)
    url_text.config(state='disabled')

def copy_url():
    url = build_full_url()
    root.clipboard_clear()
    root.clipboard_append(url)
    copy_btn.config(text="Copied!")
    root.after(2000, lambda: copy_btn.config(text="Copy URL"))

def show_documentation():
    docs = """
 API DOCUMENTATION
RETRIEVE ALL SERVERS FROM ALL COUNTRIES
GET /api.php?country=all
GET SERVERS FROM A SPECIFIC COUNTRY
GET /api.php?country=CH
SEARCH SERVERS BY CITY NAME
GET /api.php?city=zurich
GET THE TOTAL SERVERS WORLDWIDE
GET /api.php?total
TOTAL NUMBER OF SERVERS BY CITY
GET /api.php?city=zurich&total
TOTAL NUMBER OF SERVERS BY COUNTRY
GET /api.php?country=ch&total
FILTER BY COUNTRY AND SEARCH BY CITY
GET /api.php?country=US&city=Seattle
DISABLE SERVER INTERNAL IDS IN RESPONSE
GET /api.php?country=CH&include_id=0
USE ALL PARAMETERS TOGETHER FOR ADVANCED QUERIES
Multiple filters can be combined in a single request
LOOKUP BY IP
GET /api.php?ip=185.159.158.141
LIST FREE SERVERS
GET /api.php?free=1
FILTER BY LOAD
GET /api.php?max_load=30
ONLINE STATUS - ONLINE/OFFLINE
GET /api.php?status=online
GET BEST SERVER (LESS LOAD)
GET /api.php?country=US&best=1
COMBINE SEARCH FILTERS
GET /api.php?country=CH&free=1&status=online
CHECK LOAD CHANGES (HOURLY) | Example: CH-4
GET /api_diff.php?diff_load=CH-4
CHECK LOAD CHANGES (PAST 7 DAYS) | Use lastN parameter
GET /api_diff.php?last1=CH-4
GET SERVER LOCATION | Example: CH-4
GET /api_location.php?server=CH-4
CHECK SERVER IP (ENTRY/EXIT) | Example: CH-4
GET /api_ip.php?server=CH-4
  CONSOLE ENDPOINT (USE WITH Caution)
GET /api_console.php
Note: Don't use this unless you're auditioning for a 'What Not to Do' tutorial.
"""
    response_text.config(state='normal')
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, docs)
    response_text.config(state='disabled')

def send_request():
    url = build_full_url()
    response_text.config(state='normal')
    response_text.delete(1.0, tk.END)
    response_text.insert(tk.END, "Sending request...\n")
    response_text.config(state='disabled')
    send_btn.config(state='disabled', text="Sending...")
    def worker():
        out = run_curl(url)
        response_text.config(state='normal')
        response_text.delete(1.0, tk.END)
        response_text.insert(tk.END, out)
        response_text.config(state='disabled')
        send_btn.config(state='normal', text="Send Request")
    threading.Thread(target=worker, daemon=True).start()

# main window
root = tk.Tk()
root.title("Proton API Client")
root.geometry("900x700")
root.configure(bg=COLORS['bg'])

# style
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background=COLORS['bg'])
style.configure('TLabel',
                background=COLORS['bg'],
                foreground=COLORS['fg'],
                font=('Segoe UI', 10))
style.configure('Title.TLabel',
                background=COLORS['bg'],
                foreground=COLORS['fg'],
                font=('Segoe UI', 20, 'bold'))
style.configure('Subtitle.TLabel',
                background=COLORS['bg'],
                foreground=COLORS['text_muted'],
                font=('Segoe UI', 9))
style.configure('TEntry',
                fieldbackground=COLORS['input_bg'],
                foreground=COLORS['fg'],
                bordercolor=COLORS['border'],
                lightcolor=COLORS['border'],
                darkcolor=COLORS['border'])
style.configure('TCombobox',
                fieldbackground=COLORS['input_bg'],
                foreground=COLORS['fg'],
                background=COLORS['input_bg'],
                bordercolor=COLORS['border'],
                arrowcolor=COLORS['fg'])

# container
main_frame = ttk.Frame(root, padding="30")
main_frame.pack(fill=tk.BOTH, expand=True)

# header
header_frame = ttk.Frame(main_frame)
header_frame.pack(fill=tk.X, pady=(0, 20))
title_label = ttk.Label(header_frame, text="Proton API Client", style='Title.TLabel')
title_label.pack()
subtitle_label = ttk.Label(header_frame, text="Dashboard Proton Vpn API", style='Subtitle.TLabel')
subtitle_label.pack()

# card frame
card_frame = tk.Frame(main_frame, bg=COLORS['card'], highlightbackground=COLORS['border'], highlightthickness=1)
card_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
inner_frame = ttk.Frame(card_frame, padding="20")
inner_frame.pack(fill=tk.BOTH, expand=True)

# endpoints
ttk.Label(inner_frame, text="Endpoint").grid(column=0, row=0, sticky=tk.W, pady=(0, 5))
endpoint_var = tk.StringVar(value=ENDPOINTS[0])
endpoint_combo = ttk.Combobox(inner_frame, textvariable=endpoint_var, values=ENDPOINTS, state='readonly', width=40)
endpoint_combo.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=(0, 15))
endpoint_combo.bind('<<ComboboxSelected>>', update_url_display)

# parameters
ttk.Label(inner_frame, text="Parameters (e.g., country=ch)").grid(column=0, row=2, sticky=tk.W, pady=(0, 5))
params_entry = ttk.Entry(inner_frame, width=40, font=('Consolas', 10))
params_entry.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=(0, 15))
params_entry.bind('<KeyRelease>', update_url_display)

# token input
ttk.Label(inner_frame, text="Token (optional)").grid(column=0, row=4, sticky=tk.W, pady=(0, 5))
token_entry = ttk.Entry(inner_frame, width=40, show="", font=('Consolas', 10))
token_entry.grid(column=0, row=5, sticky=(tk.W, tk.E), pady=(0, 15))
token_entry.bind('<KeyRelease>', update_url_display)

# copy button
url_frame = tk.Frame(inner_frame, bg=COLORS['card'])
url_frame.grid(column=0, row=6, sticky=(tk.W, tk.E), pady=(0, 15))
ttk.Label(url_frame, text="Full URL").pack(anchor=tk.W, pady=(0, 5))
url_display_frame = tk.Frame(url_frame, bg=COLORS['input_bg'], highlightbackground=COLORS['accent'], highlightthickness=1)
url_display_frame.pack(fill=tk.X)
url_text = tk.Text(url_display_frame, height=2, bg=COLORS['input_bg'], fg=COLORS['accent'],
                   font=('Consolas', 9), wrap=tk.WORD, padx=10, pady=8, relief=tk.FLAT)
url_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
copy_btn = tk.Button(url_display_frame, text="Copy URL", bg=COLORS['accent'], fg=COLORS['fg'],
                     font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, padx=15, cursor='hand2',
                     activebackground=COLORS['accent_hover'], command=copy_url)
copy_btn.pack(side=tk.RIGHT, padx=5, pady=5)

# send and documentation buttons
button_frame = tk.Frame(inner_frame, bg=COLORS['card'])
button_frame.grid(column=0, row=7, pady=(0, 20))
send_btn = tk.Button(button_frame, text="Send Request", bg=COLORS['accent'], fg=COLORS['fg'],
                     font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, padx=30, pady=12,
                     cursor='hand2', activebackground=COLORS['accent_hover'], command=send_request)
send_btn.pack(side=tk.LEFT, padx=5)
docs_btn = tk.Button(button_frame, text="API Documentation", bg=COLORS['input_bg'], fg=COLORS['fg'],
                     font=('Segoe UI', 11, 'bold'), relief=tk.FLAT, padx=30, pady=12,
                     cursor='hand2', activebackground=COLORS['border'], command=show_documentation)
docs_btn.pack(side=tk.LEFT, padx=5)

# response area
ttk.Label(inner_frame, text="Response").grid(column=0, row=8, sticky=tk.W, pady=(0, 5))
response_frame = tk.Frame(inner_frame, bg=COLORS['input_bg'], highlightbackground=COLORS['border'], highlightthickness=1)
response_frame.grid(column=0, row=9, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
scrollbar = tk.Scrollbar(response_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
response_text = tk.Text(response_frame, bg=COLORS['input_bg'], fg=COLORS['fg'],
                        font=('Consolas', 9), wrap=tk.WORD, padx=10, pady=10,
                        relief=tk.FLAT, yscrollcommand=scrollbar.set)
response_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=response_text.yview)
response_text.config(state='disabled')

# grid weights
inner_frame.columnconfigure(0, weight=1)
inner_frame.rowconfigure(9, weight=1)

# footer
footer_label = ttk.Label(main_frame,
                         text=f"User-Agent: {USER_AGENT}",
                         style='Subtitle.TLabel')
footer_label.pack(pady=(10, 0))

# initial URL display
update_url_display()

# button hover effects
def on_enter(e, btn, color):
    btn['background'] = color
def on_leave(e, btn, color):
    btn['background'] = color
send_btn.bind("<Enter>", lambda e: on_enter(e, send_btn, COLORS['accent_hover']))
send_btn.bind("<Leave>", lambda e: on_leave(e, send_btn, COLORS['accent']))
copy_btn.bind("<Enter>", lambda e: on_enter(e, copy_btn, COLORS['accent_hover']))
copy_btn.bind("<Leave>", lambda e: on_leave(e, copy_btn, COLORS['accent']))
docs_btn.bind("<Enter>", lambda e: on_enter(e, docs_btn, COLORS['border']))
docs_btn.bind("<Leave>", lambda e: on_leave(e, docs_btn, COLORS['input_bg']))

root.mainloop()
