"""
Todo CLI Interface

This module provides the menu-driven console interface for the todo application.
"""
from typing import Optional
from .services import TodoService


class TodoCLI:
    """
    Menu-driven console interface for the todo application.
    Implements a loop-based interface with numbered options.
    """

    def __init__(self):
        """Initialize the CLI with a todo service."""
        self.service = TodoService()

    def display_menu(self):
        """Display the main menu options."""
        print("\nTodo Application Menu:")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Completion")
        print("6. Exit")

    def get_user_choice(self) -> str:
        """
        Get user's menu choice.

        Returns:
            The user's choice as a string
        """
        try:
            choice = input("Choose an option: ").strip()
            return choice
        except (EOFError, KeyboardInterrupt):
            print("\nApplication interrupted. Exiting...")
            return "6"  # Return exit option

    def run(self):
        """Run the main application loop."""
        print("Welcome to the Todo Application!")
        while True:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.handle_add_task()
            elif choice == "2":
                self.handle_view_tasks()
            elif choice == "3":
                self.handle_update_task()
            elif choice == "4":
                self.handle_delete_task()
            elif choice == "5":
                self.handle_toggle_task()
            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-6.")

    def handle_add_task(self):
        """Handle the add task functionality."""
        print("\n--- Add New Task ---")
        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Task title cannot be empty.")
                return

            description_input = input("Enter task description (optional, press Enter to skip): ").strip()
            description = description_input if description_input else None

            task = self.service.add_task(title, description)
            print(f"Task added successfully with ID {task.id}!")
        except ValueError as e:
            print(f"Error: {e}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return

    def handle_view_tasks(self):
        """Handle the view tasks functionality."""
        print("\n--- All Tasks ---")
        tasks = self.service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            status = "Completed" if task.completed else "Incomplete"
            description = task.description if task.description else "No description"
            print(f"ID: {task.id}, Title: {task.title}, Description: {description}, Status: {status}")

    def handle_update_task(self):
        """Handle the update task functionality."""
        print("\n--- Update Task ---")
        try:
            task_id_input = input("Enter task ID to update (or 'cancel' to abort): ").strip()
            if task_id_input.lower() == 'cancel':
                print("Update operation cancelled.")
                return

            task_id = int(task_id_input)
            task = self.service.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            print(f"Current title: {task.title}")
            new_title = input("Enter new title (or press Enter to keep current): ").strip()
            if new_title == "":
                new_title = task.title

            if not new_title:
                print("Task title cannot be empty.")
                return

            print(f"Current description: {task.description or 'No description'}")
            new_description_input = input("Enter new description (or press Enter to keep current): ").strip()
            if new_description_input == "":
                new_description = task.description
            else:
                new_description = new_description_input if new_description_input else None

            updated_task = self.service.update_task(task_id, new_title, new_description)
            if updated_task:
                print(f"Task {task_id} updated successfully!")
            else:
                print(f"Failed to update task {task_id}.")

        except ValueError:
            print("Invalid task ID. Please enter a number or 'cancel'.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return

    def handle_delete_task(self):
        """Handle the delete task functionality."""
        print("\n--- Delete Task ---")
        try:
            task_id = int(input("Enter task ID to delete: "))
            task = self.service.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            confirm = input(f"Are you sure you want to delete task '{task.title}'? (yes/no): ").strip().lower()
            if confirm in ['yes', 'y']:
                if self.service.delete_task(task_id):
                    print(f"Task {task_id} deleted successfully!")
                else:
                    print(f"Failed to delete task {task_id}.")
            else:
                print("Delete operation cancelled.")

        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return

    def handle_toggle_task(self):
        """Handle the toggle task completion functionality."""
        print("\n--- Toggle Task Completion ---")
        try:
            task_id = int(input("Enter task ID to toggle: "))
            task = self.service.get_task(task_id)
            if not task:
                print(f"Task with ID {task_id} not found.")
                return

            toggled_task = self.service.toggle_task_completion(task_id)
            if toggled_task:
                status = "completed" if toggled_task.completed else "incomplete"
                print(f"Task {task_id} is now {status}!")
            else:
                print(f"Failed to toggle task {task_id}.")

        except ValueError:
            print("Invalid task ID. Please enter a number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")
            return