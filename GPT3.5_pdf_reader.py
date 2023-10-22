from pdfminer.high_level import extract_text
import os
import openai
import json
import tkinter as tk


openai.api_key = 'please use your own, thank you'


def extract_text_from_pdf(pdf_directory):
    text_content = {}
    for file_name in os.listdir(pdf_directory):
        if file_name.endswith('.pdf'):
            file_path = os.path.join(pdf_directory, file_name)
            text = extract_text(file_path)
            text_content[file_name] = text
    return text_content

pdf_directory = "C:\\Users\\Owner\\OneDrive\\Documents\\2023-2024\\Multigas\\AI\\Data"
pdf_texts = extract_text_from_pdf(pdf_directory)


# Assuming pdf_texts is a dictionary containing the extracted text for each PDF file

file_name_to_check = "P1.pdf" 
snippet = pdf_texts[file_name_to_check][:500] # First 500 characters


def ask_gpt3_5(question, reference_material):
    # Maximum tokens for the prompt (leaving room for question)
    max_tokens_prompt = 3947

    # Constructing the prompt with the question
    prompt_question = f"Question: {question}\nReference Material: "
    prompt_completion = "\nAnswer:"

    # Calculating the remaining tokens for the reference material
    remaining_tokens = max_tokens_prompt - len(prompt_question.split()) - len(prompt_completion.split())

    # Truncating the reference material to fit within the token limit
    truncated_reference_material = " ".join(reference_material.split()[:remaining_tokens])

    # Constructing the full prompt
    prompt = prompt_question + truncated_reference_material + prompt_completion

    # Sending the prompt to GPT-3.5
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150 # Tokens for the completion
    )

    # Extracting the answer from the response
    answer = response.choices[0].text

    return answer



def ask_question(question, file_name):
    # Retrieving the reference material from the extracted text of the specified file
    reference_material = pdf_texts[file_name]

    # Calling the GPT-3.5 query function with the question and reference material
    answer = ask_gpt3_5(question, reference_material)

    return answer

def search_term(term):
    results = []
    for file_name, text in pdf_texts.items():
        pages = text.split('\f') # Assuming page breaks are represented by '\f'
        for page_num, page_text in enumerate(pages):
            if term.lower() in page_text.lower():
                results.append((file_name, page_num + 1)) # Page numbers are 1-based
    return results



# Path to the cache file
cache_file_path = "C:\\Users\\Owner\\OneDrive\\Documents\\2023-2024\\Multigas\\AI\\processed_data\\pdf_texts_cache.json"


def save_to_cache(data):
    with open(cache_file_path, 'w') as file:
        json.dump(data, file)

def load_from_cache():
    with open(cache_file_path, 'r') as file:
        return json.load(file)

# Checking if the cache file exists
try:
    pdf_texts = load_from_cache()
    print("Loaded extracted text from cache.")
except FileNotFoundError:
    pdf_texts = extract_text_from_pdf(pdf_directory)
    save_to_cache(pdf_texts)
    print("Extracted text from PDF files and saved to cache.")


# Defining the actions for the search and ask buttons
def on_search():
    term = term_entry.get()
    results = search_term(term)
    search_results_text_widget.delete('1.0', tk.END)
    if results:
        search_results_text_widget.insert(tk.END, '\n'.join([f"{file_name}, page {page_num}" for file_name, page_num in results]))
    else:
        search_results_text_widget.insert(tk.END, f"The term '{term}' was not found in the PDFs.")


def on_ask():
    file_name = file_name_entry.get()
    question = question_entry.get()
    
    ask_results_text_widget.delete('1.0', tk.END)
    if file_name in pdf_texts:
        answer = ask_question(question, file_name)
        ask_results_text_widget.insert(tk.END, answer)
    else:
        ask_results_text_widget.insert(tk.END, f"File {file_name} not found in the extracted texts. Please enter a valid file name.")
        
# Creating and configure the main window
root = tk.Tk()
root.title("PDF Search and Ask")

# Creating the search section
search_label = tk.Label(root, text="Search for a term:")
search_label.pack()

term_entry = tk.Entry(root)
term_entry.pack()

search_button = tk.Button(root, text="Search", command=on_search)
search_button.pack()

search_results_text_widget = tk.Text(root, width=80, height=10, wrap=tk.WORD)
search_results_text_widget.pack()

# Creating the ask section
ask_label = tk.Label(root, text="Ask a question about a file:")
ask_label.pack()

ask_results_text_widget = tk.Text(root, width=80, height=10, wrap=tk.WORD)
ask_results_text_widget.pack()

file_name_label = tk.Label(root, text="File name (e.g., P1.pdf):")
file_name_label.pack()

file_name_entry = tk.Entry(root)
file_name_entry.pack()

question_label = tk.Label(root, text="Question:")
question_label.pack()

question_entry = tk.Entry(root)
question_entry.pack()

ask_button = tk.Button(root, text="Ask", command=on_ask)
ask_button.pack()

ask_results_text = tk.StringVar()
ask_results_label = tk.Label(root, textvariable=ask_results_text)
ask_results_label.pack()

root.mainloop()
