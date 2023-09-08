# Fishing Tackle Management System

By David Oak

<img src="docs/responsive-design.png" alt="A repsonsive screenshot of the application">

[Link to live site](https://python-module-3c3f040b0b4c.herokuapp.com/)

## Introduction

A fishing tackle shop spends a lot of time manually updating, creating and managing their fishing tackle products. They have requested from me a CLI based application where they can access their stock management system, which is setup using a Google Sheet. This application must be able to update, create and delete products, as well as have additional functionality such as a login/sign up field for security, and the ability to check margins of products.

They estimate that this will half the time they currently spend managing the Google Sheet manually, which frees up resources for them to invest in growing their business both online and in store.

### Business Requirements

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


