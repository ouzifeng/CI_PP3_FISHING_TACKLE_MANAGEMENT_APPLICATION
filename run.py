from authentication import login, is_valid_email
from authentication import signup
from product_management import (
    update_product_details,
    delete_product,
    check_out_of_stock,
    create_product,
    check_product_margins
)


def main():
    """Main function to prompt user for what they want to do."""
    logged_in = False

    while not logged_in:
        print(
            "\nWelcome to the fishing tackle management system. If at any "
            "time you need to restart the system, press the red button "
            "at the top labeled 'RUN PROGRAM'"
        )
        print("\nWhat do you want to do?")
        print("1. Login")
        print("2. Sign up")
        print("3. Exit Application")
        try:
            choice = input("Select an option: ")

            if choice == '1':
                logged_in = login()
                if logged_in:
                    break

            elif choice == '2':
                signup()
            elif choice == '3':
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Invalid choice!")

    while logged_in:
        print("\nWhat do you want to do?")
        print("1. View all out-of-stock products")
        print("2. Create a new product")
        print("3. Update Product Details")
        print("4. Delete a Product")
        print("5. Check Product Margins")
        print("6. Log out")

        try:
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
                raise ValueError
        except ValueError:
            print("\nInvalid choice. Please choose a number between 1 and 6")


if __name__ == "__main__":
    main()
