# %%
import requests
from bs4 import BeautifulSoup

# Make a request to the website
url = "https://endocrinology.dk/nbv/diabetes-melitus/behandling-og-kontrol-af-type-2-diabetes/"
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# TODO: Create a function to loop through the headers.


def scrape_endo_guidelines(output_file_path: str):
    """
    Loop through the file
    """
    # Local header variables
    header_vars = ["h1", "h2", "h3"]
    if not isinstance(output_file_path, str):
        raise TypeError("output_file_path must be a string")
    with open(output_file_path, "w") as f:
        for header in soup.find_all(header_vars):
            for elem in header.next_siblings:
                if elem.name == header_vars[0]:
                    f.write(f"# {elem.get_text()}\n")
                elif elem.name == header_vars[1]:
                    f.write(f"## {elem.get_text()}\n")
                elif elem.name == header_vars[2]:
                    f.write(f"### {elem.get_text()}\n")
                elif (
                    elem.name == "p"
                    and elem.next_sibling
                    and elem.next_sibling.name == "p"
                ):
                    f.write(elem.get_text() + "\n")
                else:
                    f.write(elem.get_text() + "\n\n")
        print(f"Done scraping {url}.\n Saved to: {output_file}")


# %%
# Save the file to the designated filename
output_file = "../data/endocrinology_guidelines_type_2_diabetes.txt"
# Scrape given website
scrape_endo_guidelines(output_file)
