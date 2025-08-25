# app_gui.py dosyası

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox, colorchooser
import os
import threading
# clipgoat_backend.py dosyasından create_story_video fonksiyonunu import ediyoruz
from clipgoat_backend import create_story_video 

class ClipGoatLocalGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ClipGoat Local - Video Story Maker")
        self.geometry("700x650") 
        self.configure(bg="#f5f5f5")

        # Stil tanımlaması (ttk widget'ları için)
        self.style = ttk.Style(self)
        self.style.theme_use('clam') 
        self.style.configure('TLabel', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10))
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white', font=('Arial', 10, 'bold')) 
        self.style.map('Accent.TButton', background=[('active', '#45a049')])

        # Arka plan videosu seçimi
        ttk.Label(self, text="Arka Plan Videosu Seç:", font=("Arial", 10, "bold")).pack(pady=(10, 0))
        self.video_path = tk.StringVar()
        video_frame = ttk.Frame(self)
        video_frame.pack(fill="x", padx=10)
        self.video_entry = ttk.Entry(video_frame, textvariable=self.video_path, width=60)
        self.video_entry.pack(side="left", padx=5, pady=5)
        ttk.Button(video_frame, text="Gözat", command=self.select_video).pack(side="left", padx=5)

        # Hikaye kutusu
        ttk.Label(self, text="Hikaye Metni:", font=("Arial", 10, "bold")).pack(pady=(15, 0))
        self.story_text = scrolledtext.ScrolledText(self, height=8, width=80, wrap=tk.WORD) 
        self.story_text.pack(pady=5)

        # Ayarlar (isteğe bağlı)
        settings_frame = ttk.LabelFrame(self, text="Ayarlar", relief=tk.RIDGE, padding=(10, 5)) 
        settings_frame.pack(fill="x", padx=10, pady=10)

        for i in range(7): 
            settings_frame.grid_rowconfigure(i, weight=1)
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(settings_frame, text="Yazı Tipi Boyutu:", font=("Arial", 9)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.font_size = tk.IntVar(value=32)
        ttk.Spinbox(settings_frame, from_=10, to=72, textvariable=self.font_size, width=5).grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="Yazı Rengi:", font=("Arial", 9)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.font_color = tk.StringVar(value="#FFFFFF")
        self.font_color_btn = ttk.Button(settings_frame, text="Renk Seç", command=self.choose_font_color)
        self.font_color_btn.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="Kutu Rengi:", font=("Arial", 9)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.box_color = tk.StringVar(value="#000000")
        self.box_color_btn = ttk.Button(settings_frame, text="Renk Seç", command=self.choose_box_color)
        self.box_color_btn.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="Kutu Şeffaflığı (0-1):", font=("Arial", 9)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.box_opacity = tk.DoubleVar(value=0.6)
        ttk.Spinbox(settings_frame, from_=0.0, to=1.0, increment=0.1, textvariable=self.box_opacity, width=5).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="Altyazı Konumu:", font=("Arial", 9)).grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.position = tk.StringVar(value="bottom")
        ttk.Combobox(settings_frame, textvariable=self.position, values=["bottom", "top", "center"], width=10, state="readonly").grid(row=4, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="TTS Hızı:", font=("Arial", 9)).grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.tts_rate = tk.IntVar(value=180)
        ttk.Spinbox(settings_frame, from_=100, to=300, textvariable=self.tts_rate, width=5).grid(row=5, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(settings_frame, text="TTS Sesi:", font=("Arial", 9)).grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.tts_gender = tk.StringVar(value="female")
        ttk.Combobox(settings_frame, textvariable=self.tts_gender, values=["female", "male"], width=10, state="readonly").grid(row=6, column=1, padx=5, pady=5, sticky="w")

        self.create_btn = ttk.Button(self, text="Videoyu Oluştur", command=self.create_video, style='Accent.TButton') 
        self.create_btn.pack(pady=20)

        self.status_label = ttk.Label(self, text="", foreground="blue", font=("Arial", 10, "bold")) 
        self.status_label.pack(pady=5)
        
    def select_video(self):
        path = filedialog.askopenfilename(title="Video Seç", filetypes=[("Video Dosyaları", "*.mp4;*.mov;*.avi;*.mkv")])
        if path:
            self.video_path.set(path)

    def choose_font_color(self):
        color = colorchooser.askcolor(title="Yazı Rengi Seç", initialcolor=self.font_color.get()) 
        if color[1]:
            self.font_color.set(color[1])

    def choose_box_color(self):
        color = colorchooser.askcolor(title="Kutu Rengi Seç", initialcolor=self.box_color.get()) 
        if color[1]:
            self.box_color.set(color[1])

    def create_video(self):
        video = self.video_path.get()
        story = self.story_text.get("1.0", tk.END).strip()
        font_size = self.font_size.get()
        font_color = self.font_color.get()
        box_color = self.box_color.get()
        box_opacity = self.box_opacity.get()
        position = self.position.get()
        tts_rate = self.tts_rate.get()
        tts_gender = self.tts_gender.get()

        if not video or not os.path.exists(video):
            messagebox.showerror("Hata", "Lütfen geçerli bir arka plan videosu seçin!")
            return
        if not story:
            messagebox.showerror("Hata", "Lütfen bir hikaye metni girin!")
            return
        
        self.create_btn.config(state=tk.DISABLED)
        self.video_entry.config(state=tk.DISABLED)
        self.story_text.config(state=tk.DISABLED)
        
        # Ayarlar frame içindeki tüm girdileri devre dışı bırak
        for child in self.winfo_children():
            if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Ayarlar":
                for widget in child.winfo_children():
                    if isinstance(widget, (ttk.Entry, ttk.Spinbox, ttk.Combobox, ttk.Button)):
                        widget.config(state=tk.DISABLED)
        
        self.status_label.config(text="Video oluşturuluyor... Lütfen bekleyin. Bu biraz zaman alabilir.", foreground="orange")
        
        thread = threading.Thread(target=self._process_create, args=(video, story, font_size, font_color, box_color, box_opacity, position, tts_rate, tts_gender))
        thread.start()

    def _process_create(self, video, story, font_size, font_color, box_color, box_opacity, position, tts_rate, tts_gender):
        try:
            out_path = create_story_video(
                video, story, font_size, font_color, box_color, box_opacity, position, tts_rate, tts_gender
            )
            self.status_label.config(text=f"Video başarıyla oluşturuldu!\nÇıktı Yolu: {out_path}", foreground="green")
            messagebox.showinfo("Başarılı", f"Video başarıyla oluşturuldu:\n{out_path}")
        except Exception as e:
            self.status_label.config(text=f"Hata oluştu: {e}", foreground="red")
            messagebox.showerror("Hata", f"Video oluşturulurken bir hata oluştu: {e}\n\nLütfen geçici dosyaların veya video dosyalarının başka bir uygulama tarafından kilitlenmediğinden emin olun. TTS hız ayarınızı kontrol edin.")
        finally:
            self.create_btn.config(state=tk.NORMAL)
            self.video_entry.config(state=tk.NORMAL)
            self.story_text.config(state=tk.NORMAL)
            
            # Ayarlar frame içindeki tüm girdileri tekrar etkinleştir
            for child in self.winfo_children():
                if isinstance(child, ttk.LabelFrame) and child.cget("text") == "Ayarlar":
                    for widget in child.winfo_children():
                        if isinstance(widget, (ttk.Entry, ttk.Spinbox, ttk.Combobox, ttk.Button)):
                            widget.config(state=tk.NORMAL)

if __name__ == "__main__":
    app = ClipGoatLocalGUI()
    app.mainloop()