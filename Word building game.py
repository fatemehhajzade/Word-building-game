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
        self.master.geometry("800x600")
        self.master.configure(bg='#E8F5E9')  # سبز کمرنگ

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#E8F5E9')
        self.style.configure('TButton', background='#81D4FA', foreground='black', font=('Arial', 12))  # آبی کمرنگ
        self.style.configure('TLabel', background='#E8F5E9', font=('Arial', 12))
        self.style.configure('TEntry', font=('Arial', 12))

        self.start_time = time.time()
        self.user_words = set()  # استفاده از set برای جلوگیری از کلمات تکراری
        self.current_word = ""
        self.used_letters = set()  # مجموعه حروف استفاده شده

        self.letter_buttons = {}  # دیکشنری برای نگه داشتن دکمه‌ها

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # عنوان بازی
        title_label = ttk.Label(main_frame, text="بازی ساخت کلمات", font=("Arial", 24, "bold"), foreground="#4CAF50")
        title_label.pack(pady=(0, 20))

        # فریم حروف (در وسط صفحه)
        letters_frame = ttk.Frame(main_frame, padding="10")
        letters_frame.pack(pady=10)
        letters_frame.configure(style='Letters.TFrame')
        self.style.configure('Letters.TFrame', background='#F8BBD0')  # صورتی کمرنگ

        # ایجاد دکمه‌ها برای حروف
        for i, letter in enumerate(LETTERS):
            row = i // 8
            col = i % 8
            letter_button = ttk.Button(letters_frame, text=letter, width=5)
            letter_button.grid(row=row, column=col, padx=2, pady=2)
            letter_button.configure(command=lambda l=letter, btn=letter_button: self.add_letter(l, btn))
            self.letter_buttons[letter_button] = letter

        # فریم نمایش کلمه فعلی
        word_frame = ttk.Frame(main_frame, padding="10")
        word_frame.pack(fill=tk.X, pady=10)

        ttk.Label(word_frame, text=":کلمه فعلی", font=("Arial", 14)).pack(side=tk.RIGHT, padx=(10, 0))
        self.current_word_var = tk.StringVar()
        current_word_entry = ttk.Entry(word_frame, textvariable=self.current_word_var, font=("Arial", 14),
                                       state='readonly', width=30, justify='right')
        current_word_entry.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=10)

        clear_button = ttk.Button(word_frame, text="پاک کردن", command=self.clear_word)
        clear_button.pack(side=tk.LEFT)

        submit_button = ttk.Button(word_frame, text="ثبت کلمه", command=self.submit_word)
        submit_button.pack(side=tk.LEFT, padx=(10, 0))

        # نوار پیشرفت زمان
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=TIME_LIMIT)
        self.progress_bar.pack(fill=tk.X, pady=10)

        # نمایش زمان باقی‌مانده
        self.time_label = ttk.Label(main_frame, font=("Arial", 14), foreground="darkred")
        self.time_label.pack(pady=5)

        # لیست کلمات وارد شده
        words_frame = ttk.Frame(main_frame, padding="10")
        words_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(words_frame, text=":کلمات وارد شده", font=("Arial", 14, "bold")).pack(anchor=tk.E)
        self.words_listbox = tk.Listbox(words_frame, font=("Arial", 12), height=5, justify=tk.RIGHT)
        self.words_listbox.pack(fill=tk.BOTH, expand=True)

        # دکمه پایان بازی
        end_button = ttk.Button(main_frame, text="پایان بازی", command=self.end_game)
        end_button.pack(pady=10)

        self.update_time()

    def add_letter(self, letter, button):
        if letter not in self.used_letters:
            self.current_word += letter
            self.current_word_var.set(self.current_word)
            self.used_letters.add(letter)
            button.config(state=tk.DISABLED, text=f"{letter} ×")

    def clear_word(self):
        self.current_word = ""
        self.current_word_var.set(self.current_word)

    def submit_word(self):
        if not self.current_word:
            return

        if self.current_word in self.user_words:
            messagebox.showwarning("کلمه تکراری", "این کلمه قبلاً وارد شده است.")
        elif self.is_valid_word(self.current_word):
            self.user_words.add(self.current_word)
            self.words_listbox.insert(0, self.current_word)  # اضافه کردن به ابتدای لیست
            messagebox.showinfo("کلمه معتبر", f"کلمه '{self.current_word}' پذیرفته شد.")
            self.clear_word()
        else:
            messagebox.showwarning("کلمه نامعتبر", "این کلمه معتبر نیست.")

    def update_time(self):
        elapsed_time = int(time.time() - self.start_time)
        remaining_time = max(0, TIME_LIMIT - elapsed_time)
        minutes, seconds = divmod(remaining_time, 60)
        self.time_label.config(text=f"زمان باقی‌مانده: {minutes:02d}:{seconds:02d}")
        self.progress_var.set(TIME_LIMIT - remaining_time)
        if remaining_time > 0:
            self.master.after(1000, self.update_time)
        else:
            self.end_game()

    def is_valid_word(self, word):
        word_counter = Counter(word)
        available_letters_counter = Counter(LETTERS)
        return all(word_counter[letter] <= available_letters_counter[letter] for letter in word_counter)

    def calculate_score(self):
        score = 0
        for word in self.user_words:
            if len(word) in [3, 4]:
                score += 2
            elif len(word) >= 5:
                score += 4

        unused_letters = set(LETTERS) - self.used_letters
        negative_score = len(unused_letters)

        return score, negative_score

    def format_result(self, score, negative_score):
        result = f"امتیاز مثبت: {score}\n"
        result += f"امتیاز منفی: {negative_score}\n"
        result += f"امتیاز نهایی: {score - negative_score}\n\n"
        result += f"تعداد کلمات ساخته شده: {len(self.user_words)}\n\n"
        result += "کلمات شما:\n"
        result += "\n".join(sorted(self.user_words))
        return result

    def show_results(self):
        score, negative_score = self.calculate_score()
        result_text = self.format_result(score, negative_score)
        messagebox.showinfo("نتیجه بازی", result_text)

    def end_game(self):
        self.show_results()
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGame(root)
    root.mainloop()
