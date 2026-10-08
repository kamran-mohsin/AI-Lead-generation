import streamlit as st
import findClients
from dotenv import load_dotenv
import os
from groq import Groq
st.title("AI Lead generation")
st.subheader("Our services")
services = [
    "web development",
    "AI Automation",
    "Content writing",
    "Copy writing",
    "Graphic Design",
    "Logo design",
    "Thumbnail design",
    "Poster design",
    "T-shirt design",
]
st.write(services)
options = ", ".join(services)
word = [s.lower() for s in services]
service = st.text_input("Enter a service:")
if service.lower() in word:
    city = st.text_input("Enter a city:")
    businessType = st.text_input("Enter business type:")
    if st.button('Fetch details'):
     st.write(
        f"You want to find {service} clients in {city} and business type is {businessType}"
     )
     st.write("."*20)
     target = {"Service": service, "City": city, "Type": businessType}
     info = f'{businessType} in {city} ("contact" OR "email" OR "phone" OR "+92")'
     search=findClients.findClients(info)
     for score in search:
        if score['phone'] is not None  and score['email'] is not None and score['Website'] is not None:
          st.write(f"Score:10/10")
          st.write(f"Status: Strong {businessType} lead \nQualifyClient:Yes Sure")
        elif score['phone'] is None and score['email'] is not None and score['Website'] is not None:
           st.write(f"Score:8/10 \n Status: Best {businessType} lead \n QualifyClient:Yes")
        elif score['phone'] is not None and score['email'] is None and score['Website'] is not None:
           st.write(f"Score:7/10 \n Status: Good {businessType} lead \n QualifyClient:OK")
        elif score['phone'] is not None and score['email'] is not None and score['Website'] is None:
           st.write(f"Score:5/10 \n Status: weak {businessType} lead \n QualifyClient:Yes, For Web service")
        else:
             st.write( f"Status: No leads found for this search \n QualifyClient:No")
        st.write("="*45)
    #File I/O
        a=""
        for key,value in score.items():
         b=f"Service:{service}\nComapny:{businessType}\n"
         a += (f"{key}:{value}\n")
    #Data store
        with open("data.txt","a") as f:
         f.write(b)
         f.write(f"{a}")
         f.write("="*40+"\n")
    #Pitch email
     if score['phone'] is not None  and score['email'] is not None and score['Website'] is not None or score['phone'] is not None and score['email'] is None and score['Website'] is not None or score['phone'] is None and score['email'] is not None and score['Website'] is not None or score['phone'] is not None and score['email'] is not None and score['Website'] is None:
        load_dotenv()
        api=os.getenv("API")
        client = Groq(api_key=api ) 
        chat=client.chat.completions.create(
        messages=[
                {"role":"user",
                 "content":f"Write a short professional cold email for {businessType} offering {service} services. Start with 'Hi [Name],' as placeholder for contact name."
                }
        ],
        model="openai/gpt-oss-20b"        )
        text=chat.choices[0].message.content
        st.write("Email:........            \n",text)
        st.write("="*40)
    #Data store
        with open("pitch.txt","a",encoding="utf-8") as f:
          f.write(text)
          f.write("\n")
          f.write("="*40)
else:
    st.write("No matching service, Please set correct service ")