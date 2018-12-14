from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk,Image
import tkinter as tk
import predict
import nutrition_facts
import numpy as np
# Here, we are creating our class, Window, and inheriting from the Frame
# class. Frame is a class from the tkinter module. (see Lib/tkinter/__init__)

FILES = ()
PATHS = []

class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):

        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        #reference to the master widget, which is the tk window
        self.master = master
        #self.files = []
        self.images = []
        self.nutrition_vals = None

        #with that, we want to then run init_window, which doesn't yet exist
        self.init_window()


    #Creation of init_window
    def init_window(self):

        # changing the title of our master widget
        self.master.title("AI Project - Nutrition Advisor")

        # allowing the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)

        # creating a button instance
        exitButton = Button(self, text="Exit",command=self.exitGUI, width = 10, borderwidth = 2)
        classifyButton = Button(self, text = "Classify", command=self.CNN, width = 10, borderwidth = 2)
        fileSelection = Button(self, text="Select File", command=self.selectFiles, width = 10, borderwidth = 2)
        nutritionButton = Button(self, text = "Nutrition", command = self.nutrition, width = 10, borderwidth = 2)

        # placing the button on my window
        exitButton.place(x=300, y=0)
        classifyButton.place(x=100, y=0)
        fileSelection.place(x=0, y=0)
        nutritionButton.place(x = 200, y = 0)

    def selectFiles(self):
        global FILES, PATHS
        FILES = filedialog.askopenfilenames()

        for file in FILES:
            PATHS.append(file)

        print("files = " + str(FILES))
        print("paths = " + str(PATHS))


        for path in FILES:
            #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
            img = Image.open(path)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.images.append(img)

        panels = []
        for im in self.images:
            #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
            panels.append(tk.Label(image = im))

        x_c = 50
        y_c = 50
        for panel in panels:
            #The Pack geometry manager packs widgets in rows or columns.
            panel.pack()
            #The location of where the image is placed.
            panel.place(x = x_c, y = y_c)
            if(x_c > 900):
                x_c = 50
                y_c += 300
            else:
                x_c += 250





        # self.files = filedialog.askopenfilenames()
        # print(self.files)

    def exitGUI(self):
        print("Exiting Now")
        exit()

    def CNN(self):
        print("Running the CNN model")

        """
        TODO:// When this function is called, we want to be able to show the food photos here
        """
        global PATHS
        results = predict.predict_classes(PATHS)
        total_diet = np.zeros((6))
        suggested_diet = np.array(food_facts['suggested'])
        x_c = 60
        y_c = 255
        for result in results:
            nut_vals = np.array(food_facts[result])
            total_diet = total_diet + nut_vals
            text_label = tk.Label(text=result)
            text_label.pack(side="bottom", fill="both", expand="yes")
            text_label.place(x=x_c, y=y_c)
            if(x_c > 900):
                x_c = 50
                y_c += 300
            else:
                x_c += 250
        output_vals = np.divide(total_diet, suggested_diet)
        # scaled has what % of a suggested diet you've achieved
        # [calories, fat, cholesterol, sodium, carbs, protein]
        scaled = np.round(output_vals * 100, decimals=1)
        self.nutrition_vals = scaled


    def nutrition(self):
        list_of_vals = self.nutrition_vals.tolist()
        messagebox.showinfo("Nutrition Facts", "Here's how much of the daily values you have already consumed if you" +
        " had one serving of each item: \n\nCalories: " + str(list_of_vals[0]) + "%\nFat: " + str(list_of_vals[1]) + "%\nCholesterol: " 
        + str(list_of_vals[2]) + "%\nSodium: " + str(list_of_vals[3]) + "%\nCarbohydrates: " + str(list_of_vals[4])
         + "%\nProtein: " + str(list_of_vals[5]) + "%")





# root window created. Here, that would be the only window, but
# you can later have windows within windows.
root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
nutrition_facts.main()
food_facts = nutrition_facts.Food.food_facts
#creation of an instance
app = Window(root)

#mainloop
root.mainloop()
