import logging
import threading
import time
from os import environ

import docker
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    format="%(asctime)s - %(name)s: %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger("inqdo watcher")


class InQdoWatcher(object):
    def __init__(self):
        self.init_docker()
        self.last_reload_thread = None
        self.reload_delay = float(environ.get("RELOAD_DELAY", 1.5))
        self.restart_timeout = int(environ.get("RESTART_TIMEOUT", 10))
        self.reload_containers = environ.get("RELOAD_CONTAINERS")

    def event_handler_factory(
        self, *args, patterns=["*.py", "*.ts", "*.js", "*.tsx"], ignore_directories=True, **kwargs
    ):
        event_handler = PatternMatchingEventHandler(
            *args, patterns=patterns, ignore_directories=ignore_directories, **kwargs
        )

        def on_any_event_callback(event):
            """
            Callback to react on any watchdog filesystem event.
            """
            containers = self.get_target_containers()
            if containers:
                if event.event_type == "modified":
                    directory = event.src_path.split("/")[2]
                    if directory in containers.keys():
                        self.reload_with_delay(containers[directory])

        event_handler.on_any_event = on_any_event_callback
        return event_handler

    def init_docker(self):
        """
        Initializes docker client with binded docker socket.
        """
        self.client = docker.DockerClient(base_url="unix://var/run/docker.sock")

    def get_target_containers(self):
        """
        Returns a docker container instance if exists, based on the RELOAD_CONTAINERS
        environment variable.
        Split on -dev for source directory.
        """
        container_ids = {}

        reload_containers = [x.strip() for x in self.reload_containers.split(",")]

        for container in reload_containers:
            container_ids[container.split("-dev")[0]] = self.client.containers.list(
                filters={"name": container}
            )
        return container_ids

    def reload_with_delay(self, containers):
        """
        Reloads conatiner with a delay based on RELOAD_DELAY enviroment variable.
        """

        def containers_reload():
            """
            Restarts given containers and reports any errors.
            """
            try:
                for container in containers:
                    logger.info("Reloading container: {0}".format(container.name))
                    container.restart(timeout=self.restart_timeout)
            except Exception as e:
                logger.error("Something went wrong while reloading: ")
                logger.error(e)

        if self.last_reload_thread:
            self.last_reload_thread.cancel()
        del self.last_reload_thread
        self.last_reload_thread = threading.Timer(self.reload_delay, containers_reload)
        self.last_reload_thread.start()

    def startWatcher(self):
        """
        Runs watchdog process to monitor file changes and reload container
        """

        observer = Observer()
        observer.schedule(self.event_handler_factory(), "/code", recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
