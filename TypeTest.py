#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import random
import sys

class TypeTester:
    def __init__(self):
        self.window = self.create_window()

        self.my_font = Font(family = "Verdana", size ="12", weight = "bold")
        self.random_line = ""
        self.wpm_value = tk.DoubleVar()
        self.average_value = tk.DoubleVar()
        
        # Create containers
        self.text_frame, self.entry_frame, self.info_frame = self.create_frames(self.window)
        # Create widgets
        self.text_widget = self.create_text_widget()
        self.entry_widget = self.create_entry_widget()
        self.pwm_title_label, self.pwm_value_label = self.create_info_widgets("WPM", self.wpm_value)
        self.average_title_label, self.average_value_label = self.create_info_widgets("Average", self.average_value)

        self.set_tags()
        self.initialize_all()
        self.set_callbacks()
        
        self.load_random_line()
        self.entry_widget.focus()
        
    def create_window(self):
        window = tk.Tk()
        window.title("TypeTester")
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.resizable(True, True)                # expand hor/ver       
        
        return window
        
    def create_frames(self, window):
        text_frame = tk.Frame(window)                    
        text_frame.grid(row=1, column=0, sticky = "news")
        #text_frame.columnconfigure(0, weight=1)
        #text_frame.rowconfigure(1, weight=1)
        
        entry_frame = tk.Frame(window)                    
        entry_frame.grid(row=0, column=0, sticky = "new")
        
        info_frame = tk.Frame(window)                    
        info_frame.grid(row=2, column=0)
        
        return text_frame, entry_frame, info_frame

    def create_text_widget(self):
        text_widget = tk.Text(self.text_frame, width=50, height=10, font=self.my_font, wrap="word")
        text_widget.pack(side="top", fill = "both", expand = True)
        #text_widget.grid(row=0, column=0, sticky = "news")
        
        return text_widget

    def create_entry_widget(self):
        entry_widget = ttk.Entry(self.entry_frame, width=50, font = self.my_font)          
        entry_widget.pack(side="top", fill = "both")
        #entry_widget.grid(row=0, column=0)

        return entry_widget

    def create_info_widgets(self, title ,value):
        title_label = tk.Label(self.info_frame, font= self.my_font, text = title, anchor = "ne")
        value_label = tk.Label(self.info_frame, font= self.my_font, textvariable=value, anchor = "nw",width = 7)
        #title_label.grid(row=0, column=0)
        #value_label.grid(row=0, column=1)
        title_label.pack(side="left")
        value_label.pack(side="left")

        return title_label, value_label
        
    def set_tags(self):
        self.text_widget.tag_configure("correct", foreground="gray")
        self.text_widget.tag_configure("wrong", foreground="red")
        self.text_widget.tag_configure("next", background="lightblue")

    def initialize_all(self, clear_text = False):
        self.test_end = False
        self.test_start = False
        self.entry_widget.delete(0, "end")
        self.clear_text_widget()
        self.text_widget.tag_add("next", "1.0")
        self.match_end_index = 0
        self.wpm_value.set(0)
        self.average_value.set(self.get_average_speed("speed_records.txt"))
        if clear_text:
            self.text_widget.delete("1.0", "end")
        
    def set_callbacks(self):
        if not self.test_start:
            self.entry_widget.bind('<KeyPress>', self.set_start_time)
        self.entry_widget.bind('<KeyRelease>', self.handle_entry)
            
    def load_random_line(self):
        self.random_line = self.get_random_line("phrases.txt")
        self.text_widget.config(state = "normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", self.random_line)
        self.text_widget.config(state = "disabled")
        self.text_widget.tag_add("next", "1.0")
        
    def get_random_line(self, filename):
        with open(filename, "rt", encoding="utf-8") as text_file:
            random_line = next(text_file)
            for num, line in enumerate(text_file):
                if random.randrange(num + 2):
                    continue
                random_line = line
                
        return random_line
        
    def clear_text_widget(self):
        self.text_widget.tag_remove("correct", "1.0", "end")
        self.text_widget.tag_remove("wrong", "1.0", "end")
        self.text_widget.tag_remove("next", "1.0", "end")
        self.text_widget.configure(bg="white")

    def set_start_time(self,event):
        # Define start time: only if character is correct and is the first of entry widget text
        # Called on a one time key press event.
        if (event.char == self.random_line[0] and not self.entry_widget.get() and not self.test_start):
            self.start_time = event.time
            self.test_start = True

    def handle_entry(self, event):
        # Called on key release event
        #print(event.keycode)                       # keycodes change on different OS
        if event.keycode == 27:                     # Escape key event
            self.initialize_all(True)
            self.load_random_line()
        elif event.keycode == 9:                    # Tab key event
            self.initialize_all()
        elif event.char or (event.keycode == 8):    # Char or Backspace key event
            self.handle_text_widget(event)
        else:                                       # Shift key event, other.
            pass

    def handle_text_widget(self,event):
        if self.test_end:
            return None
        self.text_input = self.entry_widget.get()
        # Get len(not_matched_ chars) and len(matched_chars)
        not_matched, matched_chars = self.matcher(self.text_input, self.random_line)
        
        # Markers for tags
        self.text_widget.mark_set("matchEnd",    "1.{}".format(matched_chars))
        self.text_widget.mark_set("wrongStart",  "1.{}".format(matched_chars))
        self.text_widget.mark_set("wrongEnd",    "1.{}".format(len(self.text_input)))
        self.text_widget.mark_set("nextChar",    "1.{}".format(matched_chars))

        # Update tag: completely remove tag and insert new(w updated index)
        # Update tag: "next" char to input(light blue)
        self.text_widget.tag_remove("next", "1.0", "end")
        self.text_widget.tag_add("next", "nextChar")

        # Test finished successfully, save record to file, set all to correct.
        if matched_chars == (len(self.random_line)-1):
            self.write_record("speed_records.txt", self.wpm_value.get())
            self.clear_text_widget()
            self.text_widget.tag_add("correct", "1.0", "end")
            self.average_value.set(self.get_average_speed("speed_records.txt"))
            self.test_end = True

        # Tag correct characters (if any)
        if matched_chars >=0 and not self.test_end:
            # Remove "wrong" tag if any, and set text widget background to white
            self.text_widget.tag_remove("wrong", "1.0", "end")
            self.text_widget.configure(bg="white")

            # Update tag: correct characters so far
            self.text_widget.tag_remove("correct", "1.0", "end")
            self.text_widget.tag_add("correct", "1.0", "matchEnd")

            # Calculation for wpm
            if event.char and not not_matched and self.test_start:
                self.wpm_value.set(round((matched_chars)/(5*(event.time-self.start_time)/(1000*60)),2))
                
            # Tag incorrect characters
            if not_matched:
                # text widget background to pink
                self.text_widget.configure(bg="pink")

                # Don't tag next char to type
                self.text_widget.tag_remove("next", "1.0", "end")

                # Update tag: wrong characters after the correct ones.
                self.text_widget.tag_remove("wrong", "1.0", "end")
                self.text_widget.tag_add("wrong", "wrongStart", "wrongEnd")

    def matcher(self, string_a, string_b):
        """
        string_a : input string
        string_b : full string to match to
        return len(not_matched_chars, matched_chars)
        """
        
        if string_a == string_b[0:len(string_a)]:
            matched = len(string_a)
        else:
            matched = self.match_end_index
            for i,char in enumerate(string_a[self.match_end_index+1:len(string_a)]):
                if string_a[0:self.match_end_index+1+i] == string_b[0:self.match_end_index+1+i]:
                    matched += 1
                    
        not_matched = len(string_a)- matched
        self.match_end_index = matched
        
        return not_matched, matched

    def write_record(self, filename, wpm_value):
        with open(filename, "a") as record_file:
            record_file.write(str(wpm_value)+"\n")

    def get_average_speed(self, filename):
        average = 0
        count = 0
        with open(filename, "rt") as record_file:
            for value in record_file:
                average += float(value)
                count += 1
            average = average/count
        return round(average,2)
        
program = TypeTester()

program.window.mainloop()
