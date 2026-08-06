import os
import random
import traceback
import time

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from image_generator import PollinationsGenerator
from image_editor import ImageEditor
from facebook_publisher import FacebookPublisher
from knowledge import router as knowledge_router
from config import OUTPUT_DIR


app = FastAPI(
    title="Facebook Poster API",
    version="2.0.0"
)

app.include_router(knowledge_router)


# ----------------------------------------------------
# Request Model
# ----------------------------------------------------
class ImageRequest(BaseModel):
    prompt: str
    title: str
    subtitle: str
    caption: str


# ----------------------------------------------------
# Random Style
# ----------------------------------------------------
STYLES = [
    "photorealistic, 8k, cinematic lighting",
    "3d blender render, vibrant colors, soft lighting",
    "vector art, flat design, minimalist",
    "cyberpunk style, neon lights, futuristic",
    "digital painting, concept art, artstation",
    "isometric illustration, modern business office"
]


# ----------------------------------------------------
# Background Worker
# ----------------------------------------------------
def process_and_post_task(data: ImageRequest):

    try:

        print("\n" + "🏃 BACKGROUND TASK STARTED".center(60, "="))

        generator = PollinationsGenerator()
        editor = ImageEditor()
        publisher = FacebookPublisher()

        # Random style
        random_style = random.choice(STYLES)

        enhanced_prompt = f"{data.prompt}, {random_style}"

        print(f"✨ Prompt:\n{enhanced_prompt}")

        # -----------------------------------
        # Generate Image
        # -----------------------------------

        print("🎨 Generating Image...")

        start = time.time()

        generated_image = generator.generate(
        prompt=enhanced_prompt
        )
        print(f"✅ Image Generation Time: {time.time() - start:.2f} seconds")
        # -----------------------------------
        # Detect Hiring Post
        # -----------------------------------

        hiring_keywords = [

            "hiring",

            "hire",

            "hired",

            "job",

            "jobs",

            "career",

            "careers",

            "vacancy",

            "vacancies",

            "opening",

            "openings",

            "position",

            "positions",

            "apply",

            "apply now",

            "join us",

            "join our team",

            "join our company",

            "recruitment",

            "recruit",

            "staffing",

            "talent",

            "talent acquisition",

            "walk in",

            "walk-in",

            "interview"

    ]

        text = (
            data.title
            + " "
            + data.subtitle
            + " "
            + data.caption
        ).lower()

        is_hiring = any(
            word in text
            for word in hiring_keywords
        )

        print(f"WE ARE HIRING Badge : {is_hiring}")

        # -----------------------------------
        # Edit Image
        # -----------------------------------

        final_image = os.path.join(
            OUTPUT_DIR,
            "final_post.jpg"
        )

        print("🖌️ Editing Image...")

        start = time.time()
        editor.process_image(
        input_path=generated_image,
        output_path=final_image,
        title=data.title,
        subtitle=data.subtitle,
        hiring=data.hiring
)

        print(f"✅ Image Editing Time: {time.time() - start:.2f} seconds")

        # -----------------------------------
        # Hashtags
        # -----------------------------------

        hashtags = """

#XENHRA
#HRConsultancy
#Recruitment
#StaffingSolutions
#PayrollServices
#HRCompliance
#Coimbatore
#Hiring

"""

        final_caption = (
            data.caption.strip()
            + "\n"
            + hashtags
        )

        # -----------------------------------
        # Publish
        # -----------------------------------

        print("🚀 Publishing to Facebook...")

        start = time.time()
        fb_response = publisher.publish(
        image_path=final_image,
        caption=data.caption
        )
        print(f"✅ Facebook Upload Time: {time.time() - start:.2f} seconds")
        print(
            "🏁 BACKGROUND TASK FINISHED".center(60, "=")
        )

    except Exception:

        print(
            "\n"
            + "❌ BACKGROUND TASK FAILED".center(
                60,
                "="
            )
        )

        traceback.print_exc()

        print("=" * 60)


# ----------------------------------------------------
# Generate Endpoint
# ----------------------------------------------------
@app.post("/generate-image")
def generate_image(
    data: ImageRequest,
    background_tasks: BackgroundTasks
):

    print("=" * 60)

    print("⚡ Request Received")

    print("=" * 60)

    background_tasks.add_task(
        process_and_post_task,
        data
    )

    return {

        "status": "success",

        "message": "Post generation started."

    }


# ----------------------------------------------------
# Health
# ----------------------------------------------------
@app.get("/")
def home():

    return {

        "status": "running",

        "version": "2.0.0"

    }


@app.get("/health")
def health():

    return {

        "status": "healthy"

    }


# ----------------------------------------------------
# Run
# ----------------------------------------------------
if __name__ == "__main__":

    import uvicorn

    uvicorn.run(

        "app:app",

        host="127.0.0.1",

        port=8000,

        reload=True

    )
