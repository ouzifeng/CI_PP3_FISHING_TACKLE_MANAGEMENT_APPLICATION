from utilities import get_integer_input
from google.oauth2.service_account import Credentials
import gspread
from prettytable import PrettyTable
from email_service import send_email

# Google Sheets authentication
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
    sku = input("Enter SKU of the product you want to update: ")
    cell = products.find(sku)
    if cell is None:
        print("Product with SKU", sku, "not found.")
        choice = input("Would you like to create a new product with this SKU? (yes/no): ")
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
        print("\nWhich detail would you like to update? (Enter 1 for Product Name, 2 for Cost Price etc, or press Enter to skip):")
        
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
    sku = input("Enter SKU of the product you want to delete: ")
    cell = products.find(sku)
    if cell is None:
        print("\nProduct with SKU", sku, "not found. Please choose another option")
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
    choice = input("\nAre you sure you want to delete this product? (yes/no): ")
    if choice.lower() == 'yes':
        double_check = input("This action is irreversible. Confirm deletion? (yes/no): ")
        if double_check.lower() == 'yes':
            products.delete_rows(row_num, row_num)
            print("Product deleted successfully!")
        else:
            print("Product deletion canceled.")
    else:
        print("Product deletion canceled.")
        
def check_out_of_stock():
    """Prints out products that are out of stock."""
    products = SHEET.worksheet('products')
    records = products.get_all_records()
    out_of_stock_items = [record for record in records if record and record.get('Stock', 1) <= 0]
    
    if not out_of_stock_items:
        print("All products are in stock!")
        return

    # Create a table
    table = PrettyTable()
    
    # Set the headers for the table
    table.field_names = ["SKU", "Product Name"]
    
    # Add rows to the table
    for item in out_of_stock_items:
        sku = item.get('SKU', '-')
        product_name = item.get('Product Name', '-')
        table.add_row([sku, product_name])
    
    # Print the table
    print(table)

    print("\nWould you like to:")
    print("1. Send an email with these products for you to order")
    print("2. Back to main menu")
    choice = input("Select an option: ")

    if choice == '1':
        recipient_email = input("Enter the email address to send to: ")
        send_email(recipient_email, "Out of Stock Products", out_of_stock_items)
        print("Email sent successfully!")
    elif choice == '2':
        return
    else:
        print("Invalid choice!")
        
def create_product():
    products_sheet = SHEET.worksheet('products')

    # Fetch existing SKUs from your product database or storage
    existing_skus = [product['SKU'] for product in products_sheet.get_all_records()]

    while True:
        sku = input("Enter the SKU for the new product: ")

        # Check if the SKU already exists
        if sku in existing_skus:
            print("SKU already exists. Please enter a unique SKU.")
            continue

        # Validate product name
        while True:
            product_name = input("Enter the name of the product: ")
            if len(product_name) <= 3:
                print("Product name must be more than 3 characters!")
                continue
            break

        # Validate cost price
        while True:
            cost_price_input = input("Enter the cost price of the product: ").replace('£', '').strip()
            try:
                cost_price = float(cost_price_input)
                if '.' not in cost_price_input:
                    cost_price = "{:.2f}".format(cost_price)
                break
            except ValueError:
                print("Cost price must be a valid number!")

        # Validate RRP
        while True:
            rrp_input = input("Enter the recommended retail price (RRP) of the product: ").replace('£', '').strip()
            try:
                rrp = float(rrp_input)
                if '.' not in rrp_input:
                    rrp = "{:.2f}".format(rrp)
                break
            except ValueError:
                print("RRP must be a valid number!")

        # If the SKU is unique, you can proceed to create the product or store it in your database.
        # Remember to break the loop to exit the SKU validation.
        break


    # Validate stock level
    while True:
        stock_input = input("Enter the stock level of the product: ")
        try:
            stock = int(stock_input)
            break
        except ValueError:
            print("Stock level must be a valid integer!")

    # Append the new product data to the worksheet
    products_sheet.append_row([sku, product_name, str(cost_price), str(rrp), str(stock)])
    
    print(f"Product {product_name} with SKU {sku} added successfully!")
    
def check_product_margins():
    while True:
        products_sheet = SHEET.worksheet('products')
        products = products_sheet.get_all_records()

        print("\nOptions:")
        print("1. Show all product margins as % ranked from highest to lowest")
        print("2. Filter out products with margins either above or below a certain %")
        print("3. Back to main menu")
        choice = input("Select an option: ")

        if choice == '1':
            margins = []
            for product in products:
                cost_price = clean_price(product['Cost Price'])
                rrp = clean_price(product['RRP'])
                margin_percentage = ((rrp - cost_price) / rrp) * 100 if rrp != 0 else 0
                margins.append({
                    'SKU': product['SKU'],
                    'Product Name': product['Product Name'],
                    'Margin %': margin_percentage
                })

            sorted_margins = sorted(margins, key=lambda x: x['Margin %'], reverse=True)
            table = PrettyTable()
            table.field_names = ["SKU", "Product Name", "Margin %"]
            for margin in sorted_margins:
                table.add_row([margin['SKU'], margin['Product Name'], f"{margin['Margin %']:.2f}%"])
            print(table)

        elif choice == '2':
            operation = None
            while operation not in ['>', '<']:
                operation = input("Enter operation (either '>' or '<'): ")
                if operation not in ['>', '<']:
                    print("Invalid operation. Please enter either '>' or '<'.")

            while True:
                try:
                    threshold = float(input("Enter threshold percentage: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

            if operation == '>':
                filtered_margins = [m for m in margins if m['Margin %'] > threshold]
            else:  # operation is '<'
                filtered_margins = [m for m in margins if m['Margin %'] < threshold]

            if not filtered_margins:
                print(f"\nThere are no products with margins {'above' if operation == '>' else 'below'} {threshold}%.")
            else:
                table = PrettyTable()
                table.field_names = ["SKU", "Product Name", "Margin %"]
                for margin in filtered_margins:
                    table.add_row([margin['SKU'], margin['Product Name'], f"{margin['Margin %']:.2f}%"])
                print(table)

        elif choice == '3':
            return  # Return to the main menu

        else:
            print("Invalid choice. Please choose a valid option (1, 2, or 3).")



def clean_price(price_str):
    """Remove any non-numeric characters and convert to float."""
    cleaned_price = ''.join(filter(str.isdigit or str.isdecimal, price_str))
    return float(cleaned_price) / 100  # Assuming the last two characters are pence




