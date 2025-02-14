import openpyxl
from tkinter import *
from tkinter import messagebox
import os  # operating system
from datetime import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from fpdf import FPDF

chatbot = ChatBot('BankBot')
trainer = ListTrainer(chatbot)

trainer.train([
    "How to check balance?",
    "Check your balance in net banking",

    "Apply for Loan?",
    "Send a mail to support@loan department",

    "Open new savings account?",
    "Please fill out the registration form to open a new savings account",

    "Close your account?",
    "Visit our nearest branch to close your account",
])

def register_and_generate_pdf(question, user_data):
    save_to_pdf(question, user_data)

def registration_form(question):
    form_window = Toplevel()
    form_window.title(question)
    form_window.geometry('300x350')  # Adjusted for extra fields if needed

    if question == "How to check balance?":
        account_number_label = Label(form_window, text="Account Number:")
        account_number_label.pack()
        account_number_entry = Entry(form_window)
        account_number_entry.pack()

        mobile_number_label = Label(form_window, text="Mobile Number:")
        mobile_number_label.pack()
        mobile_number_entry = Entry(form_window)
        mobile_number_entry.pack()

        def submit_balance_form():
            account_number = account_number_entry.get()
            mobile_number = mobile_number_entry.get()
            user_data = [account_number, mobile_number]

            register_and_generate_pdf(question, user_data)

            form_window.destroy()

            response = chatbot.get_response(question)
            print(f"BankBot: {response}")

        submit_button = Button(form_window, text="Submit", command=submit_balance_form)
        submit_button.pack()

    else:
        first_name_label = Label(form_window, text="First Name:")
        first_name_label.pack()
        first_name_entry = Entry(form_window)
        first_name_entry.pack()

        last_name_label = Label(form_window, text="Last Name:")
        last_name_label.pack()
        last_name_entry = Entry(form_window)
        last_name_entry.pack()

        email_label = Label(form_window, text="Email:")
        email_label.pack()
        email_entry = Entry(form_window)
        email_entry.pack()

        mobile_label = Label(form_window, text="Mobile:")
        mobile_label.pack()
        mobile_entry = Entry(form_window)
        mobile_entry.pack()

        def submit_form():
            user_data = [
                first_name_entry.get(),
                last_name_entry.get(),
                email_entry.get(),
                mobile_entry.get()
            ]

            register_and_generate_pdf(question, user_data)

            form_window.destroy()

            response = chatbot.get_response(question)
            print(f"BankBot: {response}")

        submit_button = Button(form_window, text="Submit", command=submit_form)
        submit_button.pack()

def save_to_pdf(question, user_data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"bank_{timestamp}.pdf"

    if os.path.exists(pdf_filename):
        os.remove(pdf_filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt="BankBot Inquiry Log", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.multi_cell(0, 10, f"Q: {question}")
    response = chatbot.get_response(question)
    pdf.multi_cell(0, 10, f"A: {response}")

    pdf.ln(4)  # Line break
    pdf.multi_cell(0, 10, f"User Data Submitted:")
    if question == "How to check balance?":
        pdf.multi_cell(0, 10, f"Account Number: {user_data[0]}")
        pdf.multi_cell(0, 10, f"Mobile Number: {user_data[1]}")
    else:
        pdf.multi_cell(0, 10, f"First Name: {user_data[0]}")
        pdf.multi_cell(0, 10, f"Last Name: {user_data[1]}")
        pdf.multi_cell(0, 10, f"Email: {user_data[2]}")
        pdf.multi_cell(0, 10, f"Mobile: {user_data[3]}")

    pdf.output(pdf_filename)
    print(f"PDF Generated: {pdf_filename}")

def main_gui():
    root = Tk()
    root.title("BankBot - Select a Question")
    root.geometry('400x400')

    questions = [
        "How to check balance?",
        "Apply for Loan?",
        "Open new savings account?",
        "Close your account?"
    ]
    def open_form(question):
        registration_form(question)

    for question in questions:
        button = Button(root, text=question, width=30, command=lambda q=question: open_form(q))
        button.pack(pady=10)
    root.mainloop()
main_gui()  # for GUI
