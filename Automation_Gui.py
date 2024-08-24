import tkinter as tk
from tkinter import filedialog, messagebox
import main
import threading


class AutomationGUI:
    def __init__(self, master):
        self.master = master
        master.title("Automatisation de navigation web")

        self.link_labels = []
        self.link_entries = []
        self.max_interval_label = None
        self.max_interval_entry = None
        self.min_duration_label = None
        self.min_duration_entry = None
        self.max_duration_label = None
        self.max_duration_entry = None
        self.log_directory_label = None
        self.log_directory_entry = None
        self.log_directory_button = None
        self.start_button = None
        self.stop_button = None

        self.automation_thread = None
        self.stop_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        for i in range(10):
            # Centrer la fenêtre sur l'écran
            window_width = 650
            window_height = 600
            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()
            x = (screen_width // 2) - (window_width // 2)
            y = (screen_height // 2) - (window_height // 2)
            self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

            link_label = tk.Label(self.master, text=f"      Lien {i+1}:", anchor="w")
            link_label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            link_entry = tk.Entry(self.master, width=40)
            link_entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.link_labels.append(link_label)
            self.link_entries.append(link_entry)

        self.max_interval_label = tk.Label(self.master, text="Intervalle d'ouverture maximum (minutes):")
        self.max_interval_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.max_interval_entry = tk.Entry(self.master)
        self.max_interval_entry.grid(row=10, column=1, padx=5, pady=5, sticky="w")

        self.min_duration_label = tk.Label(self.master, text="Durée d'ouverture minimum (minutes):")
        self.min_duration_label.grid(row=11, column=0, padx=5, pady=5, sticky="w")
        self.min_duration_entry = tk.Entry(self.master)
        self.min_duration_entry.grid(row=11, column=1, padx=5, pady=5, sticky="w")

        self.max_duration_label = tk.Label(self.master, text="Durée d'ouverture maximum (minutes):")
        self.max_duration_label.grid(row=12, column=0, padx=5, pady=5, sticky="w")
        self.max_duration_entry = tk.Entry(self.master)
        self.max_duration_entry.grid(row=12, column=1, padx=5, pady=5, sticky="w")

        instructions_label = tk.Label(self.master, text="Exemple: 24 heures == 1440 minutes")
        instructions_label.grid(row=13, column=0, columnspan=3, padx=5, pady=5)

        self.log_directory_label = tk.Label(self.master, text="                 Dossier des logs:")
        self.log_directory_label.grid(row=14, column=0, padx=0, pady=5, sticky="w")
        self.log_directory_entry = tk.Entry(self.master, width=40)
        self.log_directory_entry.grid(row=14, column=1, padx=0, pady=5, sticky="w")
        self.log_directory_button = tk.Button(self.master, text="Parcourir", command=self.select_log_directory)
        self.log_directory_button.grid(row=14, column=2, padx=0, pady=5, sticky="e")

        self.start_button = tk.Button(self.master, width=15, bg="lightgreen", text="Démarrer", command=self.start_automation)
        self.start_button.grid(row=15, column=0, padx=5, pady=5, sticky="e")
        self.stop_button = tk.Button(self.master, width=15, bg="red", text="Arrêter", command=self.stop_automation)
        self.stop_button.grid(row=15, column=1, padx=5, pady=5, sticky="e")

    def select_log_directory(self):
        log_directory = filedialog.askdirectory(initialdir="~/Downloads")
        self.log_directory_entry.delete(0, tk.END)
        self.log_directory_entry.insert(0, log_directory)

    def start_automation(self):
        if self.automation_thread and self.automation_thread.is_alive():
            messagebox.showerror("Erreur", "L'automatisation est déjà en cours.")
            return

        links = [entry.get() for entry in self.link_entries if entry.get()]
        if not links:
            messagebox.showerror("Erreur", "Veuillez entrer au moins un lien.")
            return

        valid_links = []        # a regarder pourqoui les lien pas correct ne devienne pas rouge et ne sont pas pris en compte
        invalid_links = []
        for i, link in enumerate(links):
            if not main.is_valid_url(link):
                self.link_entries[i].config(bg="red")
                invalid_links.append(link)
            else:
                self.link_entries[i].config(bg="white")
                valid_links.append(link)

        if invalid_links:
            messagebox.showerror("Erreur", "Un ou plusieurs liens sont invalides. Veuillez vérifier les liens en rouge.")

        if not valid_links:
            return

        if not self.max_interval_entry.get():
            messagebox.showerror("Erreur", "Veuillez spécifier un intervalle d'ouverture maximum.")
            return

        if not self.min_duration_entry.get():
            messagebox.showerror("Erreur", "Veuillez spécifier une durée d'ouverture minimum.")
            return

        if not self.max_duration_entry.get():
            messagebox.showerror("Erreur", "Veuillez spécifier une durée d'ouverture maximum.")
            return

        try:
            max_interval = int(self.max_interval_entry.get()) if self.max_interval_entry.get() else 2
        except ValueError:
            messagebox.showerror("Erreur", "L'intervalle d'ouverture maximum doit être un nombre entier.")
            return

        try:
            min_duration = int(self.min_duration_entry.get()) if self.min_duration_entry.get() else 1
        except ValueError:
            messagebox.showerror("Erreur", "La durée d'ouverture minimum doit être un nombre entier.")
            return

        try:
            max_duration = int(self.max_duration_entry.get()) if self.max_duration_entry.get() else 1
        except ValueError:
            messagebox.showerror("Erreur", "La durée d'ouverture maximum doit être un nombre entier.")
            return

        log_directory = self.log_directory_entry.get()

        if not log_directory:
            messagebox.showerror("Erreur", "Veuillez spécifier un dossier pour les logs.")
            return

        self.stop_event.clear()
        self.automation_thread = threading.Thread(target=main.start_automation,
                                                  args=(valid_links, max_interval, min_duration, max_duration,
                                                        log_directory, self.stop_event))
        self.automation_thread.start()

    def stop_automation(self):
        if not self.automation_thread or not self.automation_thread.is_alive():
            messagebox.showerror("Erreur", "L'automatisation n'est pas en cours.")
            return

        if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir arrêter l'automatisation?"):
            self.stop_event.set()
            self.automation_thread.join()


root = tk.Tk()
app = AutomationGUI(root)
root.mainloop()
