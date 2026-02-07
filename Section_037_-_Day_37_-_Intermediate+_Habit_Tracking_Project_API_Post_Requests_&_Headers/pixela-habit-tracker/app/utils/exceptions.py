class HabitTrackerError(Exception):
    pass


class ConfigurationError(HabitTrackerError):
    pass


class PixelaAPIError(HabitTrackerError):
    def __init__(self, message, status_code=None):
        self.status_code = status_code
        super().__init__(message)


class NetworkError(HabitTrackerError):
    pass
