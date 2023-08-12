class data_ui_state:
    def __init__(
            self,
            timeout: int = 30,
            num_to_process: int|None = None
        ) -> None:
        self.timeout = timeout
        self.num_to_process = num_to_process