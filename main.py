import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Function to train the model and perform prediction
def train_and_predict(input_csv_path):
    # Train the model
    data = pd.read_csv('ccd.csv')

    X = data[['Age', 'Salary']]
    y = data['Buy']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    knn = KNeighborsClassifier(n_neighbors=2)
    knn.fit(X_train, y_train)

    # Process the input CSV file
    input_data = pd.read_csv(input_csv_path)

    # Perform prediction
    predictions = knn.predict(input_data[['Age', 'Salary']])

    # Add predictions to input data
    input_data['Prediction'] = predictions

    return input_data

# Function to perform prediction
def perform_prediction():
    # Get the input CSV file path from the entry field
    input_csv_path = csv_entry.get()
    try:
        # Perform prediction using the trained model
        output_data = train_and_predict(input_csv_path)

        # Display prediction results in the output text widget
        output_text.delete(1.0, tk.END)  # Clear previous output
        output_text.insert(tk.END, output_data.to_string(index=False))

    except Exception as e:
        messagebox.showerror("Error", str(e))


# Create main window
root = tk.Tk()
root.title("CreditCue")  # Set the title to "CreditCue"

# Create frame for input fields
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Add label for CSV file path entry field
csv_label = tk.Label(input_frame, text="Enter CSV File Path:")
csv_label.grid(row=0, column=0, padx=5, pady=5)

# Add entry field for CSV file path
csv_entry = tk.Entry(input_frame, width=50)
csv_entry.grid(row=0, column=1, padx=5, pady=5)

# Add button to perform prediction
predict_button = tk.Button(input_frame, text="Predict", command=perform_prediction)
predict_button.grid(row=0, column=2, padx=5, pady=5)

# Create frame for output display
output_frame = tk.Frame(root)
output_frame.pack(pady=10)

# Add output text widget to display prediction results
output_text = tk.Text(output_frame, height=20, width=80)
output_text.pack()

# Run the main event loop
root.mainloop()