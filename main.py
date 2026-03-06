from yaspin import yaspin
import psycopg2
import time
import os
from dotenv import load_dotenv


load_dotenv()

def anim(text: str):
	for char in text:
		time.sleep(0.05)
		print(char, end="")
	print()
	
def anim_with_input(text: str):
	for char in text:
		time.sleep(0.05)
		print(char, end="", flush=True)
	return input()
		
	
def loading_anim():
	spinner = yaspin(color="white")
	spinner.start()
	time.sleep(3)
	spinner.stop()
	
def clear_terminal():
	os.system('cls' if os.name == 'nt' else 'clear')
	time.sleep(1)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def press_any_key_to_continue():
	anim_with_input("Press any key to continue...")

def show_all_tasks():
	clear_terminal()
	loading_anim()
	with get_connection() as conn:
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM tasks")
			rows = cursor.fetchall()

			if not rows:
				anim("You don't have any tasks yet!")
			else:
				for row in rows:
					completed = "x" if row[2] else " "
					anim(f"[{completed}] {row[1]}")
			press_any_key_to_continue()

def add_task():
	clear_terminal()
	loading_anim()
	name = anim_with_input("Enter the name of the task to add: ")
	
	with get_connection() as conn:
		with conn.cursor() as cursor:

			cursor.execute(
                "SELECT * FROM tasks WHERE title = %s",
                (name,)
            )

			row = cursor.fetchone()
			if row:
				anim("A task with that name already exists!")
			else:
				cursor.execute("INSERT INTO tasks (title) VALUES (%s)", (name,))
				anim("Adding a new task is complete!")
	press_any_key_to_continue()

def complete_task():
	clear_terminal()
	loading_anim()
	name = anim_with_input("Enter the name of the completed task: ")
	with get_connection() as conn:
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM tasks WHERE title = %s", (name,))
			row = cursor.fetchone()
			if row:
				cursor.execute("UPDATE tasks SET is_done = %s WHERE title = %s", (True, name))
				anim("The task has been successfully completed!")
			else:
				anim("Task not found!")
	press_any_key_to_continue()

def delete_task():
	clear_terminal()
	loading_anim()
	name = anim_with_input("Enter the name of the task to be deleted: ")
	with get_connection() as conn:
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM tasks WHERE title = %s", (name,))
			row = cursor.fetchone()
			if row:
				cursor.execute("DELETE FROM tasks WHERE title = %s", (name,))
				anim("Task successfully deleted!")
			else:
				anim("Task not found!")
	press_any_key_to_continue()

def show_pending_tasks():
	clear_terminal()
	loading_anim()
	with get_connection() as conn:
		with conn.cursor() as cursor:
			cursor.execute("SELECT * FROM tasks")
			rows = cursor.fetchall()

			if not rows:
				anim("You don't have any tasks yet!")
			else:
				cursor.execute("SELECT * FROM tasks WHERE is_done = false")

				rows = cursor.fetchall()

				if not rows:
					anim("You have no uncompleted tasks!")
				else:
					for row in rows:
						anim(f"[ ] {row[1]}")

	press_any_key_to_continue()


def show_menu():
	anim("=== TASK MANAGER ===")
	anim("1. Show all tasks")
	anim("2. Add task")
	anim("3. Complete task")
	anim("4. Delete task")
	anim("5. Show pending tasks")
	anim("0. Exit")
	
working = True

def exit_from_tasklist():
	global working
	clear_terminal()
	loading_anim()
	anim("Bye!")
	working = False
	
actions = {
			"1": show_all_tasks,
			"2": add_task,
			"3": complete_task,
			"4": delete_task,
			"5": show_pending_tasks,
			"0": exit_from_tasklist,
		}

def main():
	while working:
		clear_terminal()
		show_menu()

		choice = input("\nChoose: ")

		action = actions.get(choice)

		if action:
			action()
		else:
			anim("Error! No such action exists!")
			press_any_key_to_continue()

main()