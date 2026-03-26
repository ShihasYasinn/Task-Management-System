class APIResponse:
    @staticmethod
    def success(data=None, message="Success"):
        return {
            "status": True,
            "message": message,
            "data": data,
        }

    @staticmethod
    def error(message="Something went wrong", data=None):
        return {
            "status": False,
            "message": message,
            "data": data,
        }