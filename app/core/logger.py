import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("customer_agent")


def section(title: str):
    logger.info("=" * 80)
    logger.info(title)
    logger.info("=" * 80)


def thought(text: str):
    logger.info(f"🧠 THOUGHT     | {text}")


def action(text: str):
    logger.info(f"⚙️ ACTION      | {text}")


def observation(text: str):
    logger.info(f"👀 OBSERVATION | {text}")


def success(text: str):
    logger.info(f"✅ SUCCESS     | {text}")


def warning(text: str):
    logger.warning(f"⚠️ WARNING     | {text}")


def error(text: str):
    logger.error(f"❌ ERROR       | {text}")