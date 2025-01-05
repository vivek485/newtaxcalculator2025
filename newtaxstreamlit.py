
from docxtpl import DocxTemplate
import pandas as pd
import numpy as np
import streamlit as st
import io

st.set_page_config(layout="wide")
st.title('ITR NEW TAX REGIME CALCULATION')



year = st.selectbox('Select Year', ['2024-25', '2025-26'])
assesment_year = st.selectbox('Select Assessment Year', ['2023-24', '2024-25', '2025-26'])
pan = st.text_input('PAN')
eid = st.text_input('Employee ID')
name = st.text_input('Name', key='name')

gross_salary = st.number_input('GROSS SALARY', value=0)
other_salary = st.number_input('OTHER SALARY', value=0)
st_deduction = st.number_input('ST DEDUCTION', value=75000)
tax_paid = st.number_input('TAX PAID', value=0)
income = gross_salary + other_salary
totalincome = income - st_deduction
data = {'year':year, 'assesment_year':assesment_year, 'pan':pan, 'eid':eid, 'name':name, 'tax_paid':tax_paid,'gross_salary':gross_salary, 'other_salary':other_salary, 'st_deduction':st_deduction, 'income':income, 'totalincome':totalincome}

df = pd.DataFrame(data,index=[0])
#st.write(df)

doc = DocxTemplate("taxnew.docx")



def calc(x):
    if x <= 300000:
        return  int(0)
def calc1(x):
    if (x > 300000) and (x < 700000):
        return 0.05 * (x - 300000)
    elif x >  700000 :
        return  0.05 * 400000
def calc2(x):
    if (x > 700000) and (x < 900000):
        return 0.1 * (x - 700000)
    elif x >  900000 :
        return  0.1 * 200000
    else:
        return int(0)
def calc3(x):
    if (x > 900000) and (x < 1200000):
        return  0.15 * (x - 900000)
    elif x > 1200000 :
        return 0.15 * 300000
    else:
        return int(0)

def calc4(x):
    if (x > 1200000) and (x < 1500000):
        return  0.2 * (x - 1200000)
    elif x > 1500000 :
        return 0.2 * 300000
    else:
        return int(0)

# def calc5(x):
#     if (x > 1500000) and (x < 1500000):
#         return  0.25 * (x - 1250000)
#     elif x > 1500000 :
#         return 0.25 * 1250000
#     else:
#         return int(0)
def calc6(x):
    if (x > 1500000) :
        return  0.3 * (x - 1500000)
    else:
        return int(0)







getdata = st.button('getdata')
if getdata:
    df['upto30l']= round((df.totalincome.apply(calc)).astype(float))
    df['upto60l'] = round((df.totalincome.apply(calc1)).astype(float))
    df['upto90l'] = round((df.totalincome.apply(calc2)).astype(float))

    df['upto12l']= round((df.totalincome.apply(calc3)).astype(float))
    df['upto15l'] = round((df.totalincome.apply(calc4)).astype(float))

    #df['upto150l'] = (df.totalincome.apply(calc5)).astype(float)
    df['greater150l'] = round((df.totalincome.apply(calc6)).astype(float))






        
    df['tot_itr'] =  round(df.upto60l + df.upto90l +df.upto12l + df.upto15l + df.greater150l)

    df['educess']= round(0.04 * df['tot_itr'])
    df['total_tax']= df['educess'] + df['tot_itr']
    df['payable_tax'] = round(df['total_tax'] - df['tax_paid'])
    df['refundable_tax'] = np.where((df.payable_tax < 0),abs(df.payable_tax),0)
    df = df.fillna(0)

    #df = pd.DataFrame({'name': name, 'gross_salary': [gross_salary], 'other_salary': [other_salary], 'st_deduction': [st_deduction], 'income': [income], 'totalincome': [totalincome], 'upto30l': [upto30l], 'upto60l': [upto60l], 'upto90l': [upto90l], 'upto12l': [upto12l], 'upto15l': [upto15l], 'greater150l': [greater150l], 'tot_itr': [tot_itr], 'educess': [educess], 'total_tax': [total_tax], 'payable_tax': [payable_tax], 'refundable_tax': [refundable_tax]})
    transposed_df = df.transpose()
    st.write(transposed_df)
    dt = df.to_dict(orient='records')
    doc.render(dt[0])
    doc_download = doc

    bio = io.BytesIO()
    doc_download.save(bio)
    if doc_download:
        st.download_button(
            label="Click here to download",
            data=bio.getvalue(),
            file_name=(f"{name}_new_itrform.docx"),
            mime="docx"
        )
        #doc.save(f"{name}_new_itrform.docx")






