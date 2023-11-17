# DEA scraper: A web scraper for national diabetes guidelines
This tool is a simple python scraper to extract data from Danish Endocrinology Society.

The tool will scrape all the national guidelines related to diabetes. The output will be
saved as standalone files in the `data` folder. Each chapter of the guideline is saved 
as a text file.

To run the file:

```bash
python scripts/endocrin_scraper.py
```

You can update where to scrape the guidelines in `endocrin_scraper.py` by updating the last lines.