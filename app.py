# Resume Builder

# Name
# email
# Phone
# equcation
# exp
# skills


import streamlit as st
import requests
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

st.title("Resume Bulder")

name = st.text_input("Enter Your Name")
email = st.text_input("Enter Your Email")
phone = st.text_input("Enter Your Mobile No")

education = st.text_area("Enter Your Education")
project = st.text_area("Enter Your Project")
skills = st.text_area("Enter Your Skills")
exp = st.text_area("Enter Your Experience")

if st.button("Generate Resume"):
    if not name or not email or not phone or not exp or not project or not skills :
        st.warning("Please Fill All details")
    else:
        with st.spinner("Generation Resume...."):
            key = st.secrets["OPENROUTER_API_KEY"]
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization":f"Bearer {key}",
                "Content-Type":"application/json"
            }
            body={
                "model":"openai/gpt-4o-mini",
                "messages":[
                    {
                        "role":"user",
                        "content":f"Create a Professional Fresher resume . name:{name} , email:{email} , phone:{phone} , Education:{education} , Skills:{skills} , project:{project} ,experience:{exp} Generate A professinal Resume . Do not invent any information . Use Clear headings and bullts poins"
                    }
                ]
            }

            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=body,
                    timeout=60
                    )
                response.raise_for_status()
                # Server Statur
                data = response.json()
                result = data["choices"][0]["message"]["content"]
                result = result.replace("#", "*")
                st.success("Resume Generated Sucessfully")
                st.markdown(result)

                # Generate PDF

                pdfBuffer = BytesIO()

                pdf = canvas.Canvas(
                    pdfBuffer,
                    pagesize=A4
                )

                width , height = A4
                y = height - 50

                pdf.setFont("Helvetica-Bold" , 16)
                pdf.drawString(50,y,name)

                y -= 10

                pdf.setFont("Helvetica-Bold" , 10)
                test = f"Email : {email} | Phone : {phone}"
                pdf.drawString(50 , y , test)

                y -= 10

                pdf.setFont("Helvetica-Bold" , 10)

                for line in result.split("\n"):
                    if y < 50 :
                        pdf.showPage()
                        y = height - 50
                        pdf.setFont("Helvetica-Bold" , 10)
                    line = line
                    if line.split():
                        pdf.drawString(50,y,line[:100])

                    y -= 20
                pdf.save()
                pdfBuffer.seek(0)

                st.download_button(
                    label="Download CV in PDF",
                    data=pdfBuffer,
                    file_name="My CV",
                    mime="application/pdf"
                )
                    
            except Exception as e:
                st.error(e)