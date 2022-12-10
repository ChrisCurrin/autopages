# autopages
Create multiple unique pdfs from a base pptx template and a list of data

## How to run

```python
python -m autopages --help
```


## Dependencies
- Python 3.6+
- Docker (for generating pdfs) - https://docs.docker.com/install/

    Uses `docker` to run `libreoffice`. The previously supported alternative of using `win32com` only works on Windows.
