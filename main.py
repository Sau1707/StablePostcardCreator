import os, io, cv2, random, warnings, logging
from dotenv import load_dotenv
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from postcard_creator.postcard_creator import PostcardCreator, Postcard, Token, Recipient, Sender
from generator import generateDescription
load_dotenv()
# Define consts 
FILENAME = "image.png"

# Define enviroment
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

# Load enviroment
STABILITY_KEY = os.getenv('STABILITY_KEY')
POSTCARD_USERNAME = os.getenv('POSTCARD_USERNAME')
POSTCARD_PASSWORD = os.getenv('POSTCARD_PASSWORD')

RECIPIENT_PRENAME  = os.getenv('RECIPIENT_PRENAME')
RECIPIENT_LASTNAME = os.getenv('RECIPIENT_LASTNAME')
RECIPIENT_STREET   = os.getenv('RECIPIENT_STREET')
RECIPIENT_PLACE    = os.getenv('RECIPIENT_PLACE')
RECIPIENT_ZIPCODE  = os.getenv('RECIPIENT_ZIPCODE')

SENDER_PRENAME  = os.getenv('SENDER_PRENAME')
SENDER_LASTNAME = os.getenv('SENDER_LASTNAME')
SENDER_STREET   = os.getenv('SENDER_STREET')
SENDER_PLACE    = os.getenv('SENDER_PLACE')
SENDER_ZIPCODE  = os.getenv('SENDER_ZIPCODE')

# Return a description for an epic image
class StablePostCard:
    def __init__(self):
        self.description = generateDescription()
        self.seed = random.randint(0, 992446758)
        self.token = Token()
        self.token.fetch_token(username=POSTCARD_USERNAME, password=POSTCARD_PASSWORD)
        self.postcard = PostcardCreator(self.token)
        self.stability_api = client.StabilityInference(key=STABILITY_KEY, verbose=True, engine="stable-diffusion-768-v2-1")

    def hasFreePostcard(self):
        return self.postcard.has_free_postcard()

    def generateImage(self):
        answers = self.stability_api.generate(
            prompt=self.description,
            seed=self.seed,
            steps=30,
            cfg_scale=8.0,
            width=1088,
            height=768,
            samples=1,
        )
    
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = Image.open(io.BytesIO(artifact.binary))
                    img.save(FILENAME)

    def scaleImage(self):
        input_image = cv2.imread(FILENAME)
        # height, width, channels = input_image.shape
        new_width = 1819
        new_height = 1311
        output_image = cv2.resize(input_image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(FILENAME, output_image)

    def sendPostcard(self, mock = False):
        if (not self.hasFreePostcard()):
            return
        recipient = Recipient(prename=RECIPIENT_PRENAME, lastname=RECIPIENT_LASTNAME, street=RECIPIENT_STREET, place=RECIPIENT_PLACE, zip_code=RECIPIENT_ZIPCODE)
        sender = Sender(prename=SENDER_PRENAME, lastname=SENDER_LASTNAME, street=SENDER_STREET, place=SENDER_PLACE, zip_code=SENDER_ZIPCODE)
        card = Postcard(message=self.description, recipient=recipient, sender=sender, picture_stream=open('./image.png', 'rb'))
        self.postcard.send_free_card(postcard=card, mock_send=mock, image_export=False)


logger = logging.getLogger('postcard_creator')

if __name__ == "__main__":
    bot = StablePostCard()
    if not bot.hasFreePostcard():
        print("The user has not a free postcard")
        exit()
    print(f"Generating image with prompt: {bot.description}")
    bot.generateImage()
    print("Scaling to postcard size")
    bot.scaleImage()
    print("Sending postcard")
    bot.sendPostcard()
    print("Done")

