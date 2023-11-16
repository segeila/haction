import openai 

#OPENAI_API_KEY = "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"

from packaging import version

required_version = version.parse("1.1.1")
current_version = version.parse(openai.__version__)

if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__}"
                     " is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

def generate_image(topic):
    client = openai.OpenAI(api_key="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",)
    response = client.images.generate(
        model="dall-e-3",
        prompt=topic,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    return image_url