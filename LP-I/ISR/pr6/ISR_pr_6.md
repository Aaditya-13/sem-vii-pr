# ISR Practical 6: Simple Static Website Search

## Aim

Create a few static HTML pages and search their text for a keyword using Python.

## How the code works

1. **Imports:** `os` creates and lists files; BeautifulSoup extracts readable text from HTML.
2. **Create website folder:** `os.makedirs("website", exist_ok=True)` creates the folder if it does not exist.
3. **Create sample pages:** The `pages` dictionary contains three HTML snippets. A loop writes each one to a file inside `website`.
4. **Get a query:** The program asks for a keyword and lowercases it so the search ignores capitalization.
5. **Search pages:** `os.listdir("website")` gets filenames from the website folder. Each file is opened, parsed, and converted to plain text. If the keyword occurs in that text, the page name, first heading, and relative link are printed.
6. **No matches:** If no page contains the keyword, it prints `No results found!`.

## Example

Typing `python` finds `python.html` because its text contains â€œPython is a programming language.â€ The search is a substring check, so it searches page text directly.

## Run

Install BeautifulSoup with `python -m pip install beautifulsoup4`. Run `python ISR_pr_6.py` from the folder where the script is located; the relative path `website` is resolved from the current working directory.

## Note


## Code with explanation

### Create the website files

    os.makedirs("website", exist_ok=True)
    pages = {
        "python.html": "<h1>Python</h1><p>Python is a programming language.</p>",
        "java.html": "<h1>Java</h1><p>Java is used for application development.</p>",
        "ai.html": "<h1>Artificial Intelligence</h1><p>AI uses machine learning.</p>"
    }

os.makedirs creates the directory if needed. pages maps each filename to HTML content.

    for name, content in pages.items():
        with open("website/" + name, "w") as f:
            f.write(content)

items() provides each filename and content pair. open with w creates or replaces the file. write saves the HTML. As written, this program creates the sample pages itself before searching.

### Get the search word

    keyword = input("Enter search keyword: ").lower()
    found = False

input waits for a keyword. lower makes it lowercase so capitalization will not affect the search. found tracks whether any page matches.

### Read each page and search its text

    for file in os.listdir("website"):
        with open("website/" + file) as f:
            soup = BeautifulSoup(f, "html.parser")
            text = soup.get_text().lower()

os.listdir returns filenames in website. The loop opens each file. BeautifulSoup parses HTML; get_text removes tags and returns readable text. lower makes the comparison case-insensitive.

    if keyword in text:
        print("Page:", file)
        print("Title:", soup.h1.text)
        print("Link:", "website/" + file)
        print("----------------")
        found = True

This checks whether the keyword appears in the page text. If it does, the program prints the filename, first h1 title, and relative link, then records that a match was found.

### No results

    if not found:
        print("No results found!")

This runs only if no page matched.

### Example and path

If the user types python, the Python page matches and its title is printed. website is relative to the current working directory, so run the script from the folder containing both the script and website directory.

