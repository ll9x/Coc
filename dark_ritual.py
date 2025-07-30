import tkinter as tk
from tkinter import font as tkfont
import pygame
import threading
import time
import os
import urllib.request

class DarkRitualApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dark Ritual")
        self.root.configure(bg='black')
        
        # تهيئة الصوت
        pygame.mixer.init()
        
        # تنزيل الملفات الصوتية إذا لم تكن موجودة
        self.audio_files = [
            "demonic_whispers.mp3",
            "ritual1.mp3",
            "ritual2.mp3",
            "ritual3.mp3"
        ]
        
        # روابط بديلة للملفات الصوتية
        self.audio_urls = [
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",  # خلفية
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",  # تعويذة 1
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",  # تعويذة 2
            "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"   # تعويذة 3
        ]
        
        self.download_audio_files()
        
        # قائمة التعاويذ
        self.chants = [
            "Zhar'kal om'thar... nah'zul ven'drath!",
            "Aperium mortis... surgite ex tenebris!",
            "Anhar'kor vel'them... audite vocem meam!"
        ]
        
        self.current_chant = 0
        self.ritual_started = False
        
        # إنشاء الواجهة
        self.create_widgets()
        
    def download_audio_files(self):
        """تحميل الملفات الصوتية إذا لم تكن موجودة"""
        for i, (url, filename) in enumerate(zip(self.audio_urls, self.audio_files)):
            if not os.path.exists(filename):
                try:
                    urllib.request.urlretrieve(url, filename)
                except Exception as e:
                    error_msg = f"Error downloading {filename}: {e}"
                    print(error_msg.encode('utf-8', errors='replace').decode('cp1252', errors='replace'))
    
    def create_widgets(self):
        """إنشاء عناصر واجهة المستخدم"""
        # تعيين حجم النافذة
        self.root.geometry("800x400")
        
        # خط مخصص
        custom_font = tkfont.Font(family="Courier", size=24, weight="bold")
        chant_font = tkfont.Font(family="Courier", size=18, weight="bold")
        
        # عنوان التطبيق
        self.title_label = tk.Label(
            self.root, 
            text="🔥 Dark Ritual 🔥", 
            fg="red", 
            bg="black",
            font=custom_font
        )
        self.title_label.pack(pady=20)
        
        # نص التعويذة
        self.chant_label = tk.Label(
            self.root, 
            text="", 
            fg="red", 
            bg="black",
            font=chant_font,
            wraplength=700
        )
        self.chant_label.pack(pady=50, padx=20)
        
        # زر البدء
        self.start_button = tk.Button(
            self.root, 
            text="ابدأ الطقوس", 
            command=self.start_ritual,
            bg="black",
            fg="red",
            font=("Arial", 14),
            relief="raised",
            bd=3,
            padx=20,
            pady=10
        )
        self.start_button.pack(pady=20)
        
        # تعبئة مساحة فارغة في الأسفل
        self.root.grid_rowconfigure(3, weight=1)
    
    def start_ritual(self):
        """بدء طقوس الظلام"""
        if not self.ritual_started:
            self.ritual_started = True
            self.start_button.config(state="disabled")
            
            # تشغيل الصوت الخلفي
            try:
                pygame.mixer.music.load(self.audio_files[0])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # -1 للتكرار اللانهائي
            except Exception as e:
                print(f"خطأ في تشغيل الصوت الخلفي: {e}")
                
            # بدء عرض التعاويذ
            self.show_next_chant()
    
    def show_next_chant(self):
        """عرض التعويذة التالية"""
        if self.current_chant < len(self.chants):
            # عرض النص
            self.chant_label.config(text=self.chants[self.current_chant])
            
            # تشغيل الصوت
            try:
                if self.current_chant < 3:  # لدينا 3 ملفات صوتية للتعاويذ
                    sound = pygame.mixer.Sound(self.audio_files[self.current_chant + 1])
                    sound.play()
            except Exception as e:
                print(f"خطأ في تشغيل صوت التعويذة: {e}")
            
            self.current_chant += 1
            
            # جدولة التعويذة التالية
            if self.current_chant < len(self.chants):
                self.root.after(6000, self.show_next_chant)
            else:
                self.root.after(6000, self.ritual_complete)
    
    def ritual_complete(self):
        """عند اكتمال الطقوس"""
        self.chant_label.config(text="👿 THEY ARE HERE 👿", font=("Courier", 32, "bold"))
        self.root.after(10000, self.root.destroy)  # إغلاق التطبيق بعد 10 ثواني

def main():
    root = tk.Tk()
    app = DarkRitualApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
