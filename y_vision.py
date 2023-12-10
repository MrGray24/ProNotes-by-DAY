# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import pandas as pd


def detect_document(uploaded_file):
    """Detects document features in an image."""

    client = vision.ImageAnnotatorClient()

    content = uploaded_file.read()

    # with open(path, "rb") as image_file:
    #     print(type(image_file))
    #     content = image_file.read()
    #     print(type(content))

    image = vision_v1.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    df = pd.DataFrame(columns=["locale","description"])
    for text in texts:
        df = pd.concat([df, pd.DataFrame([
            dict(
                locale = text.locale,
                description = text.description
            )])],
            ignore_index=True
        )

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    result = df["description"][0]
    return result

if __name__ == "__main__":
    # detect_document("./handwriting2.jpg")
    pass