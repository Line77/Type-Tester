from tkinter import *
from tkinter import ttk, font
from difflib import SequenceMatcher

class TypeTester:
    def __init__(self, master):
        self.master = master
        master.title("TypeTester")

        # Get test text, single line of a text file
        self.random_line = ""
        self.get_phrase("phrases.txt")

        # Define start time variable for pwm calculation
        self.start_time = 0

        # Font for all widgets
        self.all_font = font.Font(family = "Verdana", size ="11", weight = "bold")

        # Create text widget
        self.text_frame = Text(master, width=50, height=10, font=self.all_font, wrap="word",background = "yellow")
        self.text_frame.insert("1.0", self.random_line)

        # Define text tags, each one modifies text to show current state
        self.text_frame.tag_configure("correct", foreground="gray")
        self.text_frame.tag_configure("wrong", foreground="red")
        self.text_frame.tag_configure("next", background="lightblue")

        # Create text entry widget
        self.text_input = StringVar()
        self.entry_frame = ttk.Entry(master, width=50, font = self.all_font)

        # Create label widget to show WPM
        self.wpm = DoubleVar()
        self.wpm_title = Label(master, font= self.all_font, text = "WPM", anchor = "ne")    #, background = "blue")
        self.wpm_number = Label(master, font= self.all_font, textvariable= self.wpm, anchor = "nw",width = 7)#,background = "orange")
        
        # Arrange widgets, layout
        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(0, weight=1)
        self.text_frame.grid(column=0, row=1, columnspan=2, sticky = "ew")
        self.entry_frame.grid(column=0, row=0, columnspan=2, sticky = "new")
        self.wpm_title.grid(column=0, row=3, sticky = "nsew")
        self.wpm_number.grid(column=1, row=3, sticky = "nsew")

        
        # Focus text entry box on start
        self.entry_frame.focus()
        # Call text update method each time a key is released, event object is passed
        self.entry_frame.bind('<KeyRelease>', self.read_entry)
        
    def get_phrase(self, filename):
        """
        Gets "random" line from a text
        """
        with open(filename, "rt",encoding='utf-8') as text_file:
            self.random_line = text_file.readline()

    def read_entry(self, event):
        """
        Gets text from entry widget and compares with test text
        """
        # Gets text on entry widget
        self.text_input = self.entry_frame.get()

        # seq contains: seq.a= len(not-matched characters), seq.size=len(matched chars)
        seq = SequenceMatcher(None,self.text_input,self.random_line).find_longest_match(0,len(self.text_input),0,len(self.random_line))

        # Markers for tags
        self.text_frame.mark_set("matchEnd",    "1.{}".format(seq.size))
        self.text_frame.mark_set("wrongStart",  "1.{}".format(seq.size))
        self.text_frame.mark_set("wrongEnd",    "1.{}".format(len(self.text_input)))
        self.text_frame.mark_set("nextChar",    "1.{}".format(seq.size))

        # Update tag: completely remove tag and insert new(w updated index)
        # Update tag: "next" char to input(light blue)
        self.text_frame.tag_remove("next", "1.0", "end")
        self.text_frame.tag_add("next", "nextChar")

        # Define start time: only if character is correct and is the first of entry widget text
        # != "" by-passes shift and other key presses, this way "start_time" is defined when
        # the first correct character key is released
        # Catch index out of range error
        try:
            if ((event.char != "") and (seq .a == 0) and
                    (self.text_input is self.text_input[0]) and
                    (self.text_input[0] == self.random_line[0])):
                self.start_time = event.time
        except:
            pass

        # Char is correct: no wrong chars on start, text is the same so far.
        if seq.a == 0 and self.text_input == self.random_line[0:seq.size]:
            # Remove "wrong" tag if any, and set text widget background to white
            self.text_frame.tag_remove("wrong", "1.0", "end")
            self.text_frame.configure(bg="white")

            # Update tag: good characters so far(gray)
            self.text_frame.tag_remove("correct", "1.0", "end")
            self.text_frame.tag_add("correct", "1.0", "matchEnd")

            # Calculation for wpm, catch ZeroDivisionError
            try:
                self.wpm.set(round((seq.size)/(5*(event.time-self.start_time)/(1000*60)),2))
            except:
                pass
        # Char is/are wrong: at start(or after text) doesn't match, or
        # characters matched to (seq.size) then didn't anymore
        if seq.a >0 or seq.b>0 or (seq.size != len(self.text_input)):
            # text widget background to pink
            self.text_frame.configure(bg="pink")

            # Don't tag next char to type
            self.text_frame.tag_remove("next", "1.0", "end")
            if seq.size < len(self.text_input):
                if seq.a == 0 and self.text_input[0:seq.size] == self.random_line[0:seq.size]:
                    # Hard-coded
                    # If a key is pressed but not released immediately, more than one character will be 
                    # present on entry box, but only one call to this method will be executed.
                    # If this key is a correct input, it will not have a "correct tag",
                    # will be black instead of gray.
                    # This extra if statement fix that.
                    self.text_frame.tag_remove("correct", "1.0", "end")
                    self.text_frame.tag_add("correct", "1.0", "1.{}".format(seq.size+1))

                # Update tag: wrong characters after the correct ones.
                self.text_frame.tag_remove("wrong", "1.0", "end")
                self.text_frame.tag_add("wrong", "wrongStart", "wrongEnd")


root = Tk()
my_gui = TypeTester(root)
root.mainloop()
