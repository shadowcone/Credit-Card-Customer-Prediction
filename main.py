import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

root = tk.Tk()
root.configure(bg="#9290C3")
root.title("CreditCue") 

input_frame = tk.Frame(root, bg="#9290C3")
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

predict_button = tk.Button(input_frame, text="Predict", command=perform_prediction, font=("Ariel", 10, "bold"), bg="white", fg="#1B1A55", activebackground="#1B1A55", activeforeground="white")
predict_button.grid(row=0, column=2, padx=5, pady=5)

select_button = tk.Button(input_frame, text="Choose File", command=select_csv_file, font=("Ariel", 10, "bold"), bg="white", fg="#1B1A55", activebackground="#1B1A55", activeforeground="white")
select_button.grid(row=0, column=0, padx=5, pady=5)

output_frame = tk.Frame(root)
output_frame.pack(pady=10)

scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL)
output_text = tk.Text(output_frame, height=20, width=80, yscrollcommand=scrollbar.set)
scrollbar.config(command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

save_button = tk.Button(root, text="Save", command=save_output, state=tk.DISABLED, font=("Ariel", 10, "bold"), bg="white", fg="#1B1A55", activebackground="#1B1A55", activeforeground="white")
save_button.pack(pady=10)

root.mainloop()
