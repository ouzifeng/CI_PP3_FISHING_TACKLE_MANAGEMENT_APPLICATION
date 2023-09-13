# Fishing Tackle Management System

By David Oak

<img src="docs/responsive-design.png" alt="A repsonsive screenshot of the application">

[Link to live site](https://python-module-3c3f040b0b4c.herokuapp.com/)

## Introduction

A fishing tackle shop spends a lot of time manually updating, creating and managing their fishing tackle products. They have requested from me a CLI based application where they can access their stock management system, which is setup using a Google Sheet. This application must be able to update, create and delete products, as well as have additional functionality such as a login/sign up field for security, and the ability to check margins of products.

They estimate that this will half the time they currently spend managing the Google Sheet manually, which frees up resources for them to invest in growing their business both online and in store.

### Business Requirements

As the end user and the customer are the same, they have given a set of clearly defined requirements the application needs to adhere to:

1. Allow user to login and sign up
2. Validate email and passwords, and give instructions on pw requirements
3. Have a clear and easy to use main menu
4. To be able to check which products are out of stock
5. To be able to email user a list of out of stock products
6. Show last time a user logged in
7. Create a new product with validation for price and stock
8. Update existing products using the SKU as the unique identifier
9. Validate price and stock update fields
10. Delete a product with a double confirmation, using the SKU as the unique identifier
11. Print out a list of all products with their margins, from highest margin to lowest
12. Have a margin filter feature, so the user can filter out/in products above/below a certain margin %, with input validation
13. If an update product is not found, give option to create a new product
14. Avoid menu loops, if input(s) are invalid allow user to input again. Do not default back to the current menu option
15. Fishing tackle product names can be long, make sure any tables printed to the terminal as less than 80 characters in width

### Target Audience

ALthough this application has been designed for a specific online store, any store that uses Google Sheets to manage products can integrate this software. However the sheets must be setup as so:

 **Sheet Name**   | **Column 1 Header**  | **Column 2 Header** | **Column 4 Header** | **Column 5 Header** |
| --------------- | -------------------- | ------------------- | ------------------- | ------------------- |
| products | SKU | Product Name | Cost Price | RRP | Stock |
| user | User | Password | Last Login |
| test_user | User | Password | Last Login |

## Technical Design

### Flowchart

This flowchart was created using Lucidcharts to plot out how the user flows through the app

## Technologies Used

#### Languages

* Python was the programming language used for the application
* HTML was used to structure the email content

#### Frameworks and Tools

* Lucidcharts for the wireframes
* Googlesheets to host the data
* Googlesheets API to interface with the application and the Googlesheets
* Heroku was used to host the application
* Git was used for version control
* CI Python Linter was used to check PEP8 conformity 
* Github was used for saving files and deploying automatically to Heroku on deployment changes
* AmIresponsive was used to test the application across different devices
* AWS SES was used as the email client

### Python & Third Party Libraries

* re - for checking inputs passed requirements
* os - used to clear terminal
* gspread - a python API for Google Sheets
* prettytable - to build the tables printed in the console
* coverage - to measure how much of the application is being tested via automated unit testing
* colorama - to provide a more interactive interface
* datetime - to store timestamps of logins
* google-auth - to authenticate Googles APIs
* unittest - to build unit testings

### Features

#### Main Menu

* Provides welcome note and instructions on how to reset the app
* Allows user to login or create an account
* Differentiate menu colour to improve readability

<details>
    <summary>Main Menu</summary>
    <img src="docs/features/main-menu.png" alt="Main Menu">
</details>  

Solves business requirement 1, 14

#### Login/Signup

1. Login - validates email
2. Login - validates password
3. Login - validates whether user exists
4. Login - displays last login time
4. Validates a genunie option (i.e. 1-3) is made, otherwiase asks user to make another choice
5. Sign up - validates email
6. Sign up - checks whether user already exists
7. Sign up - gives password requirements
8. Sign up - requires input password twice
9. Sign up - provides feedback account was created

<details>
    <summary>Login/Signup</summary>
    <img src="docs/features/login-val-1.png" alt="Login area 1">
    <img src="docs/features/login-val-2.png" alt="Login area 2">
    <img src="docs/features/login-val-3.png" alt="Login area 3">
    <img src="docs/features/login-val-4.png" alt="Login area 4">
    <img src="docs/features/signup-val-1.png" alt="Sign up area 1">
    <img src="docs/features/signup-val-2.png" alt="Sign up area 2">
    <img src="docs/features/signup-val-3.png" alt="Sign up area 3">
</details>  

Solves business requirements 1,2,3,6, 14


#### Product Management Menu

1. Clear and easy to navigate
2. Option to check out of stock products
3. Option to start managing products
4. Option to start deleting products
5. Option to start checking product margins

<details>
    <summary>Product Management Menu</summary>
    <img src="docs/features/product-management-menu.png" alt="Product Management Menu">
</details> 

Solves business requirements 3

#### Out of stock products

1. View all out of stock products
2. User will want to place an order with the manufacturer for stock, so an email can be send as a table with all the OOS products
3. Option to go abck to the main menu

<details>
    <summary>Out of stock products</summary>
    <img src="docs/features/oos-1.png" alt="Print out of stock products">
    <img src="docs/features/oos-2.png" alt="Send email with out of stock products">
    <img src="docs/features/oos-3.png" alt="Out of stock products email">
</details> 

