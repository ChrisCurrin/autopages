import logging
from pathlib import Path

import docker

logger = logging.getLogger(__name__)


def ppt_to_pdf(ppt_file: str | Path):
    """Convert a powerpoint file to a pdf file

    This uses LibreOffice in a docker container, so it may take a while, especially
    initially. But it is the most robust method.
    See error messages for help.

    :param ppt_file: path to the powerpoint file

    """
    from pathlib import Path

    docker_image = "linuxserver/libreoffice:amd64-6.4.6.2-r2-ls2"  # defaults to latest

    try:
        client = docker.from_env()
    except docker.api.client.DockerException:
        raise EnvironmentError(
            """Docker is not running. Please start docker and try again.
            """
        )

    # check if libreoffice docker image exists and pull it if not
    try:
        client.images.get(docker_image)
    except docker.api.client.DockerException:
        logger.info("Pulling docker image for libreoffice ...")
        client.images.pull(docker_image)

    # get the full path to the folder. As string for key specifying docker volume.
    ppt_folder = str(Path(ppt_file).parent.absolute())
    # remove the rest of the path
    ppt_file = Path(ppt_file).name

    # use libreoffice
    logger.info(
        "converting powerpoint to pdf using LibreOffice docker container..."
    )

    container = client.containers.run(
        "linuxserver/libreoffice:latest",
        f"libreoffice --headless --convert-to pdf {ppt_file}",
        volumes={ppt_folder: {"bind": "/tmp/ppttopdf", "mode": "rw"}},
        working_dir="/tmp/ppttopdf",
        auto_remove=True,
    )
    container.stop()
    logger.info("...converted")
