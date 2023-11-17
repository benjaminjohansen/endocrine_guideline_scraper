import requests
from bs4 import BeautifulSoup

## Helper functions
### Define a translational dict
translate_dict = {
    "æ": "ae",
    "ø": "oe",
    "å": "aa",
    "Æ": "AE",
    "Ø": "OE",
    "Å": "AA",
}


def check_list(list_of_urls: list):
    """
    This helper function test if a given list is a) not empty and b) contains three elements.
    A warning is raised if there's empty elements in the list elements.
    """
    # Assert that the list is not empty
    assert list_of_urls, "The list is empty."

    # Assert that each item in the list has exactly three values and none of them are empty
    for i, item in enumerate(list_of_urls):
        assert len(item) == 3, f"Row {i} does not have exactly three values."
        empty_values = [j for j, value in enumerate(item, start=1) if not value]
        assert (
            not empty_values
        ), f"Row {i} has empty values at positions {empty_values}."


## Main function
### Get all guidelins
def create_list_of_urls(url_to_scrape: str):
    """
    Creates a list of urls from a website containing three elements

    Input
    url_to_scrape(str):             A url string to scrape

    Output
    url_header_filename_list(list): A list containing elements with three elements:
                                    url:        of the subpage
                                    header:     the header name of the list
                                    filename:   the converted filename of the list in
                                                as lower case, with underscores and with
                                                Danish letters subbed with latin letters.
    """

    assert url_to_scrape, "You entered an empty string, please enter a valid url"
    main_url = url_to_scrape
    # main_url = "https://endocrinology.dk/nbv/diabetes-melitus/"

    main_response = requests.get(main_url)

    main_soup = BeautifulSoup(main_response.content, "html.parser")

    # Create a set to store the URLs. Set's are imutabel and great for the task.
    url_set = set()

    # Create a list to store the sets in
    url_header_filename_list = []

    # Select all <a> tags with class "elementor-sub-item"
    links = main_soup.select("a.elementor-sub-item")

    # Now "links" is a list of all <a> tags with the class "elementor-sub-item"
    # Iterate over each link and extract the url, the header and convert the header to
    # a filename.
    for link in links:
        url = link.get("href")
        # The text describing the link will be the header for the document.
        header = link.text  # or link.get_text()
        # Convert the header text into snake_case
        file_name = link.text.lower().replace(" ", "_").replace(".", "")
        # print(url, text)

        # Clean up file names
        for source, translate in translate_dict.items():
            file_name = file_name.replace(source, translate)

        # Limit the search to only contain the NBV's related to diabetes melitus
        # Check if the URL starts with "https://endocrinology.dk/nbv/diabetes-melitus/"
        # and is not equal to "https://endocrinology.dk/nbv/diabetes-melitus/"
        if (
            url.startswith("https://endocrinology.dk/nbv/diabetes-melitus/")
            and url != "https://endocrinology.dk/nbv/diabetes-melitus/"
        ):
            # Add the URL to the set
            if url not in url_set:
                url_set.add(url)
                # print(url, header, file_name)
                # Add the URL and text to the list
                url_header_filename_list.append((url, header, file_name))

    return url_header_filename_list


## Scraping each guideline
def scrape_guidelines(list_of_guidelines: list, output_directory: str):
    """
    Scrapes all guidelines from the Danish endocrine society given a list with URL's,
    headers and file names.
    Returns a file writen with the filenames.
    input
    list_of_guidelines(list):   A list containing three items:
                                URL of the page
                                The header as text (will be inserted into the document)
                                The filename that the output file should be saved as
    output_directory(str):      Where directory where the files are saved

    output
    A file      :   A file named after the filename containing all the text from a guideline.
    """
    header_vars = ["h1", "h2", "h3"]

    for guideline in list_of_guidelines:
        # get the url from the guideline
        url = guideline[0]
        # create a html request
        response = requests.get(url)
        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # output_file = "../data/endocrinology_guidelines_type_2_diabetes.txt"
        output_file = f"{output_directory}/{guideline[2]}.txt"

        with open(output_file, "w") as f:
            # Write the header guideline as level 1
            f.write(f"#{guideline[1]}\n")
            # Otherwise traverse through all headers and write to the file
            for header in soup.find_all(header_vars):
                for elem in header.next_siblings:
                    if elem.name == header_vars[0]:
                        f.write(f"# {elem.get_text()}\n")
                    elif elem.name == header_vars[1]:
                        f.write(f"## {elem.get_text()}\n")
                    elif elem.name == header_vars[2]:
                        f.write(f"### {elem.get_text()}\n")
                    # Write the paragraphs, if it is not the last paragraph, write it out
                    elif (
                        elem.name == "p"
                        and elem.next_sibling
                        and elem.next_sibling.name == "p"
                    ):
                        f.write(elem.get_text() + "\n")
                    else:
                        f.write(elem.get_text() + "\n\n")

    print(f"Wrote {len(list_of_guidelines)} guidelines to {output_directory}.")


## Main script
danish_endocrinology_url = "https://endocrinology.dk/nbv/diabetes-melitus/"
output_directory_path = "/home/benleb/pySurvive/data"
url_header_filename_list = create_list_of_urls(url_to_scrape=danish_endocrinology_url)
scrape_guidelines(
    list_of_guidelines=url_header_filename_list, output_directory=output_directory_path
)
