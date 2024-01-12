import pandas as pd
import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkFont
'''
from android.permissions import Permission, request_permissions, check_permission

def check_permissions(perms):
    for perm in perms:
        if check_permission(perm) != True:
            return False
    return True

perms = [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
    
if  check_permissions(perms)!= True:
    request_permissions(perms)
'''
class FlashcardApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Flashcards")
        self.master.geometry('800x600')
        #self.master.config(bg='lightblue')

        #startmenu
        self.start_frame = tk.Frame(master)
        self.start_frame.pack(fill = 'both',expand = True)
       

        start_text = tk.Label(self.start_frame, text = "Bienvenido a FLASHCARDS\n\n\nDesarrollado por Marc Roig i Samuel Ortega\n\nIdea original de Samuel Ortega",
                              font = ('Helvetica', 20, 'bold'))
        start_text.pack(pady = 20)

        self.quiz_frame = tk.Frame(master)
        start_button = tk.Button(self.start_frame, text = 'INICIO', font = ('Arial', 15), command = self.OnStart)
        start_button.pack()

        

        #self.load_csv_file()

        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        answers_font = tkFont.Font(family="Helvetica", size=12, weight="bold")
        questions_font = tkFont.Font(family='Arial', size = 12, weight='bold')

        self.question_counter_label = tk.Label(self.quiz_frame, text="")
        self.question_counter_label.pack()

        self.question_label = tk.Label(self.quiz_frame , text="",font=questions_font,wraplength=780, justify='left', anchor='w')
        self.question_label.pack()

        self.next_button = tk.Button(self.quiz_frame, text="Siguiente", command=self.next_question)
        self.next_button.pack()

        answer_frame = tk.Frame(self.quiz_frame)
        answer_frame.pack(pady = 10)

        self.answer_button_design = {
            'bg': '#4CAF50',
            'fg': 'white',
            'font': answers_font,
            'borderwidth': 2,
            'relief': 'raised',
            'wraplength' : 780,
        }


        self.option_buttons = []
        for i in range(4):
            button = tk.Button(answer_frame, text="",**self.answer_button_design,command=lambda i=i: self.check_answer(i))
            button.grid(row = i, column = 0, padx = 10, pady = 5, sticky = 'ew')
            self.option_buttons.append(button)
            
        
        #Colocacion de objetos
        result_label_frame = tk.Frame(self.quiz_frame)
        result_label_frame.pack()
        
        button_frame = tk.Frame(self.quiz_frame)
        button_frame.pack()


        self.score_label = tk.Label(self.quiz_frame, text=f"{self.correct_answers} Aciertos\n{self.wrong_answers} Fallos", font = ('Helvetica', 16, 'bold'))
        self.score_label.pack()

        self.result_label = tk.Label(result_label_frame, text="", width = 100, height =2, font = ('Helvetica', 15))
        self.result_label.pack( padx = 5)


        self.restart_button = tk.Button(button_frame, text="Restart", command=self.restart_quiz, width = 10, height = 2)
        self.restart_button.pack(side = tk.LEFT, padx=5)

        # Exit button
        self.exit_button = tk.Button(button_frame, text="Exit", command=master.destroy, width = 10, height = 2)
        self.exit_button.pack(side = tk.LEFT, padx = 5)



        #Test para colocar cada boton en su sitio
        #self.mouse_coords_label = tk.Label(master, text='Coordenadas: ')
        #self.mouse_coords_label.pack()
        #master.bind('<Motion>', self.updateCoords)



        if hasattr(self, 'df'):
            self.randomize_questions()
            self.update_question()

    
    def OnStart(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack(fill = 'both', expand = True)
        self.load_csv_file()
        self.restart_quiz()


    def updateCoords(self, event): #Funcion de prueba no tocar y no se ejecuta
        coords = f'Coordendas: x={event.x}, y={event.y}'
        self.mouse_coords_label.config(text = coords) 


    def load_csv_file(self):
        file_path = filedialog.askopenfilename(title="Carga el CSV", filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.df = pd.read_csv(file_path)

    def randomize_questions(self):
        self.df = self.df.sample(frac=1).reset_index(drop=True)

    def update_question(self):
        self.question_counter_label.config(text=f"Question {self.current_question + 1} of {len(self.df)}")
        question = self.df.iloc[self.current_question]
        self.question_label.config(text=question['Question'], wraplength=780, justify='left', anchor='w')
        for i, button in enumerate(self.option_buttons):
            button.config(text=question[f'Option{i + 1}'], state=tk.NORMAL, bg='grey', wraplength=780)
    
    def restart_quiz(self):
        # Reset the quiz
        self.current_question = 0
        self.correct_answers = 0
        self.wrong_answers = 0
        self.score_label.config(text=f"{self.correct_answers} Aciertos\n{self.wrong_answers} Fallos")
        self.result_label.config(text="")
        self.randomize_questions()
        self.update_question()

        # Re-enable and reset buttons
        for button in self.option_buttons:
            button.config(state=tk.NORMAL, bg='grey')

    def check_answer(self, selected_option):
        for button in self.option_buttons:
            button.config(state=tk.DISABLED)

        correct_option = self.df.iloc[self.current_question]['CorrectAnswer'] - 1
        if selected_option == correct_option:
            self.result_label.config(text="Resulta que no eres tan retrasado como pareces, bien hecho por ahora")
            self.option_buttons[selected_option].config(bg='lime green')
            self.correct_answers += 1
            self.score_label.config(text=f"{self.correct_answers} Aciertos\n{self.wrong_answers} Fallos")
        else:
            #self.option_buttons[correct_option].config(bg='green')
            self.result_label.config(text=f"Te jodes gilipollas, la respuesta correcta era la opcion {int(correct_option) + 1}")
            self.wrong_answers += 1
            self.option_buttons[selected_option].config(bg='firebrick2')
            self.score_label.config(text=f"{self.correct_answers} Aciertos\n{self.wrong_answers} Fallos")
            self.option_buttons[correct_option].config(bg='lime green')
            

    def next_question(self):
        if self.current_question < len(self.df) - 1:
            self.current_question += 1
            self.update_question()
            self.score_label.config(text=f"{self.correct_answers} Aciertos\n{self.wrong_answers} Fallos")
            self.result_label.config(text = ' ')
        else:
            if self.correct_answers > (self.correct_answers + self.wrong_answers) / 2 :
                self.result_label.config(text=f"Has acertado {self.correct_answers} de {self.correct_answers + self.wrong_answers} estas aprobado")
            else:
                self.result_label.config(text=f"Has acertado {self.correct_answers} de {self.correct_answers + self.wrong_answers} eres mas tonto que el Subi")

root = tk.Tk()
app = FlashcardApp(root)
root.mainloop()
