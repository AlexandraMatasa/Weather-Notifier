import customtkinter as ctk
from tkinter import messagebox
from src.storage.user_preferences import save_preferences
from src.validators.validation import Validator


def create_option_menu(parent_frame, label_text, variable, values, row):
    """
    Create an OptionMenu with a label in the provided frame.

    Args:
        parent_frame: The frame in which the OptionMenu and label should be placed.
        label_text (str): The text for the label.
        variable (tkinter variable): The variable to associate with the OptionMenu.
        values (list): The options for the OptionMenu.
        row (int): The row in the grid to place the widgets.
    """
    frame = ctk.CTkFrame(parent_frame)
    frame.grid(row=row, column=0, columnspan=2, pady=10, sticky="ew")
    frame.grid_columnconfigure(1, weight=1)

    label = ctk.CTkLabel(frame, text=label_text, anchor="w")
    label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    option_menu = ctk.CTkOptionMenu(frame, variable=variable, values=values)
    option_menu.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


def launch_gui(schedule_callback):
    """
    Launch the GUI to get user preferences for weather notifications.
    """

    def save_user_preferences():
        """
        Save the user's preferences when the Save button is clicked.
        """
        frequency = frequency_var.get()
        send_email = email_var.get() == 1  # If the checkbox is checked (1), send_email is set to True
        send_sms = sms_var.get() == 1  # If the checkbox is checked (1), send_sms is set to True
        to_email = email_entry.get()
        to_phone = phone_entry.get()
        city = city_entry.get()
        notification_preference = preference_var.get()

        if not city:
            messagebox.showwarning("Input Error", "Please enter a city.")
            return

        if send_email:
            if not to_email:
                messagebox.showwarning("Input Error", "Please enter an email address.")
                return
            if not Validator.validate_email(to_email):
                messagebox.showwarning("Invalid Email", "Please enter a valid email address.")
                return

        if send_sms:
            if not to_phone:
                messagebox.showwarning("Input Error", "Please enter a phone number.")
                return
            if not Validator.validate_phone(to_phone):
                messagebox.showwarning("Invalid Phone Number",
                                       "Please enter a valid phone number in the format +40756611781.")
                return

        if not send_email and not send_sms:
            messagebox.showwarning("Input Error", "Please select at least one notification method (Email or SMS).")
            return

        save_preferences(frequency, send_email, send_sms, to_email, to_phone, city, notification_preference)
        messagebox.showinfo("Preferences Saved", "Your preferences have been saved successfully!")

        from src.app import job
        job()

        schedule_callback()

        # Close the GUI window
        root.destroy()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.title("Weather Notifier")
    root.geometry("400x550")

    frequency_var = ctk.StringVar(value="daily")
    email_var = ctk.IntVar()
    sms_var = ctk.IntVar()
    preference_var = ctk.StringVar(value="full-weather")

    main_frame = ctk.CTkFrame(root)
    main_frame.pack(expand=True, fill='both', padx=20, pady=20)

    main_frame.grid_columnconfigure(0, weight=1)
    for i in range(6):
        main_frame.grid_rowconfigure(i, weight=1)

    # Notification frequency dropdown
    create_option_menu(main_frame, "Notification Frequency:", frequency_var, ["10 minutes", "hourly", "6 hours", "daily"], 0)

    # Notification preference dropdown
    create_option_menu(main_frame, "Notification Preference:", preference_var, ["umbrella-only", "full-weather"], 1)

    # Email settings
    email_frame = ctk.CTkFrame(main_frame)
    email_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
    email_frame.grid_columnconfigure(1, weight=1)

    email_check = ctk.CTkCheckBox(email_frame, text="Send email", variable=email_var)
    email_check.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    email_label = ctk.CTkLabel(email_frame, text="Email Address:", anchor="w")
    email_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    email_entry = ctk.CTkEntry(email_frame, width=200, placeholder_text="example@gmail.com")
    email_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # SMS settings
    sms_frame = ctk.CTkFrame(main_frame)
    sms_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")
    sms_frame.grid_columnconfigure(1, weight=1)

    sms_check = ctk.CTkCheckBox(sms_frame, text="Send SMS", variable=sms_var)
    sms_check.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    phone_label = ctk.CTkLabel(sms_frame, text="Phone Number:", anchor="w")
    phone_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    phone_entry = ctk.CTkEntry(sms_frame, width=200, placeholder_text="+40756611781")
    phone_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # City input
    city_frame = ctk.CTkFrame(main_frame)
    city_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")
    city_frame.grid_columnconfigure(1, weight=1)

    city_label = ctk.CTkLabel(city_frame, text="City:", anchor="w")
    city_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    city_entry = ctk.CTkEntry(city_frame, width=200)
    city_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    # Save button
    save_button = ctk.CTkButton(main_frame, text="Save Preferences", command=save_user_preferences, width=200)
    save_button.grid(row=5, column=0, columnspan=2, pady=20)

    # Start the GUI
    root.mainloop()


# Run the application
# launch_gui()
