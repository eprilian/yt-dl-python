import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage
import yt_dlp
import threading

def get_formats():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a valid YouTube URL")
        return

    ydl_opts = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])

            format_list.delete(0, tk.END)
            for f in formats:
                if f.get("format_note") and f.get("ext"):
                    format_list.insert(tk.END, f"{f['format_id']} - {f['format_note']} ({f['ext']})")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def choose_save_location():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        save_location.set(folder_selected)

def download_video():
    url = url_entry.get()
    selected_format = format_list.curselection()
    save_path = save_location.get()

    if not url or not selected_format:
        messagebox.showerror("Error", "Please select a format to download")
        return

    if not save_path:
        messagebox.showerror("Error", "Please choose a save location")
        return

    format_id = format_list.get(selected_format[0]).split(" - ")[0]
    ydl_opts = {
        "format": f"{format_id}+bestaudio/best",
        "outtmpl": f"{save_path}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "progress_hooks": [update_progress]
    }

    log_text.insert(tk.END, "Starting download...\n")
    #progress_bar['value'] = 0

    threading.Thread(target=download_thread, args=(url, ydl_opts)).start()

def download_thread(url, ydl_opts):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Success", "Download complete!")
        log_text.insert(tk.END, "Download complete!\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        log_text.insert(tk.END, f"Error: {str(e)}\n")
    finally:
        #progress_bar['value'] = 100
        progress_label.config(text="Download complete!")

def update_progress(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '0%').strip('%')
        eta = d.get('_eta_str', '')
        
        try:
            progress_value = float(percent)
        except ValueError:
            progress_value = 0
        
        progress_label.config(text=f"Downloading: {d.get('_percent_str', '0%')} | ETA: {eta}")
        #progress_bar['value'] = progress_value
        log_text.insert(tk.END, f"Progress: {d.get('_percent_str', '0%')} | ETA: {eta}\n")
        log_text.yview_moveto(1)
    elif d['status'] == 'finished':
        progress_label.config(text="Download complete!")
        #progress_bar['value'] = 100
        log_text.insert(tk.END, "Merging complete!\n")

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("960x680")
root.configure(bg="#1e2a33")

try:
    logo_img = PhotoImage(file="logo.png")
    root.iconphoto(False, logo_img)  
except Exception as e:
    print("Failed to load image!", str(e))

# bg_img = PhotoImage(file="background.png") 
# bg_label = tk.Label(root, image=bg_img)
# bg_label.place(relwidth=1, relheight=1)  


# root.wm_attributes('-alpha', 0.5)

style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#1e2a33", foreground="#ecf0f1")
style.configure("TEntry", font=("Arial", 12), padding=6)

save_location = tk.StringVar()

header_frame = tk.Frame(root, bg="#3498db")
header_frame.pack(fill=tk.X, pady=2)  

try:
    logo_label = tk.Label(header_frame, image=logo_img, bg="#3498db")
    logo_label.pack(pady=2)
except Exception as e:
    print("Failed to load image!", str(e))

header_label = tk.Label(header_frame, text="YouTube Video Downloader", font=("Arial", 12, "bold"), fg="#ecf0f1", bg="#3498db")
header_label.pack(pady=2)

main_frame = tk.Frame(root, bg="#1e2a33")
main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

left_frame = tk.Frame(main_frame, bg="#1e2a33")
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

tk.Label(left_frame, text="Link YouTube:", font=("Arial", 12), fg="#ecf0f1", bg="#1e2a33").pack(side=tk.TOP, pady=5)
url_entry = ttk.Entry(left_frame, width=50)
url_entry.pack(side=tk.TOP, pady=5)

get_formats_btn = ttk.Button(left_frame, text="Process Link", command=get_formats)
get_formats_btn.pack(side=tk.TOP, pady=5)

tk.Label(left_frame, text="Quality Video:", font=("Arial", 12), fg="#ecf0f1", bg="#1e2a33").pack(side=tk.TOP, pady=5)
format_list = tk.Listbox(left_frame, width=50, height=10, bg="#34495e", fg="#ecf0f1")
format_list.pack(side=tk.TOP, pady=5)

tk.Label(left_frame, text="Save Video To:", font=("Arial", 12), fg="#ecf0f1", bg="#1e2a33").pack(side=tk.TOP, pady=5)
save_entry = ttk.Entry(left_frame, textvariable=save_location, width=40)
save_entry.pack(side=tk.TOP, pady=5)

choose_folder_btn = ttk.Button(left_frame, text="Browse", command=choose_save_location)
choose_folder_btn.pack(side=tk.TOP, pady=5)

right_frame = tk.Frame(main_frame, bg="#1e2a33")
right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

download_btn = ttk.Button(right_frame, text="Download Video", command=download_video, width=20)
download_btn.pack(pady=20)

progress_label = tk.Label(right_frame, text="", font=("Arial", 12), fg="#ecf0f1", bg="#1e2a33")
progress_label.pack(pady=5)

#progress_bar = ttk.Progressbar(right_frame, orient=tk.HORIZONTAL, length=500, mode='determinate')
#progress_bar.pack(pady=5)

tk.Label(right_frame, text="Log Download:", font=("Arial", 12), fg="#ecf0f1", bg="#1e2a33").pack(side=tk.TOP, pady=5)

log_text = tk.Text(right_frame, height=10, width=50, state=tk.NORMAL, bg="#34495e", fg="#ecf0f1", font=("Courier New", 10))
log_text.pack(pady=5, fill=tk.BOTH, expand=True)

footer_frame = tk.Frame(root, bg="#1e2a33")
footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

copyright_label = tk.Label(footer_frame, text="© 2025 noname-00. All rights reserved.", font=("Arial", 10), fg="#ecf0f1", bg="#1e2a33")
copyright_label.pack()

root.mainloop()