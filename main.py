import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk  # Importing PIL modules
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

root = tk.Tk()
root.title("Credit Card Customer Prediction Model")

# Colors for dark theme
bg_color = "#202020"
button_bg_color = "#333333"
button_fg_color = "white"
text_color = "white"

# Change the theme to "clam"
style = ttk.Style(root)
style.theme_use("clam")

# Configure the styles for buttons and frames
style.configure("TButton", background=button_bg_color, foreground=button_fg_color, font=("Arial", 10, "bold"))
style.configure("TFrame", background=bg_color)
style.configure("TLabel", foreground=text_color, background=bg_color)

def on_enter(event):
    pass

def on_leave(event):
    pass

# Function to set background image
def set_background(image_path):
    img = Image.open(image_path)
    background_image = ImageTk.PhotoImage(img)
    background_label = tk.Label(root, image=background_image)
    background_label.place(relwidth=1, relheight=1)
    background_label.image = background_image

# Set background image
set_background("bg.jpg")  

input_frame = ttk.Frame(root)
input_frame.pack(pady=10)

csv_entry = tk.Entry(input_frame, width=50)
csv_entry.grid(row=0, column=1, padx=5, pady=5)

def select_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        csv_entry.delete(0, tk.END)
        csv_entry.insert(0, file_path)

def train_and_predict(input_csv_path):
    data = pd.read_csv('customers.csv')

    x = data[['Age', 'Salary']]
    y = data['Buy']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=2)
    knn.fit(x_train, y_train)

    input_data = pd.read_csv(input_csv_path)

    predictions = knn.predict(input_data[['Age', 'Salary']])

    input_data['Prediction'] = predictions

    return input_data

def perform_prediction():
    input_csv_path = csv_entry.get()
    try:
        output_data = train_and_predict(input_csv_path)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output_data.to_string(index=False))
    except Exception as e:
        messagebox.showerror("Error", str(e))

    # Enable the save button
    save_button.config(state=tk.NORMAL)

def save_output():
    output = output_text.get(1.0, tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])
    if file_path:
        try:
            with open(file_path, "w") as file:
                file.write(output)
            messagebox.showinfo("Success", "Output saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

predict_button = ttk.Button(input_frame, text="Predict", command=perform_prediction)
predict_button.grid(row=0, column=2, padx=5, pady=5)
predict_button.bind("<Enter>", on_enter)
predict_button.bind("<Leave>", on_leave)

select_button = ttk.Button(input_frame, text="Choose File", command=select_csv_file)
select_button.grid(row=0, column=0, padx=5, pady=5)
select_button.bind("<Enter>", on_enter)
select_button.bind("<Leave>", on_leave)

output_frame = ttk.Frame(root)
output_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL)
output_text = tk.Text(output_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

save_button = ttk.Button(root, text="Save Output", command=save_output, state=tk.DISABLED)
save_button.pack(pady=10)
save_button.bind("<Enter>", on_enter)
save_button.bind("<Leave>", on_leave)

root.mainloop()
