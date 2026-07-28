from concurrent.futures import ThreadPoolExecutor


class WorkerManager:
    """
    Central thread pool used for background processing.
    """

    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)


worker_manager = WorkerManager()