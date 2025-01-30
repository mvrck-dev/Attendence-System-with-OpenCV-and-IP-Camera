def capture_photos(camera_type):
    ID_NAMES_FILE = 'id-names.csv'

    # Create the file and directory if they don't exist
    if not os.path.exists(ID_NAMES_FILE):
        id_names = pd.DataFrame(columns=['id', 'name'])
        id_names.to_csv(ID_NAMES_FILE, index=False)
    else:
        id_names = pd.read_csv(ID_NAMES_FILE)

    if not os.path.exists('faces'):
        os.makedirs('faces')

    print('Welcome!')
    print('\nPlease put in your ID.')
    print('If this is your first time choose a random ID between 1-10000')

    id = int(input('ID: '))
    name = ''

    if id in id_names['id'].values:
        name = id_names[id_names['id'] == id]['name'].item()
        print(f'Welcome Back {name}!!')
    else:
        name = input('Enter your name: ')
        new_entry = pd.DataFrame([{'id': id, 'name': name}])
        id_names = pd.concat([id_names, new_entry], ignore_index=True)
        os.makedirs(f'faces/{id}', exist_ok=True)
        id_names.to_csv(ID_NAMES_FILE, index=False)

    print("\nLet's capture!")
    print("Now this is where you begin taking photos. Once you see a rectangle around your face, press the 's' key to capture a picture.", end=" ")
    print("It is recommended to take at least 20-25 pictures, from different angles, in different poses, with and without specs.")
    input("\nPress ENTER to start when you're ready, and press the 'q' key to quit when you're done!")

    # Use the selected camera type
    if camera_type == "Laptop":
        start_laptop_camera(id)
    elif camera_type == "IP Camera":
        start_ip_camera(id)

# Modify `open_menu` to pass the selection
def open_menu():
    root = tk.Tk()
    root.title("Camera Selection Menu")
    root.geometry("300x200")

    def on_select_camera_type(camera_type):
        root.destroy()  # Close the menu before starting camera
        capture_photos(camera_type)  # Pass the selected camera type

    label = tk.Label(root, text="Choose Camera Type", font=('Helvetica', 14))
    label.pack(pady=20)

    laptop_button = tk.Button(root, text="Laptop Camera", width=20, command=lambda: on_select_camera_type("Laptop"))
    laptop_button.pack(pady=10)

    ip_camera_button = tk.Button(root, text="IP Camera", width=20, command=lambda: on_select_camera_type("IP Camera"))
    ip_camera_button.pack(pady=10)

    root.mainloop()
