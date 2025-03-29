import os

# Here define your project structure
project_structure = {
    "app": [
        "__init__.py",
        "main.py",
        "dependencies.py",
        "routers/__init__.py",
        "routers/items.py",
        "routers/users.py",
        "crud/__init__.py",
        "crud/item.py",
        "crud/user.py",
        "schemas/__init__.py",
        "schemas/item.py",
        "schemas/user.py",
        "models/__init__.py",
        "models/item.py",
        "models/user.py",
        "external_services/__init__.py",
        "external_services/email.py",
        "external_services/notification.py",
        "utils/__init__.py",
        "utils/authentication.py",
        "utils/validation.py",
    ],
    "tests": [
        "__init__.py",
        "test_main.py",
        "test_items.py",
        "test_users.py",
    ],
}

# Here define the project level files
project_files = ["requirements.txt", ".gitignore", "README.md"]

def create_project_structure(base_path="FastAPI_Project"):
    os.makedirs(base_path, exist_ok=True)

    for folder, files in project_structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        for file in files:
            file_path = os.path.join(base_path, file)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")

    for file in project_files:
        file_path = os.path.join(base_path, file)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write("")

    print(f"FastAPI project structure created successfully in '{base_path}'!")


# Run the script
if __name__ == "__main__":
    create_project_structure()
