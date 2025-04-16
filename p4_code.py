# Colby Eastmond, Merrick Morgan, Spencer Jorgenson, Jacob Lee, Talon Condie
# P4 - Retail Sales Pandas and Postgres

# The purpose of this assignment is to use Pandas and Postgres to interact with an excel file, create a database table
# and pull data from a Postgres database table


# Import packages
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plot
import openpyxl
import psycopg2



# Create a variable to enter the while loop. Until bContinue = False, continue the loop
bcontinue = True

# Initialize the while loop
while bcontinue:
    # Collect input from the user
    print("If you want to import data, enter 1.\nIf you want to see summaries of stored data, enter 2.\nEnter any other value to exit the program: ")
    userInput = input("Please Enter Value: ")

    # PART 1: If they enter 1, do the following:
    if userInput == '1': 
        # 1.	Read the Retail_Sales_Data.xlsx into python.
        df = pd.read_excel("Retail_Sales_Data.xlsx")

        # 2.	Separate the "name” column into a “first_name” and “last_name” column and delete (or overwrite) the original “name” column
        dfSeparateNames = df["name"].str.split("_", expand=True)
        dfSeparateNames.columns = ["First Name", "Last Name"]

        df.insert(1, "First Name", dfSeparateNames["First Name"])
        df.insert(2, "Last Name", dfSeparateNames["Last Name"])
        del df['name']

        # 3.	Fix the “category” column so that the categories actually match the product that was sold
        productCategoriesDict = {
            'Camera': 'Technology',
            'Laptop': 'Technology',
            'Gloves': 'Apparel',
            'Smartphone': 'Technology',
            'Watch': 'Accessories',
            'Backpack': 'Accessories',
            'Water Bottle': 'Household Items',
            'T-shirt': 'Apparel',
            'Notebook': 'Stationery',
            'Sneakers': 'Apparel',
            'Dress': 'Apparel',
            'Scarf': 'Apparel',
            'Pen': 'Stationery',
            'Jeans': 'Apparel',
            'Desk Lamp': 'Household Items',
            'Umbrella': 'Accessories',
            'Sunglasses': 'Accessories',
            'Hat': 'Apparel',
            'Headphones': 'Technology',
            'Charger': 'Technology'}
        df['category'] = df['product'].map(productCategoriesDict)

        # 4.	Save the results as a table called ‘sale’ in your is303 postgres database.
        username = 'postgres'
        password = 'pgadmin4'
        host = 'localhost'
        port = '5432'
        database = 'IS303'

        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')
        df.to_sql('sale', con=engine, if_exists='replace', index=True)
        print('Data Imported')
        # 5.	Print out the message: “You've imported the excel file into your postgres database.”
        print("You've imported the excel file into your postgres database.")

    # PART 2: If they enter 2, do the following:
    elif userInput == '2':
        # 1.	Print out: “The following are all the categories that have been sold:”
        print("The following are all the categories that have been sold: ")
        print()

        # 2.	Print out each of the categories stored in your database from the ‘sale’ table with a number preceding it. You can’t just hardcode the categories in, your program must read them from the database. It should look like this:
            # 1: Technology
            # 2: Apparel
            # 3: Accessories
            # 4: Household Items
            # 5: Stationery
        dfImported = pd.read_sql_query('SELECT * FROM sale', engine)
        categories = dfImported['category'].unique()

        categorydict = {}

        for index, category in enumerate(categories, start=1):
            categorydict[index] = category
            print(f"{index}. {category}")
        print()


    # 3.	Print out: “Please enter the number of the category you want to see summarized: “
        print("Please enter the number of the category you want to see summarized: ")
        sumCategory = int(input("Enter a number: "))
        selectedCategory = categorydict[sumCategory]

        dfFiltered = dfImported[dfImported['category']== selectedCategory]

    # 4.	Then, for the entered category, calculate and display the sum of total sales, the average sale amount, and the total units sold.
        total_sales = dfFiltered['total_price'].sum()
        avg_sale = dfFiltered['total_price'].mean()
        total_units = dfFiltered['quantity_sold'].sum()
        print(f"Total sales for {selectedCategory}: ${total_sales:,.2f}")
        print(f"Average sale for {selectedCategory}: ${avg_sale:,.2f}")
        print(f"Total units for {selectedCategory}: ${total_units:,.2f}")
        
    # 5.	Then, display a bar chart with the x axis as the products in that category and the y axis as the sum of the total sales of that product.

        sales_by_product = dfFiltered.groupby('product')['total_price'].sum().reset_index()
        sales_by_product.plot.bar( x = 'product', y = 'total_price', rot=15, title = f'Total Sales by Product in {selectedCategory}')
    # a.	The title of the chart should be “Total Sales by Product in Category (but put the actual category name)
    # b.	The x label should be “Product”, the y label should be “Total Sales”
        plot.xlabel("Product")
        plot.ylabel("Total Sales")
        plot.show()




    # If they enter anything other than 1 or 2:
    # 1.	Print: "Closing the program."
    else:
        print("Closing the program")
        bcontinue = False
    


