import logging

logger = logging.getLogger("JSBuild")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(levelname)s - %(message)s")

ch.setFormatter(formatter)

logger.addHandler(ch)
