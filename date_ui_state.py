import datetime
from dataclasses import dataclass, field


@dataclass()
class DataUiState:
    def __init__(
            self,
            timeout: int = 30,
            num_to_process: int | None = None,
            month_start: int = datetime.datetime.month,
            year_start: int = datetime.datetime.year
    ) -> None:
        self.timeout = timeout
        self.num_to_process = num_to_process
        self.month_start = month_start
        self.year_start = year_start
