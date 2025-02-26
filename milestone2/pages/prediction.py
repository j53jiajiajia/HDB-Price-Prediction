import datetime

import pandas as pd
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt

from prediction.model import predict_resale, predict_rental, ResaleModelCaller, RentalModelCaller, load_prediction_model

RESALE_START_YEAR = 1990
RESALE_FLAT_TYPES = ['1-ROOM', '2-ROOM', '3-ROOM', '4-ROOM', '5-ROOM', 'EXECUTIVE', 'MULTI-GENERATION']
RESALE_STOREY_RANGES = ['1 TO 5', '6 TO 10', '11 TO 15', '16 TO 20', '21 TO 25', '26 TO 30', '31 TO 51']
RESALE_FLAT_MODELS = ['Model A', 'Improved', 'New Generation', 'Simplified', 'Premium Apartment', 'Standard',
                      'Apartment', 'Maisonette', 'Model A2', 'DBSS', 'Model A-Maisonette', 'Adjoined flat', 'Terrace',
                      'Multi Generation', 'Type S1', 'Type S2', 'Improved-Maisonette', '2-room',
                      'Premium Apartment Loft', 'Premium Maisonette', '3Gen']

RENTAL_START_YEAR = 2021
RENTAL_FLAT_TYPES = ['1-ROOM', '2-ROOM', '3-ROOM', '4-ROOM', '5-ROOM', 'EXECUTIVE']


def load_past_data(label, town, street_name, block, flat_type):
    if label == 'Resale':
        df = pd.read_csv('data/resale_dataset_cached.csv')
    else:
        df = pd.read_csv('data/rental_dataset_cached.csv')
    df = df[(df['town'] == town) & (df['street_name'] == street_name) & (df['block'] == block) & (
            df['flat_type'] == flat_type)]

    if label == 'Resale':
        df["datetime"] = df["year"].astype(str) + "-" + df["month_category"].astype(str)
    else:
        df["datetime"] = (df["month_inc"].astype(int) - 1).apply(
            lambda x: datetime.datetime(RENTAL_START_YEAR + x // 12, x % 12 + 1, 1))
    df["datetime"] = pd.to_datetime(df["datetime"])
    return df.groupby("datetime").agg({"price": "mean"}).reset_index().copy()


def ask_for_user_input(label):
    dt = datetime.datetime.now()
    if label == 'Resale':
        town = st.text_input('Town', value='JURONG WEST')
        street_name = st.text_input('Street Name', value='BOON LAY PL')
        block = st.text_input('Block', value='211')
    else:
        town = st.text_input('Town', value='QUEENSTOWN')
        street_name = st.text_input('Street Name', value='HOLLAND AVE')
        block = st.text_input('Block', value='8')

    if label == 'Resale':
        input_data = {'year': [], 'month_category': [], 'flat_type': [], 'storey_range': [], 'flat_model': [],
                      'town': [], 'street_name': [], 'block': [], }
        flat_type = st.select_slider('Flat Type', RESALE_FLAT_TYPES, value='3-ROOM')
        storey_range = st.select_slider('Storey Range', RESALE_STOREY_RANGES, value='16 TO 20')
        flat_model = st.selectbox('Flat Model', RESALE_FLAT_MODELS)
        for month in range(6):
            target_year = (dt + datetime.timedelta(days=30 * month)).year
            target_month = (dt + datetime.timedelta(days=30 * month)).month
            input_data['year'].append(str(target_year))
            input_data['month_category'].append(str(target_month))
            input_data['flat_type'].append(flat_type)
            input_data['storey_range'].append(storey_range)
            input_data['flat_model'].append(flat_model)
            input_data['town'].append(town)
            input_data['street_name'].append(street_name)
            input_data['block'].append(block)
    else:
        input_data = {'month_inc': [], 'month_category': [], 'flat_type': [], 'town': [], 'street_name': [],
                      'block': [], }
        flat_type = st.select_slider('Flat Type', RENTAL_FLAT_TYPES, value='3-ROOM')
        for month in range(6):
            target = dt + datetime.timedelta(days=30 * month)
            month_inc = (target.year - RENTAL_START_YEAR) * 12 + target.month
            input_data['month_inc'].append(str(month_inc))
            input_data['month_category'].append(str(target.month))
            input_data['flat_type'].append(flat_type)
            input_data['town'].append(town)
            input_data['street_name'].append(street_name)
            input_data['block'].append(block)
    prediction_input = pd.DataFrame(input_data)
    return prediction_input, town, street_name, block, flat_type


def price_prediction(label):
    if label == 'Resale':
        st.header("Prediction - Resale Price (Per Sqm)")
    else:
        st.header("Prediction - Monthly Rental Price")
    prediction_input, town, street_name, block, flat_type = ask_for_user_input(label)
    if st.button('Predict'):
        # Load the past data
        past_df: pd.DataFrame = load_past_data(label, town, street_name, block, flat_type)
        past_df["type"] = "historical price"

        # Next 6 months
        months = [(datetime.datetime.now() + datetime.timedelta(days=30 * i)).strftime('%b %Y') for i in range(6)]

        # Regression
        if label == 'Resale':
            pred, cls_pred_proba, cls_edge = predict_resale(prediction_input)
        else:
            pred, cls_pred_proba, cls_edge = predict_rental(prediction_input)

        # Append the prediction to the past data
        rows = []
        for i in range(6):
            now = datetime.datetime.now()
            dt = datetime.datetime(now.year, (datetime.datetime.now() + datetime.timedelta(days=30 * i)).month, 1)
            rows.append((dt, pred[i][0], "predicted price"))
        prediction_df = pd.DataFrame(rows, columns=['datetime', 'price', 'type'])
        df = pd.concat([past_df, prediction_df])

        # Plot the past and prediction data
        ax = sns.lineplot(data=df, x='datetime', y='price', hue='type')
        ax.set_title(f'Trends in Prices for `{street_name}_{block}_{flat_type}`')
        ax.set_ylabel('Price')
        ax.set_xlabel('Date')
        ax.tick_params(axis='x', rotation=45)
        st.pyplot(ax.get_figure())

        # Plot the probability
        cls_edge = cls_edge[0].tolist()
        bins = [f"({int(cls_edge[i])}, {int(cls_edge[i + 1])}]" for i in range(len(cls_edge) - 1)]
        palette_color = sns.color_palette('bright')
        fig, axs = plt.subplots(3, 2, figsize=(14, 21))
        for idx, prob in enumerate(cls_pred_proba):
            ax = axs[idx // 2][idx % 2]
            ax.pie(prob, labels=bins, colors=palette_color, autopct='%.1f%%')
            ax.set_title(f'Price Probability of {months[idx]}')
        st.pyplot(fig)


_, _ = ResaleModelCaller(), RentalModelCaller()
load_prediction_model()

session_state = st.session_state
with st.sidebar:
    # pick dataset
    st.markdown("## Choose the Dataset as followed:")
    cols = st.columns(3)
    with cols[0]:
        if st.button('Resale'):
            session_state['resale_clicked'] = True
            session_state['rental_clicked'] = False
            session_state['label'] = 'Resale'
    with cols[1]:
        if st.button('Rental', key='rental'):
            session_state['resale_clicked'] = False
            session_state['rental_clicked'] = True
            session_state['label'] = 'Rental'
    if session_state['resale_clicked']:
        st.markdown('<style>.stButton>button {background-color: gray; color: block}</style>', unsafe_allow_html=True)

    if session_state['rental_clicked']:
        st.markdown('<style>.stButton>button {background-color: gray; color: black}</style>', unsafe_allow_html=True)
    # tabs
    st.markdown("## Tabs")
    st.page_link("main.py", label="Statistics", icon="📊")
    st.page_link("pages/prediction.py", label="Prediction", icon="📈")
price_prediction(session_state['label'])
