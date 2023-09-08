from authentication import login, signup
from product_management import update_product_details, delete_product, check_out_of_stock, create_product

def main():
    """Main function to prompt user for what they want to do."""
    logged_in = False

    while not logged_in:
        print("\nWhat do you want to do?")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit Application")
        
        choice = input("Select an option: ")

        if choice == '1':
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            logged_in = login(email, password)
        elif choice == '2':
            signup()
        elif choice == '3':
            exit()
        else:
            print("Invalid choice!")

while logged_in:
    print("\nWhat do you want to do?")
    print("1. View all out-of-stock products")
    print("2. Create a new product")
    print("3. Update Product Details")
    print("4. Delete a Product")
    print("5. Check Product Margins")
    print("6. Log out")
    
    choice = input("Select an option: ")

    if choice == '1':
        check_out_of_stock()
    elif choice == '2':
        create_product()
    elif choice == '3':
        update_product_details()
    elif choice == '4':
        delete_product()
    elif choice == '5':
        check_product_margins()
    elif choice == '6':
        logged_in = False
        print("Logged out successfully!")
    else:
        print("Invalid choice!")


if __name__ == "__main__":
    main()

