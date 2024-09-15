import subprocess
import sys
import logging

from config.config import setup_logging

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


def start_broker(broker_name: str) -> subprocess.Popen:
    cmd = [
        sys.executable,
        "-m",
        "taskiq",
        "worker",
        f"src.brokers.{broker_name}:{broker_name}_broker",
    ]
    try:
        logger.info(f"Starting broker: {broker_name}")
        process = subprocess.Popen(cmd)
        return process
    except RuntimeError as e:
        logger.error(f"RuntimeError occurred while starting broker {broker_name}: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise


def main():
    brokers = ["meals", "health", "supps"]  # List of brokers
    broker_processes = []

    # Start all brokers
    for broker in brokers:
        try:
            process = start_broker(broker)
            broker_processes.append(process)
        except RuntimeError:
            logger.error(f"Failed to start broker {broker}.")
            # Optionally handle specific broker failure logic here

    # Start the event listener
    logger.info("Starting event listener")
    try:
        cmd = [sys.executable, "src/event_listener.py"]
        event_listener_process = subprocess.Popen(cmd)

        # Wait for the event listener process to finish
        event_listener_process.wait()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received. Terminating brokers...")
        for process in broker_processes:
            process.terminate()
        logger.info("Brokers terminated.")
    except RuntimeError as e:
        logger.error(f"RuntimeError occurred: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        # Ensure all brokers are terminated
        for process in broker_processes:
            if process.poll() is None:  # Check if process is still running
                process.terminate()
        logger.info("Cleaned up all brokers.")


if __name__ == "__main__":
    main()
