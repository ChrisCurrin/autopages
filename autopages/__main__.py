import argparse
import json
import logging
from pathlib import Path

from autopages.ppt import create_ppt
from autopages.topdf import ppt_to_pdf


logger = logging.getLogger(__name__)


def parse_args():
    """Setup the input and output arguments for the script
    Return the parsed input and output files
    """
    parser = argparse.ArgumentParser(
        description="Create pdf documents from json data and a pptx template"
    )

    parser.add_argument(
        "data",
        type=argparse.FileType("r"),
        help="file with the data",
    )
    parser.add_argument(
        "template",
        type=argparse.FileType("r"),
        help="Powerpoint file used as the template",
    )

    parser.add_argument(
        "outfile",
        help="Output powerpoint report file",
    )
    # add single-doc flag
    parser.add_argument(
        "-s",
        "--single",
        action="store_true",
        help="Create a single document instead of one document per data item",
    )
    # add convert flag
    parser.add_argument(
        "-c",
        "--convert",
        action="store_true",
        help="Convert the report to a pdf file. Can be omitted"
        " if the outfile ends with 'pdf'",
    )
    # add delete flag
    parser.add_argument(
        "-rm",
        "--delete",
        action="store_true",
        help="Delete the pptx file after converting to pdf",
    )
    return parser.parse_args()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    args = parse_args()

    template_name = Path(args.template.name).resolve()

    all_data: list[dict[str, dict[str, str]] | dict[str, str]]

    if args.data.name.endswith(".json"):
        # read json file
        try:
            all_data = json.loads(args.data.read())
        except json.JSONDecodeError as e:
            logger.error(f"Error reading json file: {e}")
            exit(1)
    elif args.data.name.endswith(".csv"):
        import pandas as pd

        # read csv file
        try:
            all_data = pd.read_csv(args.data.name, sep=",").to_dict(
                orient="records"
            )  # type: ignore
        except pd.errors.ParserError as e:
            logger.error(f"Error reading csv file: {e}")
            exit(1)
    else:
        logger.error(
            f"Unknown file extension: {args.data.name}. Only json and csv are supported"
        )
        exit(1)

    output_name = str(args.outfile)

    convert = args.convert

    if output_name.endswith(".pdf"):
        output_name = output_name[:-4]
        convert = True

    if not str(output_name).endswith(".pptx"):
        output_name = f"{output_name}.pptx"

    if args.single:
        # convert all_data list to dict where key is the value for the "Title" key
        # check if "Title" is in the data
        if "title" not in all_data[0]:
            logger.error(
                "Single document mode requires the data to have a 'title' key"
            )
            exit(1)
        all_data = [{data["title"]: data for data in all_data}]

    for i, data in enumerate(all_data):
        output_name_item = (
            output_name.replace(".pptx", f"_{i}.pptx")
            if "output" not in data
            else output_name
        )
        # create the ppt file
        create_ppt(
            template_name,
            output_name_item,
            data,
        )

        # convert to pdf if needed and delete ppt file afterwards (optional)
        if convert:
            ppt_to_pdf(output_name_item)
            if args.delete:
                Path(output_name_item).unlink(missing_ok=True)
