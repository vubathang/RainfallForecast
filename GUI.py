import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from joblib import load

def choose_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)  # Xóa nội dung cũ trong Entry
        file_entry.insert(0, file_path)  # Hiển thị đường dẫn tệp đã chọn
        update_treeview(file_path)

def update_treeview(file_path):
    treeview.delete(*treeview.get_children())  # Xóa tất cả các dòng hiện tại trong Treeview
    
    df = pd.read_csv(file_path)
    df = df[:57]
    for row in df.iterrows():
        date = row['Date']
        rainfall = row['RainFall']
        treeview.insert('', 'end', values=(date, f"{rainfall} mm"))

    # Căn giữa văn bản trong cột 'Date'
    treeview.column('Date', anchor='center', width=70)
    
    # Căn giữa văn bản trong cột 'Rainfall'
    treeview.column('Rainfall', anchor='center')

    # Thiết lập tiêu đề của cột 'Rainfall' in đậm và thêm " mm"
    treeview.heading('Rainfall', text='Rainfall (mm)')

# 
def predict():
    model = load('model.joblib')

    file_path = file_entry.get()
    df = pd.read_csv(file_path)
    X = df['RainFall'].tail(57).values.reshape(1, -1)
    predicted_result = model.predict(X)[0]
    
    if predicted_result == 0:
        predicted_result = "0mm - 50mm"
    elif predicted_result == 1:
        predicted_result = "50mm - 100mm"
    elif predicted_result == 2:
        predicted_result = "100mm - 150mm"
    elif predicted_result == 3:
        predicted_result = "150mm - 200mm"
    result_label.config(text=f"Result: {predicted_result}")
    result_label.config(bg='yellow', font=('Helvetica', 12, 'bold'))

# Create main window
root = tk.Tk()

root.title("Rainfall Forecast")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 500
window_height = 600
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# Đặt vị trí cửa sổ
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Tạo nút "Chọn tệp" và liên kết nó với hàm choose_file()
choose_button = tk.Button(root, text="Choose file", command=choose_file)
choose_button.pack(pady=10)

# Tạo một Entry widget để hiển thị đường dẫn tệp
file_entry = tk.Entry(root, width=40)
file_entry.pack(pady=10)

# Tạo Treeview để hiển thị dữ liệu dưới dạng bảng
treeview = ttk.Treeview(root, columns=('Date', 'Rainfall'), show='headings')
treeview.heading('Date', text='Date')
treeview.heading('Rainfall', text='Rainfall (mm)')
treeview.pack(fill=tk.BOTH, expand=True)

# Tạo nút "Dự đoán" và liên kết nó với hàm predict
predict_button = tk.Button(root, text="Run", command=predict)
predict_button.pack(pady=10)

# Tạo một Label widget để hiển thị kết quả
result_label = tk.Label(root, text="Result")
result_label.pack(pady=20)  # Đặt margin ở dưới là 20px

root.mainloop()
