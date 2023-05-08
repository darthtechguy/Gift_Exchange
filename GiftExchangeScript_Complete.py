import os
import json

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_name(name, name_list):
    if name not in name_list:
        name_list.append(name)
        return True
    return False

def prompt_number(user_name, name_list, available_numbers):
    while True:
        try:
            num = int(input("Enter a number (1-{}): ".format(len(available_numbers))))
            if num in available_numbers and name_list[num - 1] != user_name:
                available_numbers.remove(num)
                return num
            else:
                print("Invalid number or choosing own name. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def edit_gift_exchange(gift_exchange, name_list, available_numbers):
    giver = input("Enter the name of the giver you want to edit: ")
    if giver not in gift_exchange:
        print("Name not found in the gift exchange list.")
        input("Press enter to continue...")
        return
    new_number = prompt_number(giver, name_list, available_numbers)
    gift_exchange[giver] = name_list[new_number - 1]


def choose_save_location():
    print("Choose the save location:")
    save_path = input("Enter the path (e.g., C:\\Users\\YourUsername\\Documents\\): ")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return save_path

def choose_save_filename():
    print("Choose the save filename:")
    save_filename = input("Enter the filename (without extension): ")
    return save_filename + ".json"

def save_data(name_list, gift_exchange, available_numbers):
    save_path = choose_save_location()
    save_filename = choose_save_filename()
    data = {
        'name_list': name_list,
        'gift_exchange': gift_exchange,
        'available_numbers': list(available_numbers)
    }
    with open(os.path.join(save_path, save_filename), 'w') as f:
        json.dump(data, f)
    print("Data saved to '{}'.".format(os.path.join(save_path, save_filename)))
    input("Press enter to continue...")

def load_data():
    print("Choose the file to load:")
    load_path = input("Enter the file path (e.g., C:\\Users\\YourUsername\\Documents\\yourfile.json): ")
    try:
        with open(load_path, 'r') as f:
            data = json.load(f)
        name_list = data['name_list']
        gift_exchange = data['gift_exchange']
        available_numbers = set(data['available_numbers'])
        return name_list, gift_exchange, available_numbers
    except FileNotFoundError:
        print("File not found. Starting with empty data.")
        input("Press enter to continue...")
        return [], {}, set()


def main():
    name_list, gift_exchange, available_numbers = load_data()

    while True:
        clear_screen()
        print("1. Add a name")
        print("2. Enter a number")
        print("3. Show gift exchange list")
        print("4. Show names not chosen")
        print("5. Show list of input names")
        print("6. Edit gift exchange list")
        print("7. Save data")
        print("8. Exit")
        choice = input("Choose an option (1-8): ")

        if choice == '1':
            name = input("Enter a name: ")
            if add_name(name, name_list):
                available_numbers.add(len(name_list))
            else:
                print("Duplicate name entry. Name not added.")
                input("Press enter to continue...")
        elif choice == '2':
            if len(available_numbers) == 0:
                print("No available numbers. Please add names first.")
                input("Press enter to continue...")
                continue
            user_name = input("Enter your name: ")
            if user_name in gift_exchange:
                print("You have already chosen a number.")
                input("Press enter to continue...")
                continue
            chosen_number = prompt_number(user_name, name_list, available_numbers)
            gift_exchange[user_name] = name_list[chosen_number - 1]
            print("You have chosen number {}.".format(chosen_number))
            input("Press enter to continue...")
        elif choice == '3':
            print("Gift Exchange List:")
            for giver, receiver in gift_exchange.items():
                print("{} -> {}".format(giver, receiver))
            input("Press enter to continue...")
        elif choice == '4':
            print("Names not chosen:")
            for i, name in enumerate(name_list, start=1):
                if i in available_numbers:
                    print(name)
            input("Press enter to continue...")
        elif choice == '5':
            print("List of input names:")
            for name in name_list:
                print(name)
            input("Press enter to continue...")
        elif choice == '6':
            edit_gift_exchange(gift_exchange, name_list, available_numbers)
        elif choice == '7':
            save_data(name_list, gift_exchange, available_numbers)
            print("Data saved.")
            input("Press enter to continue...")
        elif choice == '8':
            generate_txt_file(gift_exchange)
            print("Generated 'gift_exchange_info.txt' with current information.")
            input("Press enter to continue...")
        elif choice == '9':
            break

if __name__ == "__main__":
    main()

