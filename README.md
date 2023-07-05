# autopages

Create multiple unique pdfs from a base pptx template and a list of data

## How to run

```bash
python -m autopages --help
```

### Examples

1. If the CSV has a column per page:

    e.g.

    ```csv
    Title for page 1,Title for page 2
    Chris Currin,Chris Currin
    Name,Name
    ```

    ```bash
    python -m autopages --template template.pptx --data data.csv --output report.pdf
    ```

    If you don't want the titles to appear on the pages, use the `--no-titles` flag or have the first row as blanks (e.g. `,,` for 3 pages).

2. If the CSV has a **row** per page:

    This requires **columns** to be specified.

    e.g.

    ```csv
    title,content
    Chris Currin,IndabaX & Imbizo
    Nerdy McNerdface,Big Nerd Ranch
    ```

    ```bash
    python -m autopages --template template.pptx --data data.csv --output report.pdf --single
    ```

## Dependencies

- Python 3.6+
- Docker (for generating pdfs) - <https://docs.docker.com/install/>

    Uses `docker` to run `libreoffice`. The previously supported alternative of using `win32com` only works on Windows.
