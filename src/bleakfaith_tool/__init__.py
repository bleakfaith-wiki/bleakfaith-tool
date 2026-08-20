import logging

log = logging.getLogger(__name__)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    log.info("Hello from bleakfaith-tool!")
