import streamlit as st
import os
import requests
import json

st.title("Scan Receipt")

image = st.file_uploader("Upload a Receipt", type=["png", "jpg", "jpeg"])

if image is not None:
    st.image(image, caption="Uploaded Receipt", use_column_width=True)
    file_details = {"FileName":image.name,"FileType":image.type,"FileSize":image.size}

    with open(os.path.join("assets",image.name), "wb") as f:
        f.write(image.getbuffer())
        receiptOcrEndpoint = 'https://ocr.asprise.com/api/v1/receipt' # Receipt OCR API endpoint
        imageFile = "assets/{}".format(image.name) # // Modify it to use your own file
        r = requests.post(receiptOcrEndpoint, data = { \
        'client_id': 'TEST',        # Use 'TEST' for testing purpose \
        'recognizer': 'auto',       # can be 'US', 'CA', 'JP', 'SG' or 'auto' \
        'ref_no': 'ocr_python_124', # optional caller provided ref code \
        }, \
        files = {"file": open(imageFile, "rb")})
        result = (r.text)
        data = json.loads(result)
        item_list =[]
        for receipt in (data['receipts']):
            items = (receipt['items'])
            for item in items:
               item_list.append(item)


    col1,col2,col3 = st.columns(3)
    fields = ["Description", 'Amount',  "Action"]
    for item in item_list:
        col1.write(item['description'])
        col2.write(item['amount'])
        button_type = "Request" 
        button_phold = col3.empty()  # create a placeholder
        do_action = button_phold.button(button_type)
        if do_action:
            pass # do some action with a row's data
            button_phold.empty()  
        
        
