import pandas as pd
import numpy as np

# Load data
cig_data = pd.read_csv("/Users/sarinatan/Desktop/HLTH470hw3/data/The_Tax_Burden_on_Tobacco__1970-2019.csv")
cpi_data = pd.read_excel("/Users/sarinatan/Desktop/HLTH470hw3/data/historical-cpi-u-202501.xlsx", skiprows=11)

# Clean tobacco data
measure_map = {
    "Average Cost per pack": "cost_per_pack",
    "Cigarette Consumption (Pack Sales Per Capita)": "sales_per_capita",
    "Federal and State tax as a Percentage of Retail Price": "tax_percent",
    "Federal and State Tax per pack": "tax_dollar",
    "Gross Cigarette Tax Revenue": "tax_revenue",
    "State Tax per pack": "tax_state"
}

cig_data["measure"] = cig_data["SubMeasureDesc"].map(measure_map)
cig_data = cig_data.rename(columns={
    "LocationAbbr": "state_abb",
    "LocationDesc": "state",
    "Data_Value": "value"
})
cig_data = cig_data[["state_abb", "state", "Year", "value", "measure"]]

final_data = cig_data.pivot(index=["state", "Year"], columns="measure", values="value").reset_index()

# Clean CPI data
cpi_data = cpi_data.melt(id_vars=["Year"], value_vars=["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."],
                          var_name="month", value_name="index")
cpi_data = cpi_data.groupby("Year", as_index=False)["index"].mean()

# Form final dataset
final_data = final_data.merge(cpi_data, on="Year", how="left")
final_data["price_cpi"] = final_data["cost_per_pack"] * (218 / final_data["index"])

# Save output
final_data.to_csv("/Users/sarinatan/Desktop/HLTH470hw3/data/output/TaxBurden_Data.txt", sep="\t", index=False)
final_data.to_csv("/Users/sarinatan/Desktop/HLTH470hw3/data/output/TaxBurden_Data.csv")
