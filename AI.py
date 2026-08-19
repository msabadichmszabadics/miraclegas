import os
import wikipediaapi
import json
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import CountVectorizer
from torch.utils.data import DataLoader, Dataset, TensorDataset
import numpy as np
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
import gc
from collections import defaultdict
import logging

# Parameters
BATCH_SIZE = 16
EPOCHS = 5
LEARNING_RATE = 0.001

# Enable logging
logging.basicConfig(level=logging.DEBUG)

# Preallocate 16 GB of RAM
fixed_memory = np.zeros((16 * 1024 * 1024 * 1024 // np.dtype(np.uint8).itemsize,), dtype=np.uint8)  # 16 GB

# Check if CUDA is available
use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")
print(f'Using device: {device}')

gc.enable()

torch.backends.cudnn.benchmark = True

# Global variables
loaded_data = None

nltk.download('punkt')
nltk.download('stopwords')

# Dummy training data
X_train = torch.randn(1000, 10).to(device)
y_train = torch.randn(1000, 100).to(device)

# Create a DataLoader
train_dataset = TensorDataset(X_train, y_train)
data_loader = DataLoader(train_dataset, batch_size=16, shuffle=False)

# Define CountVectorizer outside of functions
vectorizer = CountVectorizer(tokenizer=word_tokenize, stop_words=stopwords.words('english'))

# Define global variables for model, criterion, optimizer, and vectorizer
model = None
criterion = None
optimizer = None
vectorizer = None

# Simple Neural Network
# Example model definition
class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Train model
def train_model(model, data_loader, criterion, optimizer, epochs=1):
    model.train()
    for epoch in range(epochs):
        for inputs, labels in data_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, torch.zeros(len(labels)).long().to(device))
            loss.requires_grad = True
            loss.backward()
            optimizer.step()

def fetch_and_categorize_from_wikipedia(page_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.3'
    }
    wiki_wiki = wikipediaapi.Wikipedia('en', headers=headers)
    page = wiki_wiki.page(page_name)
    if page.exists():
        content = page.text
        categories = page.categories.keys()
        return content, categories
    else:
        return None, None

def topic_exists(topic):
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            if topic in data:
                return True
    return False

def article_exists(topic, article):
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            if topic in data and article in data[topic]:
                return True
    return False

def fetch_and_add_to_json(topic, article):
    wiki_wiki = wikipediaapi.Wikipedia("en")
    page = wiki_wiki.page(article)
    if page.exists():
        data = defaultdict(list)
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        data[topic].append(article)
        with open(json_path, "w") as f:
            json.dump(data, f)
        messagebox.showinfo("Success", f"Article '{article}' added to topic '{topic}' in JSON file.")
    else:
        messagebox.showerror("Error", f"Article '{article}' does not exist on Wikipedia.")

def handle_user_input():
    topic = topic_entry.get().strip()
    article = article_entry.get().strip()
    
    if not topic or not article:
        messagebox.showerror("Error", "Please enter both topic and article.")
        return
    
    if not topic_exists(topic):
        messagebox.showinfo("Info", f"Topic '{topic}' not found in JSON file. Fetching data from Wikipedia...")
        fetch_and_add_to_json(topic, article)
    else:
        if article_exists(topic, article):
            messagebox.showinfo("Info", f"Article '{article}' already exists under topic '{topic}' in JSON file.")
        else:
            messagebox.showinfo("Info", f"Topic '{topic}' found in JSON file, but article '{article}' not found.")

def load_word_list_and_fetch():
    file_path = filedialog.askopenfilename()
    if not file_path:
        messagebox.showerror("Error", "No file selected.")
        return
    
    topic = topic_entry.get().strip()
    if not topic:
        messagebox.showerror("Error", "Please enter a topic.")
        return
    
    with open(file_path, "r") as file:
        words = file.read().splitlines()
    
    if not words:
        messagebox.showerror("Error", "Word list is empty.")
        return
    
    for word in words:
        fetch_and_add_to_json(topic, word)

def select_memory_storage_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        storage_var.set(folder_path)

def accept_memory_storage_folder():
    # This function retrieves the selected folder path from the storage variable and proceeds to create necessary files.
    memory_storage_folder = storage_var.get()
    if not memory_storage_folder:
        # If no folder is selected, it prompts the user with an error message.
        messagebox.showerror("Error", "Please select a memory storage folder.")
        return
    else:
        # If a folder is selected, it ensures the folder exists and creates necessary JSON and SQLite files.
        if not os.path.exists(memory_storage_folder):
            os.makedirs(memory_storage_folder)
        json_path = os.path.join(memory_storage_folder, 'data.json')
        create_json_file(json_path)
        db_path = os.path.join(memory_storage_folder, 'data.db')
        create_sqlite_db(db_path)
        # Notifies the user that the memory storage folder is selected and necessary files are created.
        messagebox.showinfo("Memory Storage Selected", f"Memory storage folder set to:\n{memory_storage_folder}")
        messagebox.showinfo("First Run", "JSON and SQLite files created.")



def add_data_to_db(db_path, title, content, categories):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO wiki_data (title, content) VALUES (?, ?)', (title, content))
        for category in categories:
            c.execute('INSERT INTO wiki_categories (title, category) VALUES (?, ?)', (title, category))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        print(f"Data with title '{title}' already exists in the database.")
        conn.close()

def create_sqlite_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS wiki_data
                    (title TEXT PRIMARY KEY, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS wiki_categories
                    (title TEXT, category TEXT)''')
    conn.commit()
    conn.close()

def create_json_file(json_path):
    with open(json_path, 'w') as f:
        json.dump({}, f)

def load_data_from_db(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM wiki_data')
    data = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    return data

def load_data_from_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data

def update_storage():
    global loaded_data
    if storage_var.get() == "SQLite":
        loaded_data = load_data_from_db(db_path_var.get())
    else:
        loaded_data = load_data_from_json(json_path_var.get())
    messagebox.showinfo("Storage Updated", "Data loaded from " + storage_var.get())

def incremental_learning(model, data_loader, new_data, criterion, optimizer, vectorizer, epochs=1):
    new_text = fetch_data_from_api(new_data)
    if new_text:
        new_text_tensor = vectorizer.transform([new_text]).toarray()
        new_text_tensor = torch.tensor(new_text_tensor, dtype=torch.float32)
        
        if new_data in class_label_mapping:
            new_label = class_label_mapping[new_data]
            new_labels = torch.tensor([new_label] * new_text_tensor.shape[0], dtype=torch.long)
        else:
            raise ValueError(f"Unknown class label: {new_data}")
        
        assert new_text_tensor.shape[0] == new_labels.shape[0], "Size mismatch between tensors"
        
        new_data_loader = DataLoader(TensorDataset(new_text_tensor, new_labels), batch_size=BATCH_SIZE, shuffle=False)
        train_model(model, new_data_loader, criterion, optimizer, epochs)

# Custom learning categories and priorities
learning_categories = {"Technology": 1, "Science": 1, "History": 1}

def start_learning():
    global model, criterion, optimizer, loaded_data, vectorizer
    
    if not storage_var.get():
        messagebox.showerror("Error", "No memory storage folder selected.")
        return
    
    memory_storage_folder = storage_var.get()
    json_path = os.path.join(memory_storage_folder, 'data.json')
    db_path = os.path.join(memory_storage_folder, 'data.db')
    
    logging.debug(f"SQLite database path: {db_path}")
    try:
        if storage_var.get() == "SQLite":
            loaded_data = load_data_from_db(db_path)
        else:
            loaded_data = load_data_from_json(json_path)
        
        corpus = list(loaded_data.values())
        vectorizer = CountVectorizer(tokenizer=word_tokenize, stop_words=stopwords.words('english'))
        vectorizer.fit(corpus)
        
        input_size = 4096
        hidden_size = 4096
        output_size = len(learning_categories)
        model = SimpleNN(input_size, hidden_size, output_size).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
        
        topics_to_learn = topic_entry.get().split(',')
        for topic in topics_to_learn:
            content, categories = fetch_and_categorize_from_wikipedia(topic)
            if content:
                add_data_to_db(db_path, topic, content, categories)
                if use_cuda:
                    calculate_on_gpu0(model, data_loader, topic, criterion, optimizer, vectorizer, epochs=EPOCHS)
                else:
                    calculate_on_cpu(model, data_loader, topic, criterion, optimizer, vectorizer, epochs=EPOCHS)
        
        messagebox.showinfo("Learning Started", f"Started learning about {', '.join(topics_to_learn)}.")

    except Exception as e:
        logging.error(f"Error in start_learning: {e}")
        messagebox.showerror("Error", f"An error occurred while starting learning: {e}")

# UI setup
# UI setup
root = tk.Tk()
root.title("Wikipedia Data Fetcher")

# Initialize storage variable
storage_var = tk.StringVar()


# Topic Entry
topic_frame = tk.Frame(root)
topic_frame.pack(pady=10)

topic_label = tk.Label(topic_frame, text="Enter topic:")
topic_label.pack(side=tk.LEFT)

topic_entry = tk.Entry(topic_frame, width=40)
topic_entry.pack(side=tk.LEFT)

# Article Entry
article_frame = tk.Frame(root)
article_frame.pack(pady=10)

article_label = tk.Label(article_frame, text="Enter article:")
article_label.pack(side=tk.LEFT)

article_entry = tk.Entry(article_frame, width=40)
article_entry.pack(side=tk.LEFT)

# Load Word List Button
load_wordlist_button = tk.Button(root, text="Load Word List and Fetch", command=load_word_list_and_fetch)
load_wordlist_button.pack(pady=10)

# Select Memory Storage Folder Button
select_storage_button = tk.Button(root, text="Select Memory Storage Folder", command=select_memory_storage_folder)
select_storage_button.pack(pady=10)

# Accept Memory Storage Folder Button
accept_storage_button = tk.Button(root, text="Accept Memory Storage Folder", command=accept_memory_storage_folder)
accept_storage_button.pack(pady=10)

# Run Learning Button
run_learning_button = tk.Button(root, text="Start Learning", command=start_learning)
run_learning_button.pack(pady=10)

root.mainloop()

   
