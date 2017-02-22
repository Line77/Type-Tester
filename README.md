# Type-Tester
  I'm a self-taught programmer and this is my first project.
  After using https://www.keyhero.com a lot, I wanted to customize a few things on their typing test.
  With that idea on my head, I decided to make my own typing test, and put to practice my python skills.
  
  I used tkinter to define a text box to show a quote, and an entry box to type each character of the quote.
  Also, there are two label widgets to show the current typing speed.
  
  Every time a key is pressed(released actually) a routine is called, wich gets a key release event and stores
  the current string on the entry box on a variable. Then a comparation is performed, between the content of both
  entry and text widgets.
  
  By default the next character to type is modified by a next tkinter tag (light blue foreground)
  Acording to the result of previous comparation, text will be modified with different tkinter tags, text could be correct(gray),
  wrong(red). Also background of thext is changed in both cases.
  

  
