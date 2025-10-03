import tkinter as tk
import getpass
import socket

from Tools.demo.hanoi import Tkhanoi


def get_shell_prompt_header():
    username = getpass.getuser()
    hostname = socket.gethostname()
    return f"Эмулятор - [{username}@{hostname}]"


def parse_input(user_input):
    tokens = user_input.split()
    if not tokens:
        return "", []
    command = tokens[0]
    args = tokens[1:]
    return command, args


SUPPORTED_COMMANDS = {"ls", "cd", "exit"}


def execute_command(command, args):
    if not command:
        return ""

    if command not in SUPPORTED_COMMANDS:
        return f"shell: {command}: command not found"

    if command == "exit":
        return "exit"

    return f"вызвана команда: {command}: аргументы: {args}"


class ShellEmulator:
    def __init__(self, root):
        self.root = root
        self.root.title(get_shell_prompt_header())
        self.root.geometry("700x500")

        self.text_area = tk.Text(root, wrap=tk.WORD, state='disabled', bg='black', fg='white', font=('Courier', 10))
        self.text_area.pack(expand=True, fill='both', padx=3, pady=3)

        self.entry = tk.Entry(root, font=('Courier', 10))
        self.entry.pack(fill='x', padx=5, pady=(0, 5))
        self.entry.bind("<Return>", self.on_enter)
        self.entry.focus()

        self.print_output(get_shell_prompt_header() + "\n")
        self.print_prompt()

    def print_output(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert('end', text)
        self.text_area.config(state='disabled')
        self.text_area.see('end')

    def print_prompt(self):
        username = getpass.getuser()
        hostname = socket.gethostname()
        prompt = f"{username}@{hostname}:~$ "
        self.print_output(prompt)

    def on_enter(self, event):
        user_input = self.entry.get()
        self.entry.delete(0, tk.END)

        self.print_output(user_input + '\n')

        command, args = parse_input(user_input)
        result = execute_command(command, args)

        if result == "exit":
            self.print_output("Выход...\n")
            self.root.after(1000, self.root.destroy)
        elif result:
            self.print_output(result + "\n")

        if result != "exit":
            self.print_prompt()


if __name__ == "__main__":
    root = tk.Tk()
    app = ShellEmulator(root)
    root.mainloop()
