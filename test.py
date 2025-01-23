from datetime import datetime

import openpyxl
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Border, Font, Side

total_map = {}
# Read the sales data from the Excel file into a DataFrame
sales_modified_df = pd.read_excel(
    "report_data/sales_modified.xlsx",
    sheet_name="Sales_export",
    engine="openpyxl",
)

# Get the unique brands from the DataFrame
unique_brands = sales_modified_df["Brand"].unique().tolist()

length_of_unique_portal = (
        len(sales_modified_df["Portal"].unique().tolist()) + 1
)
length_of_unique_brands = (
        len(sales_modified_df["Brand"].unique().tolist()) + 1
)  # +1 for (Total) Row

# Initialize an empty DataFrame to store the combined pivot tables
combined_pivot_table = pd.DataFrame()

# Get the current time and create a DataFrame with it
current_time = datetime.now().strftime("%H:%M")
time_column = pd.DataFrame({"Current Time": [current_time]})

# Initialize border style
border_style = Border(
    left=Side(style="thin", color="000000"),
    right=Side(style="thin", color="000000"),
    top=Side(style="thin", color="000000"),
    bottom=Side(style="thin", color="000000"),
)

# Create a heading row DataFrame with column names
heading_row = pd.DataFrame(
    {
        "Brand": ["Brand"],
        "Current Time": ["Current Time"],
        "Portal": ["Portal"],
        "Total Order Qty": ["Total Order Qty"],
        "Total Order Amount (in Lacs)": ["Total Order Amount (in Lacs)"],
        "ASP": ["ASP"]
    }
)

# Create an empty DataFrame with three rows
empty_rows = pd.DataFrame({"": [""]}, index=range(1))

# * ----------------    All Brands Pivot    ----------------
# Loop through each unique brand
for brand in unique_brands:
    # Create a DataFrame with the current brand name
    brand_column = pd.DataFrame({"Brand": [brand]})

    # Check if the brand is "SKECHERS", "SAMSONITE" and "AMERICAN TOURISTER"
    if brand in ["SKECHERS", "SAMSONITE", "AMERICAN TOURISTER"]:
        # Skip to the next iteration if the brand is "SKECHERS", "SAMSONITE" and "AMERICAN TOURISTER"
        continue
    else:
        # For other brands, create a pivot table with order quantity and amount aggregated by Portal
        pivot_table = pd.pivot_table(
            sales_modified_df[sales_modified_df["Brand"] == brand],
            index="Portal",
            values=["Order Qty", "Order Amount"],
            aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
        ).reset_index()
        # Rename columns in the pivot table
        pivot_table = pivot_table.rename(
            columns={
                "Order Qty": "Total Order Qty",
                "Order Amount": "Total Order Amount (in Lacs)",
            }
        )
        pivot_table["ASP"] = (pivot_table["Total Order Amount (in Lacs)"] / pivot_table["Total Order Qty"]).round(2)
        total_order_qty = pivot_table["Total Order Qty"].sum()
        total_order_amount = pivot_table["Total Order Amount (in Lacs)"].sum()
        asp = total_order_amount / total_order_qty
        # Add the 'Total Order Amount (in Lacs)'
        pivot_table["Total Order Amount (in Lacs)"] = (
                pivot_table["Total Order Amount (in Lacs)"] / 100000
        ).round(2)

        # Calculate Total Order Qty and Total Order Amount
        total_order_qty = pivot_table["Total Order Qty"].sum()
        total_order_amount = pivot_table["Total Order Amount (in Lacs)"].sum()
        asp = round(asp, 2)
        # Create a DataFrame for the Total row
        total_row = pd.DataFrame(
            {
                "Portal": ["Total"],
                "Total Order Qty": [total_order_qty],
                "Total Order Amount (in Lacs)": [total_order_amount],
                "ASP": [asp]
            }
        )

        # Concatenate the Total row with the pivot table
        pivot_table = pd.concat([pivot_table, total_row], ignore_index=True)

    # Concatenate the brand name, current time, and pivot table horizontally
    first_conc = pd.concat([brand_column, time_column], axis=1)
    second_conc = pd.concat([first_conc, pivot_table], axis=1)

    # Concatenate the heading row, concatenated DataFrame, and empty rows vertically
    brand_time_pivot = pd.concat([heading_row, second_conc, empty_rows], axis=0)

    # Concatenate the brand's pivot table with the combined pivot table
    combined_pivot_table = pd.concat(
        [combined_pivot_table, brand_time_pivot], ignore_index=True
    )

# * ----------------    End of All Brands Pivot    ----------------

# * ----------------    Skechers, Skechers Apparels and Skechers Kidswear Pivot    ----------------
# Filter data for "SKECHERS", "SKECHERS APPARELS" and "SKECHERS KIDSWEAR"
skechers_df = sales_modified_df[
    (sales_modified_df["Brand"] == "SKECHERS")
    & (
        ~sales_modified_df["Category1"].isin(
            [
                "APPARELS MEN",
                "APPARELS WOMEN",
                "Baby",
                "Apparels",
                "FASHION ACCESSORIES",
            ]
        )
    )
    & (~sales_modified_df["SKU Desc"].str.contains("BOYS|GIRLS"))
    ]

# Create a pivot table for "SKECHERS"
skechers_pivot_table = pd.pivot_table(
    skechers_df,
    index="Portal",
    values=["Order Qty", "Order Amount"],
    aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
).reset_index()

# Rename columns in the "SKECHERS" pivot table
skechers_pivot_table = skechers_pivot_table.rename(
    columns={
        "Order Qty": "Total Order Qty",
        "Order Amount": "Total Order Amount (in Lacs)",
    }
)
skechers_pivot_table["ASP"] = (
            skechers_pivot_table["Total Order Amount (in Lacs)"] / skechers_pivot_table["Total Order Qty"]).round(2)

skechers_pivot_table["Total Order Amount (in Lacs)"] = (
        skechers_pivot_table["Total Order Amount (in Lacs)"] / 100000
).round(2)

# Filter data for "SKECHERS APPARELS"
skechers_apparels_df = sales_modified_df[
    (sales_modified_df["Brand"] == "SKECHERS")
    & (
        sales_modified_df["Category1"].isin(
            [
                "APPARELS MEN",
                "APPARELS WOMEN",
                "Baby",
                "Apparels",
                "FASHION ACCESSORIES",
            ]
        )
    )
    ]
if skechers_apparels_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    skechers_apparels_pivot_table = dummy_data
else:
    # Create a pivot table for "SKECHERS APPARELS"
    skechers_apparels_pivot_table = pd.pivot_table(
        skechers_apparels_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SKECHERS APPARELS" pivot table
    skechers_apparels_pivot_table = skechers_apparels_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    skechers_apparels_pivot_table["ASP"] = (
                skechers_apparels_pivot_table["Total Order Amount (in Lacs)"] / skechers_apparels_pivot_table[
            "Total Order Qty"]).round(2)

    skechers_apparels_pivot_table["Total Order Amount (in Lacs)"] = (
            skechers_apparels_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# Filter data for "SKECHERS KIDSWEAR"
skechers_kidswear_df = sales_modified_df[
    (sales_modified_df["Brand"] == "SKECHERS")
    & (sales_modified_df["Category1"] == "FOOTWEAR")
    & (sales_modified_df["SKU Desc"].str.contains("BOYS|GIRLS"))
    ]
if skechers_kidswear_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    skechers_kidswear_pivot_table = dummy_data
else:
    # Create a pivot table for "SKECHERS APPARELS"
    skechers_kidswear_pivot_table = pd.pivot_table(
        skechers_kidswear_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SKECHERS APPARELS" pivot table
    skechers_kidswear_pivot_table = skechers_kidswear_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    skechers_kidswear_pivot_table["ASP"] = (
                skechers_kidswear_pivot_table["Total Order Amount (in Lacs)"] / skechers_kidswear_pivot_table[
            "Total Order Qty"]).round(2)

    skechers_kidswear_pivot_table["Total Order Amount (in Lacs)"] = (
            skechers_kidswear_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# * ----------------    Samsonite and Samsonite Red Pivot    ----------------
# Filter data for "SAMSONITE"
samsonite_df = sales_modified_df[
    (sales_modified_df["Brand"] == "SAMSONITE")
    & (~sales_modified_df["SKU Desc"].str.contains("SAMSONITE RED"))
    ]
if samsonite_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    samsonite_pivot_table = dummy_data
else:
    # Create a pivot table for "SAMSONITE"
    samsonite_pivot_table = pd.pivot_table(
        samsonite_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SAMSONITE" pivot table
    samsonite_pivot_table = samsonite_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    samsonite_pivot_table["ASP"] = (
                samsonite_pivot_table["Total Order Amount (in Lacs)"] / samsonite_pivot_table["Total Order Qty"]).round(
        2)

    samsonite_pivot_table["Total Order Amount (in Lacs)"] = (
            samsonite_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# Filter data for "SAMSONITE RED"
samsonite_red_df = sales_modified_df[
    (sales_modified_df["Brand"] == "SAMSONITE")
    & (sales_modified_df["SKU Desc"].str.contains("SAMSONITE RED"))
    ]
if samsonite_red_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    samsonite_red_pivot_table = dummy_data
else:
    # Create a pivot table for "SAMSONITE"
    samsonite_red_pivot_table = pd.pivot_table(
        samsonite_red_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SAMSONITE" pivot table
    samsonite_red_pivot_table = samsonite_red_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    samsonite_red_pivot_table["ASP"] = (
                samsonite_red_pivot_table["Total Order Amount (in Lacs)"] / samsonite_red_pivot_table[
            "Total Order Qty"]).round(2)

    samsonite_red_pivot_table["Total Order Amount (in Lacs)"] = (
            samsonite_red_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# * ----------------    AT Backpack, AT Trolly bag and AT Duffle bag Pivot    ----------------
# Filter data for "AT Backpack"
at_backpack_df = sales_modified_df[
    (sales_modified_df["Brand"] == "AMERICAN TOURISTER")
    & (sales_modified_df["SKU Desc"].str.contains("BACKPACK"))
    ]
if at_backpack_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    at_backpack_pivot_table = dummy_data
else:
    # Create a pivot table for "SAMSONITE"
    at_backpack_pivot_table = pd.pivot_table(
        at_backpack_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SAMSONITE" pivot table
    at_backpack_pivot_table = at_backpack_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    at_backpack_pivot_table["ASP"] = (at_backpack_pivot_table["Total Order Amount (in Lacs)"] / at_backpack_pivot_table[
        "Total Order Qty"]).round(2)

    at_backpack_pivot_table["Total Order Amount (in Lacs)"] = (
            at_backpack_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# Filter data for "AT Trolly Bag"
at_trolly_bag_df = sales_modified_df[
    (sales_modified_df["Brand"] == "AMERICAN TOURISTER")
    & (sales_modified_df["SKU Desc"].str.contains("TROLLY BAG"))
    ]
if at_trolly_bag_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    at_trolly_bag_pivot_table = dummy_data
else:
    # Create a pivot table for "SAMSONITE"
    at_trolly_bag_pivot_table = pd.pivot_table(
        at_trolly_bag_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SAMSONITE" pivot table
    at_trolly_bag_pivot_table = at_trolly_bag_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    at_trolly_bag_pivot_table["ASP"] = (
                at_trolly_bag_pivot_table["Total Order Amount (in Lacs)"] / at_trolly_bag_pivot_table[
            "Total Order Qty"]).round(2)

    at_trolly_bag_pivot_table["Total Order Amount (in Lacs)"] = (
            at_trolly_bag_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# Filter data for "AT Duffle Bag"
at_duffle_bag_df = sales_modified_df[
    (sales_modified_df["Brand"] == "AMERICAN TOURISTER")
    & (sales_modified_df["SKU Desc"].str.contains("DUFFLE BAG"))
    ]
if at_duffle_bag_df.empty:
    # Create a dummy table with 0 values
    columns = [
        "Portal",
        "Total Order Qty",
        "Total Order Amount (in Lacs)",
        "ASP"
    ]
    dummy_data = pd.DataFrame([["ALL", 0, 0, 0]], columns=columns)
    at_duffle_bag_pivot_table = dummy_data
else:
    # Create a pivot table for "SAMSONITE"
    at_duffle_bag_pivot_table = pd.pivot_table(
        at_duffle_bag_df,
        index="Portal",
        values=["Order Qty", "Order Amount"],
        aggfunc={"Order Qty": "sum", "Order Amount": "sum"},
    ).reset_index()

    # Rename columns in the "SAMSONITE" pivot table
    at_duffle_bag_pivot_table = at_duffle_bag_pivot_table.rename(
        columns={
            "Order Qty": "Total Order Qty",
            "Order Amount": "Total Order Amount (in Lacs)",
        }
    )
    at_duffle_bag_pivot_table["ASP"] = (
                at_duffle_bag_pivot_table["Total Order Amount (in Lacs)"] / at_duffle_bag_pivot_table[
            "Total Order Qty"]).round(2)

    at_duffle_bag_pivot_table["Total Order Amount (in Lacs)"] = (
            at_duffle_bag_pivot_table["Total Order Amount (in Lacs)"] / 100000
    ).round(2)

# ! ---------------  (Total) Row for SKECHERS  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS
skechers_total_asp = skechers_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(skechers_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places
skechers_total_order_qty = skechers_pivot_table["Total Order Qty"].sum()
skechers_total_order_amount = skechers_pivot_table["Total Order Amount (in Lacs)"].sum()

# Create a DataFrame for the Total row for SKECHERS
skechers_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [skechers_total_order_qty],
        "Total Order Amount (in Lacs)": [skechers_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS pivot table
skechers_pivot_table = pd.concat(
    [skechers_pivot_table, skechers_total_row], ignore_index=True
)
# ! ---------------  (Total) Row for SKECHERS APPARELS  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS APPARELS
skechers_apparels_total_order_qty = skechers_apparels_pivot_table[
    "Total Order Qty"
].sum()
skechers_apparels_total_order_amount = skechers_apparels_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = skechers_apparels_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(skechers_apparels_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SKECHERS APPARELS
skechers_apparels_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [skechers_apparels_total_order_qty],
        "Total Order Amount (in Lacs)": [skechers_apparels_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS APPARELS pivot table
skechers_apparels_pivot_table = pd.concat(
    [skechers_apparels_pivot_table, skechers_apparels_total_row], ignore_index=True
)

# ! ---------------  (Total) Row for SKECHERS KIDSWEAR  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS APPARELS
skechers_kidswear_total_order_qty = skechers_kidswear_pivot_table[
    "Total Order Qty"
].sum()
skechers_kidswear_total_order_amount = skechers_kidswear_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = skechers_kidswear_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(skechers_kidswear_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SKECHERS APPARELS
skechers_kidswear_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [skechers_kidswear_total_order_qty],
        "Total Order Amount (in Lacs)": [skechers_kidswear_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS APPARELS pivot table
skechers_kidswear_pivot_table = pd.concat(
    [skechers_kidswear_pivot_table, skechers_kidswear_total_row], ignore_index=True
)
# ! ---------------  End of (Total) Rows  ---------------

# ! ---------------  (Total) Row for SAMSONITE  ---------------
# Calculate Total Order Qty and Total Order Amount for SAMSONITE
samsonite_total_order_qty = samsonite_pivot_table["Total Order Qty"].sum()
samsonite_total_order_amount = samsonite_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = samsonite_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(samsonite_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SAMSONITE
samsonite_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [samsonite_total_order_qty],
        "Total Order Amount (in Lacs)": [samsonite_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SAMSONITE pivot table
samsonite_pivot_table = pd.concat(
    [samsonite_pivot_table, samsonite_total_row], ignore_index=True
)

# ! ---------------  (Total) Row for SAMSONITE RED  ---------------
# Calculate Total Order Qty and Total Order Amount for SAMSONITE RED
samsonite_red_total_order_qty = samsonite_red_pivot_table["Total Order Qty"].sum()
samsonite_red_total_order_amount = samsonite_red_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = samsonite_red_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(samsonite_red_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SAMSONITE RED
samsonite_red_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [samsonite_red_total_order_qty],
        "Total Order Amount (in Lacs)": [samsonite_red_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SAMSONITE RED pivot table
samsonite_red_pivot_table = pd.concat(
    [samsonite_red_pivot_table, samsonite_red_total_row], ignore_index=True
)

# ! ---------------  (Total) Row for AT BACKPACK  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS APPARELS
at_backpack_total_order_qty = at_backpack_pivot_table["Total Order Qty"].sum()
at_backpack_total_order_amount = at_backpack_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = at_backpack_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(at_backpack_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SKECHERS APPARELS
at_backpack_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [at_backpack_total_order_qty],
        "Total Order Amount (in Lacs)": [at_backpack_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS APPARELS pivot table
at_backpack_pivot_table = pd.concat(
    [at_backpack_pivot_table, at_backpack_total_row], ignore_index=True
)

# ! ---------------  (Total) Row for AT TROLLY BAG  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS APPARELS
at_trolly_bag_total_order_qty = at_trolly_bag_pivot_table["Total Order Qty"].sum()
at_trolly_bag_total_order_amount = at_trolly_bag_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = at_trolly_bag_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(at_trolly_bag_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SKECHERS APPARELS
at_trolly_bag_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [at_trolly_bag_total_order_qty],
        "Total Order Amount (in Lacs)": [at_trolly_bag_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS APPARELS pivot table
at_trolly_bag_pivot_table = pd.concat(
    [at_trolly_bag_pivot_table, at_trolly_bag_total_row], ignore_index=True
)

# ! ---------------  (Total) Row for AT DUFFLE BAG  ---------------
# Calculate Total Order Qty and Total Order Amount for SKECHERS APPARELS
at_duffle_bag_total_order_qty = at_duffle_bag_pivot_table["Total Order Qty"].sum()
at_duffle_bag_total_order_amount = at_duffle_bag_pivot_table[
    "Total Order Amount (in Lacs)"
].sum()
skechers_total_asp = at_duffle_bag_pivot_table["ASP"].sum()  # Sum of the ASP column
number_of_entries = len(at_duffle_bag_pivot_table["ASP"])  # Number of entries in the ASP column

# Calculate the ASP as the sum of the ASP column divided by the number of entries
asp = skechers_total_asp / number_of_entries
asp = round(asp, 2)  # Round to 2 decimal places

# Create a DataFrame for the Total row for SKECHERS APPARELS
at_duffle_bag_total_row = pd.DataFrame(
    {
        "Portal": ["Total"],
        "Total Order Qty": [at_duffle_bag_total_order_qty],
        "Total Order Amount (in Lacs)": [at_duffle_bag_total_order_amount],
        "ASP": [asp]
    }
)

# Concatenate the Total row with the SKECHERS APPARELS pivot table
at_duffle_bag_pivot_table = pd.concat(
    [at_duffle_bag_pivot_table, at_duffle_bag_total_row], ignore_index=True
)

# ! "SKECHERS"
# Create brand and time columns for "SKECHERS" pivot table
skechers_brand_column = pd.DataFrame({"Brand": ["SKECHERS"]})
skechers_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS"
skechers_first_conc = pd.concat([skechers_brand_column, skechers_time_column], axis=1)
skechers_second_conc = pd.concat([skechers_first_conc, skechers_pivot_table], axis=1)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS"
skechers_brand_time_pivot = pd.concat(
    [heading_row, skechers_second_conc, empty_rows], axis=0
)
# ! "SKECHERS APPARELS"
# Create brand and time columns for "SKECHERS APPARELS" pivot table
skechers_apparels_brand_column = pd.DataFrame({"Brand": ["SKECHERS APPARELS"]})
skechers_apparels_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
skechers_apparels_first_conc = pd.concat(
    [skechers_apparels_brand_column, skechers_apparels_time_column], axis=1
)
skechers_apparels_second_conc = pd.concat(
    [skechers_apparels_first_conc, skechers_apparels_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
skechers_apparels_brand_time_pivot = pd.concat(
    [heading_row, skechers_apparels_second_conc, empty_rows], axis=0
)
# ! "SKECHERS KIDSWEAR"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
skechers_kidswear_brand_column = pd.DataFrame({"Brand": ["SKECHERS KIDS"]})
skechers_kidswear_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
skechers_kidswear_first_conc = pd.concat(
    [skechers_kidswear_brand_column, skechers_kidswear_time_column], axis=1
)
skechers_kidswear_second_conc = pd.concat(
    [skechers_kidswear_first_conc, skechers_kidswear_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
skechers_kidswear_brand_time_pivot = pd.concat(
    [heading_row, skechers_kidswear_second_conc, empty_rows], axis=0
)
# * ----------------    End of Skechers, Skechers Apparels and Skechers Kidswear Pivot    ----------------

# ! "SAMSONITE"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
samsonite_brand_column = pd.DataFrame({"Brand": ["SAMSONITE"]})
samsonite_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
samsonite_first_conc = pd.concat(
    [samsonite_brand_column, samsonite_time_column], axis=1
)
samsonite_second_conc = pd.concat([samsonite_first_conc, samsonite_pivot_table], axis=1)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
samsonite_brand_time_pivot = pd.concat(
    [heading_row, samsonite_second_conc, empty_rows], axis=0
)

# ! "SAMSONITE RED"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
samsonite_red_brand_column = pd.DataFrame({"Brand": ["SAMSONITE RED"]})
samsonite_red_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
samsonite_red_first_conc = pd.concat(
    [samsonite_red_brand_column, samsonite_red_time_column], axis=1
)
samsonite_red_second_conc = pd.concat(
    [samsonite_red_first_conc, samsonite_red_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
samsonite_red_brand_time_pivot = pd.concat(
    [heading_row, samsonite_red_second_conc, empty_rows], axis=0
)

# ! "AMERICAN TOURISTER BACKPACK"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
at_backpack_brand_column = pd.DataFrame({"Brand": ["AT BACKPACK"]})
at_backpack_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
at_backpack_first_conc = pd.concat(
    [at_backpack_brand_column, at_backpack_time_column], axis=1
)
at_backpack_second_conc = pd.concat(
    [at_backpack_first_conc, at_backpack_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
at_backpack_brand_time_pivot = pd.concat(
    [heading_row, at_backpack_second_conc, empty_rows], axis=0
)

# ! "AMERICAN TOURISTER TROLLY BAG"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
at_trolly_bag_brand_column = pd.DataFrame({"Brand": ["AT TROLLY BAG"]})
at_trolly_bag_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
at_trolly_bag_first_conc = pd.concat(
    [at_trolly_bag_brand_column, at_trolly_bag_time_column], axis=1
)
at_trolly_bag_second_conc = pd.concat(
    [at_trolly_bag_first_conc, at_trolly_bag_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
at_trolly_bag_brand_time_pivot = pd.concat(
    [heading_row, at_trolly_bag_second_conc, empty_rows], axis=0
)

# ! "AMERICAN TOURISTER DUFFLE BAG"
# Create brand and time columns for "SKECHERS KIDSWEAR" pivot table
at_duffle_bag_brand_column = pd.DataFrame({"Brand": ["AT DUFFLE BAG"]})
at_duffle_bag_time_column = pd.DataFrame({"Current Time": [current_time]})

# Concatenate brand, time, and pivot table dataframes for "SKECHERS APPARELS"
at_duffle_bag_first_conc = pd.concat(
    [at_duffle_bag_brand_column, at_duffle_bag_time_column], axis=1
)
at_duffle_bag_second_conc = pd.concat(
    [at_duffle_bag_first_conc, at_duffle_bag_pivot_table], axis=1
)

# Concatenate heading row, concatenated dataframes, and empty rows vertically for "SKECHERS APPARELS"
at_duffle_bag_brand_time_pivot = pd.concat(
    [heading_row, at_duffle_bag_second_conc, empty_rows], axis=0
)

# Concatenate the pivot tables for "SKECHERS" and "SKECHERS APPARELS" with the combined pivot table
combined_pivot_table = pd.concat(
    [
        combined_pivot_table,
        skechers_brand_time_pivot,
        skechers_apparels_brand_time_pivot,
        skechers_kidswear_brand_time_pivot,
        samsonite_brand_time_pivot,
        samsonite_red_brand_time_pivot,
        at_backpack_brand_time_pivot,
        at_trolly_bag_brand_time_pivot,
        at_duffle_bag_brand_time_pivot,
    ],
    ignore_index=True,
)

# * ----------------    All Portal Pivot    ----------------
all_portal_table = pd.pivot_table(
    sales_modified_df,
    values=["Order Qty", "Order Amount"],
    index="Portal",
    aggfunc={
        "Order Qty": "sum",
        "Order Amount": "sum",
    },
    margins=True,  # Include margins for totals
    margins_name="Total",  # Customize the name for the totals column
).rename(
    columns={
        "Order Qty": "Total Order Qty",
        "Order Amount": "Total Order Amount (in Lacs)",
    }
)
all_portal_table["Total Order Amount (in Lacs)"] = (
        all_portal_table["Total Order Amount (in Lacs)"] / 100000
).round(2)
# Reset the index of the pivot table
all_portal_table.reset_index(inplace=True)

all_portal_table = pd.concat(
    [
        time_column,
        all_portal_table,
    ],
    axis=1,
    ignore_index=True,
)
# Set column names
all_portal_table.columns = [
    "Current Time",
    "Portal",
    "Total Order Amount (in Lacs)",
    "Total Order Qty",
]
# * ----------------    End of All Portal Pivot    ----------------

# * ----------------    Warehouse Location Pivot    ----------------
location_pivot_table = pd.pivot_table(
    sales_modified_df,
    values="Order Qty",
    index="Portal",
    columns="WH",
    aggfunc="sum",
    margins=True,  # Include margins for totals
    margins_name="Total",  # Customize the name for the totals colum
)
# * ----------------    End of Warehouse Location Pivot    ----------------

# * ----------------    Brand - Location Pivot    ----------------
# Filter out rows where the Brand is "SKECHERS"
# filtered_sales_df = sales_modified_df[sales_modified_df["Brand"] != "SKECHERS"]

brand_location_pivot_table = pd.pivot_table(
    sales_modified_df,
    values="Order Qty",
    index="Brand",
    columns="WH",
    aggfunc="sum",
    margins=True,  # Include margins for totals
    margins_name="Total",  # Customize the name for the totals column
)

# # Create pivot tables for each category
# skechers_pivot = pd.pivot_table(
#     skechers_df,
#     values="Order Qty",
#     index=["Brand"],
#     columns="WH",
#     aggfunc="sum",
# )

# skechers_kidswear_pivot = pd.pivot_table(
#     skechers_kidswear_df,
#     values="Order Qty",
#     index=["Brand"],
#     columns="WH",
#     aggfunc="sum",
# )

# skechers_apparels_pivot = pd.pivot_table(
#     skechers_apparels_df,
#     values="Order Qty",
#     index=["Brand"],
#     columns="WH",
#     aggfunc="sum",
# )

# # Rename the indices for clarity
# skechers_pivot.index = ["SKECHERS"]
# skechers_kidswear_pivot.index = ["SKECHERS KIDSWEAR"]
# skechers_apparels_pivot.index = ["SKECHERS APPARELS"]

# # Concatenate the new rows with the main pivot table
# brand_location_pivot_table = pd.concat([
#     brand_location_pivot_table,
#     skechers_pivot,
#     skechers_kidswear_pivot,
#     skechers_apparels_pivot
# ])

# # Add total column
# brand_location_pivot_table['Total'] = brand_location_pivot_table.sum(axis=1)

# # Recompute the total row
# total_row = brand_location_pivot_table.sum(numeric_only=True).to_frame().T
# total_row.index = ['Total']

# # Append the total row to the DataFrame
# brand_location_pivot_table = pd.concat([brand_location_pivot_table, total_row])

# # Reset index to ensure 'Brand' is a normal column and avoid numeric indices
# brand_location_pivot_table = brand_location_pivot_table.reset_index()

# # Ensure the "Brand" column is renamed properly
# brand_location_pivot_table.rename(columns={'index': 'Brand'}, inplace=True)

# * ----------------    End of Brand - Location Pivot    ----------------

# Reset the index of the combined pivot table
combined_pivot_table.reset_index(drop=True, inplace=True)

all_portal_table_start_row = len(combined_pivot_table) + 1
location_table_start_row = len(combined_pivot_table) + len(all_portal_table) + 3
brand_location_table_start_row = (
        len(combined_pivot_table) + len(all_portal_table) + len(location_pivot_table) + 5
)

# Write the combined pivot table to an Excel file
with pd.ExcelWriter(
        "report_data/MIS_report.xlsx",
        engine="openpyxl",
        mode="w",
) as writer:
    # Remove the existing "For MIS" sheet if it exists
    if "For MIS" in writer.book.sheetnames:
        writer.book.remove(writer.book["For MIS"])  # Remove existing sheet if it exists

    combined_pivot_table.to_excel(
        writer,
        sheet_name="For MIS",
        index=False,
    )
    all_portal_table.to_excel(
        writer,
        sheet_name="For MIS",
        index=False,
        startrow=all_portal_table_start_row,
    )
    location_pivot_table.to_excel(
        writer,
        sheet_name="For MIS",
        startrow=location_table_start_row,
    )
    brand_location_pivot_table.to_excel(
        writer,
        sheet_name="For MIS",
        startrow=brand_location_table_start_row,
    )

workbook = load_workbook("report_data/MIS_report.xlsx")
sheet = workbook.active

# Remove the first row
sheet.delete_rows(1)

# Define the headers to be bolded
headers_to_bold = [
    "Brand",
    "Current Time",
    "Portal",
    "Total Order Qty",
    "Total Order Amount (in Lacs)",
    "ASP"

]

# Iterate over the rows in the sheet (up to row 60)
for row in sheet.iter_rows(min_row=1, max_row=100):
    for cell in row:
        # Check if the value in the cell matches any of the headers to be bolded
        if cell.value in headers_to_bold:
            cell.font = Font(bold=True)

# * Iterate C column check on every row where Portal is located in Bold get the row number
# * ----------    Brands Border    ----------
start_lst = []
for start, row in enumerate(sheet.iter_rows(min_col=3, max_col=3), start=1):
    # Check if the font of the cell in the "C" column is bold
    if row[0].value == "Portal" and row[0].font.bold:
        # If the "C" column is in bold, add the row number to the list
        start_lst.append(start)

end_lst = []
for end, row in enumerate(sheet.iter_rows(min_col=3, max_col=3), start=1):
    if "ASP" in str(row[0].value):
        break
    # Check if the cell in the "C" column is empty
    if row[0].value is None or (
            isinstance(row[0].value, str) and row[0].value.strip() == ""
    ):
        end_lst.append(end - 1)

pairs = [(start_lst[i], end_lst[i]) for i in range(len(start_lst))]

for pair in pairs:
    start_row, end_row = pair
    for row in sheet.iter_rows(
            min_row=start_row, max_row=end_row, min_col=1, max_col=5
    ):
        for cell in row:
            cell.border = border_style

# * ----------    All Portal Border    ----------
portal_table_start = 0
for start, row in enumerate(sheet.iter_rows(min_col=2, max_col=2), start=1):
    if row[0].value == "Portal" and row[0].font.bold:
        portal_table_start = start

for row in sheet.iter_rows(
        min_row=portal_table_start,
        max_row=portal_table_start
                + length_of_unique_portal,  # no. of row need to be border.
        min_col=1,
        max_col=4,
):
    for cell in row:
        cell.border = border_style

# * ----------    Warehouse Border    ----------
warehouse_location_table_start = 0
for start, row in enumerate(sheet.iter_rows(min_col=1, max_col=1), start=1):
    if row[0].value == "Portal" and row[0].font.bold:
        warehouse_location_table_start = start

for row in sheet.iter_rows(
        min_row=warehouse_location_table_start,
        max_row=warehouse_location_table_start
                + length_of_unique_portal,  # no. of row need to be border.
        min_col=1,
        max_col=8,
):
    for cell in row:
        cell.border = border_style
# * ----------    Warehouse Border    ----------
warehouse_location_table_start = 0
for start, row in enumerate(sheet.iter_rows(min_col=1, max_col=1), start=1):
    if row[0].value == "Brand" and row[0].font.bold:
        warehouse_location_table_start = start

for row in sheet.iter_rows(
        min_row=warehouse_location_table_start,
        max_row=warehouse_location_table_start
                + length_of_unique_brands,  # no. of row need to be border.
        min_col=1,
        max_col=8,
):
    for cell in row:
        cell.border = border_style

# * ----------  Auto-fit the columns  ----------
for col in sheet.columns:
    max_length = 0
    column = col[0].column_letter
    for cell in col:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2) * 1.2  # Adjusting the width for padding
    sheet.column_dimensions[column].width = adjusted_width

# Iterate through each row in column C
for row in sheet.iter_rows(min_row=1, min_col=3, max_col=3):
    for cell in row:
        if cell.value == "Total":
            # Apply bold font to each cell in the row
            for c in range(1, sheet.max_column + 1):
                sheet.cell(row=cell.row, column=c).font = openpyxl.styles.Font(
                    bold=True
                )
workbook.save("report_data/MIS_report.xlsx")
