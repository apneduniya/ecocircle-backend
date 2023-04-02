from fastapi import FastAPI
import uvicorn
import csv
import datetime
import random
# from typing import List
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)


class EmailSchema(BaseModel):
    email: list[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME ="pythoncsvproject@gmail.com",
    MAIL_PASSWORD = "vaydiqkckumbvmof",
    MAIL_FROM = "pythoncsvproject@email.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


def get_important_days():
    now = datetime.datetime.now()
    month = now.strftime("%B") # returns the full month name
    date = now.strftime("%d") # returns the day of the month as a zero-padded decimal number

    data: list= []
    with open(r"backend/Scripts/important_days.csv", "r") as cf:
        csvFile = csv.reader(cf)
        for line in csvFile:
            line_list = list(line)
            if month == str(line_list[0]) and date == int(line_list[1]):
                data.extend(line_list)
    cf.close()

    quotes: list= []

    if not data:
        with open(r"backend/Scripts/quotes.csv", "r") as cf:
            csvFile = csv.reader(cf)
            for line in csvFile:
                line_list = list(line)
                quotes.append(line_list)
        cf.close()
        data.extend(random.choice(quotes))
        # data.extend(quotes)
 
    # displaying the contents of the CSV file
    return data


@app.get("/")
async def root():
    return {"data": "welcome to EcoCircle!!"}


@app.get("/get_quote")
async def get_quote():
    data = get_important_days()
    return {"data": data}


@app.get("/products")
async def get_products():
    data = [
            {
                "id": 1,
                "productName": "Recycled Bells",
                "productDetails": "Made from fabric waste which would otherwise be thrown in landfills, here is the star product colourful bells to brighten up your space, that our team has handcrafted with a lot of love. ",
                "productImg": "https://saahaszerowaste.com/wp-content/uploads/2021/08/IMG_E4827-300x3001-1.webp",
                "productExchangeRequirement": "4pcs X-size Fabric clothes",
            },
            {
                "id": 2,
                "productName": "Eco Photo Frame",
                "productDetails": "These photoframes are made from eco-boards. Eco-boards are excellent alternatives to plywood and are made of recycled multi-layer single use plastics majorly used in packaging by the FMCG and pharma companies. Eco-boards are corrosion proof, fire proof, water proof and termite resistant.",
                "productImg": "https://saahaszerowaste.com/wp-content/uploads/2019/11/Photo_frame_side.jpg",
                "productExchangeRequirement": "0.3kg papers",
            },
            {
                "id": 3,
                "productName": "Hardbound Diary A5",
                "productDetails": "This recycled paper consumes only 25% of the electrical power and only 1/3rd of the thermal energy as compared to virgin paper.",
                "productImg": "https://saahaszerowaste.com/wp-content/uploads/2017/01/hardbound-diary-a5-350x350.jpg",
                "productExchangeRequirement": "5kg papers",
            },
            {
                "id": 4,
                "productName": "Eco Board Planter",
                "productDetails": "These planters are made from eco-boards. Eco-boards are excellent alternatives to plywood and are made of recycled multi-layer single use plastics majorly used in packaging by the FMCG and pharma companies. Eco-boards are corrosion proof, fire proof, water proof and termite resistant.",
                "productImg": "https://saahaszerowaste.com/wp-content/uploads/2022/11/ECO-BOARD-PLANTER2.jpg",
                "productExchangeRequirement": "2pcs Eco boards",
            },
            {
                "id": 5,
                "productName": "Recycled Napkins",
                "productDetails": " Our tissues are unbleached (hence the brown colour), thus saving a lot of water that would be required for the bleaching process. When buying tissues, choose tree-free, recycled paper!",
                "productImg": "https://saahaszerowaste.com/wp-content/uploads/2021/08/Napkin_1.jpeg",
                "productExchangeRequirement": "0.5kg papers",
            },
        ]
    return data


@app.post("/mail/{email}")
async def post_order(email: str):
    quotes: list= get_important_days()

#     <p>Thanks for ordering from EcoCircle</p> 
# <p>With every order we get, we plant a plant in there's name 😉🙃</p>

    html = f"""
<h4>{quotes[0]}</h4>
<h5>- By {quotes[1]}</h5>
"""
    message = MessageSchema(
        subject="Quotes from Eco Circle",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})     


# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)