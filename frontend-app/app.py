import streamlit as st
import requests
import os
import json
import pandas as pd
import base64
from datetime import datetime


api_server = 'http://192.168.0.59:8080'


# API calls
def put_customer(id,customer):
    r = requests.put(f'{api_server}/customer/{id}',
                        headers={'content-type': 'application/json'},
                        data=json.dumps(customer))
    if r.status_code == 204:
        return True
    else:
        st.write(r.status_code)
        st.write(r.json)
        return None


def delete_customer(id):
    r = requests.delete(f'{api_server}/customer/{id}')
    if r.status_code == 204:
        return True
    else:
        return False


def post_customer(customer):
    r = requests.post(f'{api_server}/customer/',
                        headers={'content-type': 'application/json'},
                        data=json.dumps(customer))
    if r.status_code == 201:
        return int(r.headers.get('Location').replace(f'{api_server}/customer/','').replace('/',''))
    elif r.status_code == 500:
        st.write('CPF already exists on the database')
        return None
    else:
        st.write(r.status_code)
        st.write(r.json)
        return None


def get_customer_by_id(id):
    r = requests.get(f'{api_server}/customer/{id}')
    if r.status_code == 200:
        return r.json()
    else:
        return {}

        
def get_customer_by_cpf(cpf):
    r = requests.get(f'{api_server}/customer/',
                    params={'cpf': cpf})
    if r.status_code == 200:
        return r.json()
    else:
        return {}


def get_customer_by_name(name):
    r = requests.get(f'{api_server}/customer/name',
                    params={'nome': name})
    if r.status_code == 200:
        return r.json()
    else:
        return {}


def get_all_customers():
    r = requests.get(f'{api_server}/customer')
    if r.status_code == 200:
        return r.json()
    else:
        return {}


#Frontend methods
def session_break(times):
    for i in range(times):
        st.write('')


def block_break():
    st.markdown('---')


def title(text,size,align,color):
    st.markdown(f'<h1 style="font-weight:bolder;font-size:{size}px;color:{color};text-align:{align};">{text}</h1>',unsafe_allow_html=True)


def text(text,size,align,color):
    st.markdown(f'<h1 style="font-size:{size}px;color:{color};text-align:{align};">{text}</h1>',unsafe_allow_html=True)


def text_sidebar(text,size,align,color):
    st.sidebar.markdown(f'<h1 style="font-size:{size}px;color:{color};text-align:{align};">{text}</h1>',unsafe_allow_html=True)


def header(text):
    st.markdown(f"<p style='color:white;'>{text}</p>",unsafe_allow_html=True)


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}" target="_blank">
            <img src="data:image/{img_format};base64,{bin_str}" />
        </a>'''
    return html_code


# App Configs and Layout
st.set_page_config(
    page_title="Customers App",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown(""" <style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)
padding = 4
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: 0rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: 2rem;
    }} </style> """, unsafe_allow_html=True)


# Main Page

title('Customers App',60,'center','gray')

img_col1, img_col2, img_col3 = st.beta_columns((1.7,2,1.7))

with img_col2:
    st.image('frontend-app/imgs/customers.png',use_column_width=True)

session_break(1)
block_break()
title('Management',30,'center','gray')
session_break(1)

func_col1, func_col2 = st.beta_columns((1,1))
with func_col1:
    with st.beta_expander('Find a customer'):
        search_by = st.selectbox('Search by ID, CPF or Name',options=('ID','CPF','Name'))
        search_value = st.text_input('Fill the value searched')

        session_break(1)
        find_buttom = st.button('Find')
        if find_buttom:
            if search_by == 'ID':
                try:
                    search_value = int(search_value)
                except:
                    st.write('The ID must be an integer value')
                else:
                    customer = get_customer_by_id(search_value)
                    if customer == {}:
                        st.write('ID not found')
                    else:
                        st.json(customer)
            elif search_by == 'CPF':
                customer = get_customer_by_cpf(search_value)
                if customer == {}:
                    st.write('CPF not found')
                else:
                    st.json(customer)
            else:
                customer = get_customer_by_name(search_value)
                if customer == []:
                    st.write('Name not found')
                else:
                    st.json(customer)
            

with func_col2:
    with st.beta_expander('Create a customer'):
        st.write('Enter the customer\'s data')
        create_form = st.form('new-customer-form')
        customer_name = create_form.text_input('Name')
        customer_cpf = create_form.text_input('CPF')
        customer_address = create_form.text_input('Address')
        customer_birth_date = create_form.date_input('Birth Date')
        customer_age = create_form.text_input('Age')
        customer_email = create_form.text_input('e-mail')
        customer_phone = create_form.text_input('Phone')
        customer_consult_date = create_form.date_input('Consult Date')
        session_break(2)
        customer_submit = create_form.form_submit_button('Create Customer')

        if customer_submit:
            now = datetime.now()

            try:
                customer = {
                    'name': customer_name,
                    'age': int(customer_age),
                    'email': customer_email,
                    'address': customer_address,
                    'cpf': customer_cpf,
                    'phone': customer_phone,
                    'birthDate': customer_birth_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'createDate': now.strftime("%Y-%m-%dT%H:%M:%S"),
                    'checkDate': customer_consult_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'updateDate': now.strftime("%Y-%m-%dT%H:%M:%S")
                }
            except:
                customer = {}
            else:
                customer_id = post_customer(customer)
                if customer_id != None:
                    st.write(f'New customer created!')
                    st.write(f'ID: {customer_id}')

func_col3, func_col4 = st.beta_columns((1,1))
with func_col3:
    with st.beta_expander('Update a customer'):
        search_for_update_value = st.text_input('Fill the ID of the customer')

        find_update_buttom = st.button('Find by ID')
        try:
            search_for_update_value = int(search_for_update_value)
        except:
            st.write('The ID must be an integer value')
        else:
            customer = get_customer_by_id(search_for_update_value)
            if customer == {}:
                st.write('ID not found')

            update_form = st.form('update-customer-form')
            update_customer_name = update_form.text_input('Name',customer['name'])
            update_customer_cpf = update_form.text_input('CPF',customer['cpf'])
            update_customer_address = update_form.text_input('Address',customer['address'])
            update_customer_birth_date = update_form.date_input('Birth Date',datetime.strptime(customer['birthDate'][0:19],'%Y-%m-%dT%H:%M:%S'))
            update_customer_age = update_form.text_input('Age',customer['age'])
            update_customer_email = update_form.text_input('e-mail',customer['email'])
            update_customer_phone = update_form.text_input('Phone',customer['phone'])
            update_customer_consult_date = update_form.date_input('Consult Date',datetime.strptime(customer['checkDate'][0:19],'%Y-%m-%dT%H:%M:%S'))
            session_break(2)
            customer_update_submit = update_form.form_submit_button('Update Customer')

            if customer_update_submit:
                now = datetime.now()

                try:
                    customer = {
                        'id': int(search_for_update_value),
                        'name': update_customer_name,
                        'age': int(update_customer_age),
                        'email': update_customer_email,
                        'address': update_customer_address,
                        'cpf': update_customer_cpf,
                        'phone': update_customer_phone,
                        'birthDate': update_customer_birth_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        'checkDate': update_customer_consult_date.strftime("%Y-%m-%dT%H:%M:%S"),
                        'updateDate': now.strftime("%Y-%m-%dT%H:%M:%S")
                    }
                    print(customer)
                except:
                    customer = {}
                else:
                    update_result = put_customer(search_for_update_value,customer)
                    if update_result != None:
                        st.write(f'Customer updated!')
with func_col4:
    with st.beta_expander('Delete a customer'):
        search_value = st.text_input('Customer\'s ID for deletion')
        customer_delete_button = st.button('Delete')
        if customer_delete_button:
            try:
                search_value = int(search_value)
            except:
                st.write('The ID must be an integer value')
            else:
                deletion_status = delete_customer(search_value)
                if deletion_status:
                    st.write('Customer deleted!')
                else:
                    st.write('ID not found')

block_break()
title('Customers Report',30,'center','gray')
session_break(1)
func_col1, func_col2 = st.beta_columns((1,4))

with func_col1:
    report_number = st.text_input('Desired number of records')
with func_col2:
    session_break(2)
    report_button = st.button('Generate Report')

if report_button:
    try:
        report_number = int(report_number)
    except:
        st.write('Invalid value. Please enter a valid integer value')
    else:
        all_customers = get_all_customers()
        df = pd.DataFrame(all_customers[0:report_number])
        st.dataframe(df)


# Navigation Panel

text_sidebar('Project Details',25,'left','gray')

project_text = '''
The frontend application sends HTTP requests to the Java API, responsible to manage the customer's table (CRUD actions) on the PostgreSQL database.
'''
st.sidebar.markdown(project_text)

st.sidebar.write('')

text_sidebar('Developer',25,'left','gray')

st.sidebar.image(image='frontend-app/imgs/rick.jpeg',use_column_width=True) 

developer_text = '''
# Richard M Souza

24 yo, graduated in system's analysis and development, experienced with games development and currently studying backend technologies.

## Social Medias
'''
st.sidebar.markdown(developer_text)
social_media_col1, social_media_col2 = st.sidebar.beta_columns((0.2,1))
with social_media_col1:
    st.markdown(get_img_with_href('frontend-app/imgs/github.png', 'https://github.com/rick667'), unsafe_allow_html=True)
with social_media_col2:
    st.markdown(get_img_with_href('frontend-app/imgs/linkedin.png', 'https://www.linkedin.com/in/richard-m-souza-83a5611b4/'), unsafe_allow_html=True)