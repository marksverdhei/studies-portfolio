import tkinter as tk
import time, re, os, string, random
import numpy as np

class TalkingElevator(tk.Frame):
    """Very simple, simulated talking elevator for the IFI building."""
    
    def __init__(self, window_size="600x500"):
        
        self.root = tk.Tk()
        self.root.title("Talking Elevator")
        self.root.geometry(window_size)

        tk.Frame.__init__(self)

        self._add_elevator()
        self._add_chat()

        self.mainloop()
        
        
    def _add_elevator(self, nb_floors=10, start_floor=1):
        """Adds widgets representing the elevator in the IFI building"""
        
        elevator_frame = tk.Frame(self.root)
        elevator_frame.pack(side=tk.LEFT)
        
        elevator_text = tk.Label(elevator_frame, text=" Elevator (current\nposition in red):\n")
        elevator_text.pack()
        
        self.floors ={}
        for i in range(nb_floors, 0, -1):
            self.floors[i] = tk.Label(elevator_frame, text="%i"%i, width=5, height=2, borderwidth=2, 
                                      relief="groove", bg="white")
            self.floors[i].pack()
        
        status_box = tk.Frame(elevator_frame, bd=1, pady=10)
        status_box.pack(expand=True, fill=tk.X)
        status_text = tk.Label(status_box, text="Status:")
        status_text.pack(side=tk.LEFT)
        self.status = tk.Label(status_box, text="Still")
        self.status.pack(side=tk.LEFT)
        
        # We start with the first floor
        self.go_to(start_floor)

    
    def _add_chat(self):
        """Adds widgets representing the chat window"""
        
        chat_frame = tk.Frame(self.root)
        
        # frame containing text box with messages and scrollbar
        self.text_frame = tk.Frame(chat_frame, bd=6)
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        # scrollbar for text box
        self.text_box_scrollbar = tk.Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        # contains messages
        self.text_box = tk.Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, 
                                state=tk.DISABLED,bd=1, padx=6, pady=6, spacing3=8, wrap=tk.WORD, 
                                bg=None, relief=tk.GROOVE, width=10, height=1)
        self.text_box.pack(expand=True, fill=tk.BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = tk.Frame(chat_frame, bd=1)
        self.entry_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # entry field
        self.entry_field = tk.Entry(self.entry_frame, bd=1, justify=tk.LEFT)
        self.entry_field.focus_set()
        self.entry_field.pack(fill=tk.X, padx=6, pady=6, ipady=3)

        # frame containing send button and emoji button
        self.send_button_frame = tk.Frame(chat_frame, bd=0)
        self.send_button_frame.pack(fill=tk.BOTH)

        # send button
        self.send_button = tk.Button(self.send_button_frame, text="Send", width=5, relief=tk.GROOVE, 
                                     bg='white', bd=1, command=self._send_action)
        self.send_button.pack(side=tk.LEFT, padx=6, pady=8, ipady=3)
        self.root.bind("<Return>", self._send_action)
        
        chat_frame.pack(expand=True, fill=tk.BOTH)

        
    def _send_action(self, event=None):
        """Acts upon a send action"""
        
        user_input = self.entry_field.get().strip("{").strip("}")
        self.entry_field.delete(0, tk.END)
        
        # we add some noise to the user input (to emulate ASR errors)
        noisy_input = self._add_noise(user_input)
        
        # We sample the confidence score from a normal distribution
        confidence_score = np.random.normal(0.8, 0.1)
        if noisy_input != user_input:
            confidence_score -= np.random.normal(0.3,0.1)
        confidence_score = max(0, min(1, confidence_score))
            
        # process the user input
        self._show_message("Human", noisy_input, confidence_score)
        self.process(noisy_input, confidence_score)
        
    
    def _add_noise(self, utterance, wer=0.2):
        """Simulate ASR errors by swapping letters in some words"""
        
        new_words = []
        for word in utterance.split():
            if random.random() < wer:
                change_index = random.choice(range(len(word)))
                new_letter = (random.choice("123456789]") if word[change_index].isdigit() 
                              else random.choice(string.ascii_letters))
                word = word[:change_index] + new_letter + word[change_index+1:]
            new_words.append(word)
        return " ".join(new_words)
        
    def _show_message(self, user, message, confidence=1):
        """Shows a message in the chat window (with confidence score in parenthesis)"""

        self.text_box.configure(state=tk.NORMAL)
        conf_string = " (%.2f)"%confidence if confidence < 1 else ""
        self.text_box.insert(tk.END, "%s: %s%s\n"%(user,message, conf_string))
        self.text_box.see(tk.END)
        self.text_box.configure(state=tk.DISABLED)
        
        
    def go_to(self, floor, duration=500):
        """Goes to a given floor (integer)"""
        
        # If urgent stop is triggered, stop ASAP
        self.urgent_stop = False
        
        if not hasattr(self, "cur_floor"):
            self.floors[floor].config(bg="red")
            self.cur_floor = floor
            
        if floor > self.cur_floor:
            next_floors = range(self.cur_floor+1, floor+1)
            self.status.config(text="UP")
        elif floor < self.cur_floor:
            next_floors = range(self.cur_floor-1, floor-1, -1)
            self.status.config(text="DOWN")
        else:
            return
        
        # Move up and down (one floor at a time)
        for next_floor in next_floors:
            if self.urgent_stop:
                break
            self.root.update()
            cur_floor_widget = self.floors[self.cur_floor]
            cur_floor_widget.after(duration, cur_floor_widget.config(bg="white"))
            self.cur_floor = next_floor
            cur_floor_widget = self.floors[self.cur_floor]
            cur_floor_widget.after(duration, cur_floor_widget.config(bg="red"))
        self.status.config(text="Still")


    def process(self, user_message, confidence_score):
        """Process the user inputs"""
       
        raise NotImplementedError("you should implement this method")
       
    
    def respond(self, system_message):
        """Respond to the user via a text message"""
        
        self._show_message("Elevator", system_message)

