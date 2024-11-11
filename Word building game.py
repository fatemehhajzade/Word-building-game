import time
from collections import Counter

# لیست حروف
letters = ['م', 'خ', 'ق', 'س', 'م', 'د', 'ع', 'س', 'م', 'ر', 'ه', 'ش', 'ل', 'ن', 'ه', 'ب', 'ا', 'ن', 'ج', 'ب', 'ا', 'د', 'ک', 'ت', 'ی', 'د', 'ک', 'م', 'ی', 'ف', 'ز', 'م']

# تنظیم زمان بازی به 10 دقیقه
start_time = time.time()
time_limit = 10 * 60  # 10 دقیقه به ثانیه

print("شما 10 دقیقه فرصت دارید تا کلمات را با حروف زیر بسازید:")
print(" ".join(letters))
print("شما می‌توانید هر حرف را فقط یک بار استفاده کنید.")

# دریافت ورودی از کاربر
user_words = []
while True:
    user_input = input("لطفاً یک کلمه وارد کنید (یا برای پایان 'done' را تایپ کنید): ")
    if user_input == "done":
        break
    
    # بررسی اینکه آیا کلمه شامل حروف تکراری است
    if len(set(user_input)) != len(user_input):
        print("این کلمه شامل حروف تکراری است و امتیاز ندارد.")
        continue
    
    # بررسی اینکه آیا کلمه فقط از حروف مجاز تشکیل شده است
    if all(letter in letters for letter in user_input):
        user_words.append(user_input)
    else:
        print("این کلمه شامل حروف نامعتبر است.")

    # بررسی زمان
    elapsed_time = time.time() - start_time
    if elapsed_time > time_limit:
        print("زمان تمام شد!")
        break

# تابع برای محاسبه امتیاز
def calculate_score(words, available_letters):
    score = 0
    used_letters = set()
    score_details = []
    negative_score = 0  # امتیاز منفی برای حروف تکراری

    for word in words:
        word_score = 0
        
        # محاسبه امتیاز بر اساس طول کلمه
        if len(word) == 2:
            continue  # دو حرفی امتیاز ندارد
        elif len(word) in [3, 4]:
            word_score += 2
        else:  # 5 حرفی و بیشتر
            word_score += 4
        
        # محاسبه حروف تکراری و افزودن امتیاز منفی
        letter_counts = Counter(word)
        for count in letter_counts.values():
            if count > 1:
                negative_score += count
        
        used_letters.update(word)
        score_details.append((word, word_score))  # ذخیره جزئیات امتیاز هر کلمه
        score += word_score

    # محاسبه امتیاز منفی برای حروف استفاده نشده
    unused_letters = set(available_letters) - used_letters
    score -= len(unused_letters)

    # اعمال امتیاز منفی برای حروف تکراری
    score -= negative_score

    return score, score_details, negative_score

# محاسبه و نمایش امتیاز نهایی
final_score, score_details, negative_score = calculate_score(user_words, letters)

print("کلمات شما:", user_words)
print("امتیاز نهایی شما:", final_score)

# نمایش جزئیات امتیازدهی
print("جزئیات امتیازدهی:")
for word, word_score in score_details:
    print(f"کلمه '{word}' امتیاز: {word_score}")

if negative_score > 0:
    print(f"امتیاز منفی به دلیل حروف تکراری: {negative_score}")