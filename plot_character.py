import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

def extract_table(url: str) -> list:
        response = requests.get(url)
        html_content = response.text

        # Step 2: Parse the Content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Check for tables in the document
        tables = soup.find_all('table')
        if not tables:
            print("No tables found in the document.")
            return None
        else:
            # Print the first table for inspection (you can remove this after confirming structure)
            print("Found tables, displaying the first table's HTML structure:")
            #print(tables[0].prettify())
            # Step 3: Extract Table Data from the First Table
            table = tables[0]  # Assuming the first table is the one we want
            data = []
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if len(columns) >= 3:
                    x = columns[0].get_text().strip()  # x-coordinate
                    y = columns[2].get_text().strip()  # y-coordinate
                    character = columns[1].get_text().strip()  # Extract character label
                    #print(f'this is x{x} and this is y {y}')
                    data.append([x, y, character])
            return data
    # Convert to DataFrame
def convert_to_dataframe(data: list) -> object:
    df = pd.DataFrame(data, columns=['x', 'y', 'character'])
    df['x'] = pd.to_numeric(df['x'], errors='coerce')  # Ensure x is numeric
    df['y'] = pd.to_numeric(df['y'], errors='coerce')  # Ensure y is numeric

    print(f'this is the data_frame{df}')
    return df
    # Step 4: Plot Characters at Each Coordinate
def plot_dataFrame(df: object):
    plt.figure(figsize=(10, 6))
    for _, row in df.iterrows():
        plt.text(row['x'], row['y'], row['character'], fontsize=12, ha='center', va='center')

    # Customize the plot
    plt.title("Character Plot Based on Coordinates")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")

    zoom_factor = 10  # Increase this factor to zoom out more
    x_min, x_max = df['x'].min() - zoom_factor, df['x'].max() + zoom_factor
    y_min, y_max = df['y'].min() - zoom_factor, df['y'].max() + zoom_factor
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)

    # Add a grid if needed
    plt.grid(which='both', linestyle='--', linewidth=0.5)
    plt.minorticks_on()

    plt.show()

def visualize_on_graph(url: str):
    table = extract_table(url)
    data_frame = convert_to_dataframe(table)
    plot_dataFrame(data_frame)

def main():
    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    visualize_on_graph(url)    

if __name__ == "__main__":
    main()