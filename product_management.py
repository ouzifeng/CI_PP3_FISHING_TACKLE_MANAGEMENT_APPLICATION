import re
import gspread
from prettytable import PrettyTable
from email_service import send_email
from google.oauth2.service_account import Credentials
from utilities import get_integer_input

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('fishing_tackle')
products = SHEET.worksheet('products')


def update_product_details():
    """ Allows the user to update product SKU, Name, Stock and Prices """
    sku = input("Enter SKU of the product you want to update: ")
    cell = products.find(sku)
    if cell is None:
        print("Product with SKU", sku, "not found.")
        prompt_msg = ("Would you like to create a new product with this "
                      "SKU? (yes/no): ")
        choice = input(prompt_msg)
        if choice.lower() == 'yes':
            create_product()
        return
    else:
        row_num = cell.row
        product_row = products.row_values(row_num)

    while True:
        print("\nCurrent Product Details:")
        print("SKU:", product_row[0])
        print("1. Product Name:", product_row[1])
        print("2. Cost Price:", product_row[2])
        print("3. RRP:", product_row[3])
        print("4. Stock:", product_row[4])
        print("5. Exit to previous menu")
        prompt_msg = ("\nWhich detail would you like to update? "
                      "(Enter 1 for Product Name, 2 for Cost Price etc, "
                      "or press Enter to skip):")
        print(prompt_msg)

        choice = input()
        if choice == '1':
            new_value = input("Enter new Product Name: ")
            products.update_cell(row_num, 2, new_value)
        elif choice == '2':
            new_value = get_integer_input("Enter new Cost Price: ")
            products.update_cell(row_num, 3, new_value)
        elif choice == '3':
            new_value = get_integer_input("Enter new RRP: ")
            products.update_cell(row_num, 4, new_value)
        elif choice == '4':
            new_value = get_integer_input("Enter new Stock: ")
            products.update_cell(row_num, 5, new_value)
        elif choice == '5' or choice == '':
            print("Exiting to previous menu.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
        product_row = products.row_values(row_num)
    print("\nProduct details updated successfully!")


def delete_product():
    """ Allows the user to delete a product """
    sku = input("Enter SKU of the product you want to delete: ")
    cell = products.find(sku)
    if cell is None:
        print("\nProduct with SKU", sku,
              "not found. Please choose another option")
        return
    else:
        row_num = cell.row
        product_row = products.row_values(row_num)
    print("\nProduct Details:")
    print("SKU:", product_row[0])
    print("Product Name:", product_row[1])
    print("Cost Price:", product_row[2])
    print("RRP:", product_row[3])
    print("Stock:", product_row[4])
    prompt_msg = ("\nAre you sure you want to delete this product? "
                  "(yes/no): ")
    choice = input(prompt_msg)
    if choice.lower() == 'yes':
        double_check_msg = ("This action is irreversible. "
                            "Confirm deletion? (yes/no): ")
        double_check = input(double_check_msg)
        if double_check.lower() == 'yes':
            products.delete_rows(row_num, row_num)
            print("Product deleted successfully!")
        else:
            print("Product deletion canceled.")
    else:
        print("Product deletion canceled.")


def check_out_of_stock():
    """ Prints out products that are out of stock. """
    products = SHEET.worksheet('products')
    records = products.get_all_records()
    out_of_stock_items = [
        record for record in records
        if record and record.get('Stock', 1) <= 0
    ]

    if not out_of_stock_items:
        print("All products are in stock!")
        return

    table = PrettyTable()

    table.field_names = ["SKU", "Product Name"]
    table.align["SKU"] = "l"
    table.align["Product Name"] = "l"

    for item in out_of_stock_items:
        sku = str(item.get('SKU', '-'))[:10]
        product_name = item.get('Product Name', '-')[:40]
        table.add_row([sku, product_name])

    for row in table._rows:
        row[0] = row[0][:10]
        row[1] = row[1][:40]

    print(table)

    menu_options = (
        "\nWould you like to:\n"
        "1. Send an email with these products for you to order\n"
        "2. Back to main menu"
    )
    print(menu_options)
    choice = input("Select an option: ")

    if choice == '1':
        recipient_email = input("Enter the email address to send to: ")
        subject = "Out of Stock Products"
        send_email(recipient_email, subject, out_of_stock_items)
        print("Email sent successfully!")
    elif choice == '2':
        return
    else:
        print(Fore.RED + "Invalid choice!")


def create_product():
    """ Allows the user to create a new product """
    products_sheet = SHEET.worksheet('products')

    products = products_sheet.get_all_records()
    existing_skus = [product['SKU'] for product in products]

    while True:
        sku = input("Enter the SKU for the new product: ")
        if sku in existing_skus:
            print("SKU already exists. Please enter a unique SKU.")
            continue
        prompt_msg = "Enter the name of the product (more than 3 chars): "
        product_name = input(prompt_msg)
        if len(product_name) <= 3:
            print("Product name must be more than 3 characters!")
            continue
        try:
            prompt_cost = "Enter the cost price: "
            cost_price = float(input(prompt_cost).replace('£', '').strip())
            prompt_rrp = "Enter the RRP of the product: "
            rrp = float(input(prompt_rrp).replace('£', '').strip())
            stock = int(input("Enter the stock level: "))
            break
        except ValueError:
            print("Enter valid values for price and stock!")

    new_row = [
        sku,
        product_name,
        f"{cost_price:.2f}",
        f"{rrp:.2f}",
        str(stock)
    ]
    products_sheet.append_row(new_row)
    print(f"Product {product_name} with SKU {sku} added successfully!")


def check_product_margins():
    """Shows product margins of all products, and filter margins"""
    products_sheet = SHEET.worksheet('products')
    products = products_sheet.get_all_records()

    while True:
        print("\nOptions:")
        print("1. Show all product margins as % ranked from highest to lowest")
        print("2. Filter out products with margins"
              "either above or below a certain %")
        print("3. Back to main menu")
        choice = input("Select an option: ")

        if choice == '1':
            margins = []
            for product in products:
                rrp = clean_price(product['RRP'])
                cost = clean_price(product['Cost Price'])
                margin_percentage = ((rrp - cost) / rrp) * 100 if rrp else 0
                margins.append({
                    'SKU': product['SKU'],
                    'Product Name': product['Product Name'],
                    'Margin %': margin_percentage
                })

            def key_func(x):
                return x['Margin %']
            sorted_margins = sorted(margins, key=key_func, reverse=True)
            table = PrettyTable()
            table.field_names = ["SKU", "Product Name", "Margin %"]
            table.align["SKU"] = "l"
            table.align["Product Name"] = "l"
            table.align["Margin %"] = "l"
            for margin in sorted_margins:
                sku = str(margin['SKU'])[:10]
                product_name = margin['Product Name'][:40]
                margin_value = f"{margin['Margin %']:.2f}%"
                table.add_row([sku, product_name, margin_value])
            print(table)

        elif choice == '2':
            operation = input("Enter operation (either '>' or '<'): ")
            if operation not in ['>', '<']:
                print("Invalid operation. Retry.")
                continue
            try:
                threshold = float(input("Enter threshold percentage: "))
            except ValueError:
                print("Invalid input. Retry.")
                continue

            def meets_threshold(margin, op, thresh):
                if op == '>':
                    return margin['Margin %'] > thresh
                if op == '<':
                    return margin['Margin %'] < thresh
                return False

            filtered_margins = [
                m for m in margins
                if meets_threshold(m, operation, threshold)
            ]

            if not filtered_margins:
                margin_direction = 'above' if operation == '>' else 'below'
                print(f"\nNo products with margins {margin_direction} "
                      f"{threshold}%.")
            else:
                table = PrettyTable()
                table.field_names = ["SKU", "Product Name", "Margin %"]
                table.align["SKU"] = "l"
                table.align["Product Name"] = "l"
                table.align["Margin %"] = "l"
                for margin in filtered_margins:
                    sku = str(margin['SKU'])[:10]
                    product_name = margin['Product Name'][:40]
                    margin_value = f"{margin['Margin %']:.2f}%"
                    table.add_row([sku, product_name, margin_value])
                print(table)

        elif choice == '3':
            return

        else:
            print("Invalid choice. Retry.")


def clean_price(price_str):
    """Remove any non-numeric characters and convert to float."""
    cleaned_price = ''.join(filter(str.isdigit or str.isdecimal, price_str))
    return float(cleaned_price) / 100
