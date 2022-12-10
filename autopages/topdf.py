from functools import lru_cache
import logging
from pathlib import Path

import docker

logger = logging.getLogger(__name__)


class DockerClientSingleton:
    """Singleton class to create a docker client

    This is a singleton class to create a docker client. It is used to
    create a docker client that can be used in the ppt_to_pdf function.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DockerClientSingleton, cls).__new__(cls)
            try:
                client = docker.from_env()
            except docker.api.client.DockerException:
                raise EnvironmentError(
                    """Docker is not running. Please start docker and try again.
                    """
                )
            cls._instance.client = client
        return cls._instance.client

    @lru_cache(maxsize=2)
    @staticmethod
    def image_check(image_name: str) -> bool:
        """Check if docker image exists and pull it if not

        :param image_name: name of the docker image
        """
        client = DockerClientSingleton()
        try:
            client.images.get(image_name)
            return True
        except docker.api.client.DockerException:
            logger.info("Pulling docker image for libreoffice ...")
            client.images.pull(image_name)
            client.images.get(image_name)
            return True


def ppt_to_pdf(ppt_file: str | Path):
    """Convert a powerpoint file to a pdf file

    This uses LibreOffice in a docker container, so it may take a while, especially
    initially. But it is the most robust method.
    See error messages for help.

    :param ppt_file: path to the powerpoint file

    """
    from pathlib import Path

    docker_image = (
        "linuxserver/libreoffice:latest"  # defaults to latest
    )
    client = DockerClientSingleton()
    DockerClientSingleton.image_check(docker_image)

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
        detach=True,
    )
    # container.stop()
    # logger.info("...converted")
