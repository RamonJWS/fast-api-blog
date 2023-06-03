from fastapi import UploadFile


class MLHandler:
    def __init__(self):
        self.nsfw: bool = False
        self.prob: float = 0.0
        self.model_name: str = ""
        self.model_type: str = ""

    def load_model(self) -> None:
        pass

    def make_prediction_image(self, image: UploadFile) -> None:
        self.model_type = "Image"
        pass

    def make_prediction_content(self, context: str) -> None:
        self.model_type = "Context"
        pass
