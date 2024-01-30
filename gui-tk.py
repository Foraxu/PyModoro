from tkinter import Tk, Frame, Image, Label

root = Tk() # create a root window
root.title("PyModoro     by: Raposa")
root.config(bg='white')

main_frame = Frame(root, width=500, height=300, bg='red')
main_frame.grid(row=0, column=0, padx=2, pady=2)

Label(main_frame, text="Example Text").grid(row=1, column=0, padx=5, pady=5)


root.mainloop()
