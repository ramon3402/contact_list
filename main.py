import storage
from storage import read_contacts, write_contacts

CONTACT_FILE_PATH = "contacts.json"


def initial_display():
    print("Welcome to your contact list!")
    print("The following is a list of useable commands: ")
    print("\"add\": Adds a contact.")
    print("\"delete\": Deletes a contact.")
    print("\"list\": Lists all contacts.")
    print("\"search\": Searches for a contact by name.")
    print("\"q\": Quits the program and saves the contact list.")
    print()

def verify_email_address(email):
    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False

    return True


def verify_phone_number(phone_number):
    if len(phone_number)<10:
        return False
    cleaned_number = phone_number.replace("-","")
    if len(cleaned_number) < 10:
        return False
    for letter in cleaned_number:
        if not letter.isdigit():
            return False
        
    return True
    
def add_contact(contacts):
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    mobile_phone_number = input("Mobile Phone Number: ").strip()
    home_phone_number = input("Home Phone Number: ").strip()
    email_address = input("Email address: ").strip()
    address = input("Address: ").strip()
    
    if not first_name or not last_name:
        print("Contact must have a first and last name.")
        
    elif mobile_phone_number and not verify_phone_number(mobile_phone_number):
        print("Invalid Mobile Phone Number.")
        
    elif home_phone_number and not verify_phone_number(home_phone_number):
        print("Invalid Home Phone Number.")
        
    elif email_address and not verify_email_address(email_address):
        print("Invalid Emial Address")
        
    elif get_contact_by_name(contacts, first_name, last_name):
        print("A contact with this name already exists.")
    #check if this contact name exist/ is unique  
    else:
        new_contact = {
            "first_name" : first_name,
            "last_name" : last_name,
            "mobile" : mobile_phone_number,
            "home" : home_phone_number,
            "email" : email_address,
            "address": address   
        }
        contacts.append(new_contact)
        
        print("Contact Added!")
        
def get_contact_by_name(contacts, first_name, last_name):
    for contact in contacts:
        if contact["first_name"] == first_name and contact["last_name"] == last_name:
            return contact

    return None

def search_for_contact(contacts):
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    matching_contacts = find_matching_contact(contacts, first_name, last_name)
    if len(matching_contacts) > 0:
        print(f"Found {len(matching_contacts)} matching contacts.")
        list_contacts(matching_contacts)
    else:
        print("Found no matching contacts.")
        
    

def find_matching_contact(contacts, first_name, last_name):
    matching_contacts = []
    for contact in contacts:
        if first_name and (first_name in contact['first_name'] or first_name.lower() in contact['first_name'] 
                           or first_name in contact['first_name'].lower() or first_name.lower() in contact['first_name'].lower()):
            matching_contacts.append(contact)
            
        if last_name and (last_name in contact['last_name'] or last_name.lower() in contact['last_name']
                                         or last_name in contact['last_name'].lower() or last_name.lower() in contact['last_name'].lower()):
            if contact not in matching_contacts:               
                matching_contacts.append(contact)
    return matching_contacts            

def delete_contact(contacts):
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    
    contact = get_contact_by_name(contacts, first_name, last_name)
    if not contact:
        print("No contact with this name exists!")
    else:
        confirm = input("Are you sure you want to remove this contact (y/n)? ")
        if confirm == 'y':
            contacts.remove(contact)
            
            
    
def get_contact_string(contact):
    string = f'{contact["first_name"].capitalize()} {contact["last_name"].capitalize()}'
    
    for field in ["mobile", "home", "email", "address"]:
        value = contact[field]
        if not value:
            continue
        string += f"\n\t{field.capitalize()}: {value}"
        
    return string


def list_contacts(contacts):
    sorted_contacts = sorted(contacts, key = lambda x:x['first_name'])
    
    for i , contact in enumerate(sorted_contacts):
        print(f"{i+1}. {get_contact_string(contact)}")


def main(contacts_path):
    initial_display()
    contacts = read_contacts(contacts_path)
    while True:
        command_entered = input("Type a command: ")
        if command_entered == "q":
            write_contacts(contacts_path, contacts)
            print("Contacts were saved successfully")
            break
        elif command_entered == "add":
            add_contact(contacts)
        elif command_entered == 'list':
            list_contacts(contacts)
        elif command_entered == "delete":
            delete_contact(contacts)    
        elif command_entered == "search":
            search_for_contact(contacts)
        else:
            print("Unkown command")
        
if __name__ == "__main__":
    main(CONTACT_FILE_PATH)
