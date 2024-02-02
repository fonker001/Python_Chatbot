#pip install spacy

import tkinter as tk
from tkinter import scrolledtext
import spacy
import os
import json

class ChatbotGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chatbot")

        # Create a scrolled text widget for the chat history
        self.chat_history = scrolledtext.ScrolledText(master, width=40, height=10, state=tk.DISABLED)
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Entry widget for user input
        self.user_input = tk.Entry(master, width=30)
        self.user_input.grid(row=1, column=0, padx=10, pady=10)

        # Button to send user input
        send_button = tk.Button(master, text="Send", command=self.send_message)
        send_button.grid(row=1, column=1, padx=10, pady=10)

        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

        # Filepath for the memory file
        self.memory_filepath = "chatbot_memory.json"

        # Dictionary to store learned responses
        self.learned_responses = self.load_memory()

    def send_message(self):
        user_message = self.user_input.get()
        self.display_message(f"You: {user_message}")

        # Process user message using spaCy
        doc = self.nlp(user_message)

        # Extract verbs from user message
        verbs = [token.text for token in doc if token.pos_ == "VERB"]

        # Generate a response based on the verbs
        response = self.generate_response(verbs)

        self.display_message(f"Chatbot: {response}")
        self.user_input.delete(0, tk.END)

        # Learn from the interaction
        self.learn_from_interaction(user_message, response, verbs)

    def generate_response(self, verbs):
        # Try to use a learned response first
        for verb in verbs:
            if verb in self.learned_responses:
                return self.learned_responses[verb]

        # If no learned response, use a default response
        return "I'm not sure how to respond to that."

    def learn_from_interaction(self, user_message, response, verbs):
        # Update learned responses based on user's feedback
        # Consider learning from a wider range of user inputs
        keywords = ["teach", "fact", "new", "interesting"]
        for keyword in keywords:
            if keyword.lower() in user_message.lower():
                self.learned_responses[keyword] = response

        # Update learned responses based on user's verbs
        for verb in verbs:
            if verb.lower() in user_message.lower():
                self.learned_responses[verb] = response

        # Save the learned responses to the memory file
        self.save_memory()

    def save_memory(self):
        with open(self.memory_filepath, 'w') as file:
            json.dump(self.learned_responses, file)

    def load_memory(self):
        if os.path.exists(self.memory_filepath):
            with open(self.memory_filepath, 'r') as file:
                return json.load(file)
        else:
            return {}

    def display_message(self, message):
        # Enable the text widget to append messages
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.yview(tk.END)
        # Disable the text widget to prevent editing
        self.chat_history.config(state=tk.DISABLED)

# Create the main Tkinter window
if __name__ == "__main__":
    root = tk.Tk()
    chatbot_app = ChatbotGUI(root)
    root.mainloop()
