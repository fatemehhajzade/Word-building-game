import time
import tkinter as tk
from tkinter import messagebox, ttk
from collections import Counter

# لیست حروف
LETTERS = ['م', 'خ', 'ق', 'س', 'م', 'د', 'ع', 'س', 'م', 'ر', 'ه', 'ش', 'ل', 'ن', 'ه', 'ب', 'ا', 'ن', 'ج', 'ب', 'ا', 'د', 'ک', 'ت', 'ی', 'د', 'ک', 'م', 'ی', 'ف', 'ز', 'م']

# تنظیمات بازی
TIME_LIMIT = 10 * 60  # 10 دقیقه به ثانیه

class WordGame:
    def __init__(self, master):
        self.master = master
        self.master.title("بازی ساخت کلمات")
        self.master.geometry("600x400")
        self.master.configure(bg='#e0f7fa')  # رنگ پس‌زمینه

        self.start_time = time.time()
        self.user_words = []

        self.create_widgets()

    def create_widgets(self):
        # فریم اصلی
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # برچسب‌ها
        ttk.Label(main_frame, text="شما 10 دقیقه فرصت دارید تا کلمات را با حروف زیر بسازید:", 
                  font=("Arial", 14), foreground="darkblue", background='#e0f7fa').pack(pady=10)

        letters_frame = ttk.Frame(main_frame)
        letters_frame.pack(pady=10)
        for letter in LETTERS:
            ttk.Label(letters_frame, text=letter, font=("Arial", 16), foreground="orange", background='#e0f7fa').pack(side=tk.LEFT, padx=2)

        ttk.Label(main_frame, text="لطفاً یک کلمه وارد کنید (یا برای پایان 'done' را تایپ کنید):", 
                  font=("Arial", 14), foreground="darkblue", background='#e0f7fa').pack(pady=10)

        # ورودی کاربر
        self.user_input_entry = ttk.Entry(main_frame, font=("Arial", 14), width=30)
        self.user_input_entry.pack(pady=10)
        self.user_input_entry.focus()

        # دکمه‌ها
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="ارسال کلمه", command=self.process_word).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="پایان بازی", command=self.end_game).pack(side=tk.LEFT, padx=5)

        # نمایش زمان باقی‌مانده
        self.time_label = ttk.Label(main_frame, font=("Arial", 14), foreground="darkred", background='#e0f7fa')
        self.time_label.pack(pady=10)
        self.update_time()

    def update_time(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, TIME_LIMIT - elapsed_time)
        minutes, seconds = divmod(remaining_time, 60)
        self.time_label.config(text=f"زمان باقی‌مانده: {minutes:02d}:{seconds:02d}")
        if remaining_time > 0:
            self.master.after(1000, self.update_time)
        else:
            self.end_game()

    def process_word(self):
        user_input = self.user_input_entry.get().strip()
        
        if not user_input:
            return

        if user_input.lower() == "done":
            self.end_game()
            return

        if len(set(user_input)) != len(user_input):
            messagebox.showwarning("حروف تکراری", "این کلمه شامل حروف تکراری است و امتیاز ندارد.")
        elif self.is_valid_word(user_input):
            self.user_words.append(user_input)
            messagebox.showinfo("کلمه معتبر", f"کلمه '{user_input}' پذیرفته شد.")
        else:
            messagebox.showwarning("حروف نامعتبر", "این کلمه شامل حروف نامعتبر است.")
        
        self.user_input_entry.delete(0, tk.END)

    def is_valid_word(self, word):
        word_counter = Counter(word)
        available_letters_counter = Counter(LETTERS)
        return all(word_counter[letter] <= available_letters_counter[letter] for letter in word_counter)

    def end_game(self):
        score, score_details, negative_score = self.calculate_score()
        result_text = self.format_result(score, score_details, negative_score)
        messagebox.showinfo("نتیجه بازی", result_text)
        self.master.quit()

    def calculate_score(self):
        score = 0
        used_letters = set()
        score_details = []
        negative_score = 0
        
        # ادامه کد...

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGame(root)
    root.mainloop()
