import pandas as pd
import streamlit as st
from PIL import Image
import math
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import folium_static
######################
# Page Title
st.title('Welcome to SD')
######################

# PIL.Image


#https://docs.streamlit.io/library/api-reference/media/st.image
st.image("https://static.vecteezy.com/system/resources/previews/000/619/126/original/vector-house-home-buildings-logo-icons-template.jpg", use_column_width=True)

@st.cache_data
def get_data():
    url = "https://cis102.guihang.org/data/AB_NYC_2019.csv"
    return pd.read_csv(url)
df = get_data()

st.header('AireBnB Data NYC (2019-09-12)')
st.dataframe(df.head(10))
borough = st.selectbox('Choose your place',df['neighbourhood_group'].unique())
df = df[df['neighbourhood_group']==borough]
neighbourhood = st.multiselect('Choose your neighbourhood',df['neighbourhood'].unique())
df = df[df['neighbourhood'].isin(neighbourhood)]
st.write("---")


values = st.slider("Price range", float(df.price.min()), 1000., (0., 10000.))
df = df[df['price'].between(values[0],values[1])]
st.dataframe(df)
st.write('Total {} housing rental are found in {} {} with price between {} and {}'.format(len(df),neighbourhood,borough,values[0],values[1]))

st.header("Where are the most expensive properties located?")
st.subheader("On a map")
st.markdown("The following map shows the top 1% most expensive Airbnbs priced at $800 and above.")

# Get "latitude", "longitude", "price" for top listings
#toplistings = df.query("price>=800")[["name", "latitude", "longitude", "price"]].dropna(how="any").sort_values("price", ascending=False)

#Top = df.values[0,:]
m = folium.Map(location=df[['latitude', 'longitude']].values[0], zoom_start=16)

tooltip = "Top listings"
for j in range(50): 
    #name, lat, lon, price = df.values[j,:]
    folium.Marker(
            location = df.iloc[j][['latitude','longitude']], 
            popup="Name:{} <br>Neighbourhood:{} <br>Host Name:{} <br>Room type:{}".format(df.iloc[j]['name'],df.iloc[j]['neighbourhood'],df.iloc[j]['host_name'],df.iloc[j]['room_type']), 
            tooltip="Price:{}$".format(df.iloc[j]['price'])
        ).add_to(m)


folium_static(m)


st.write("---")

st.markdown("""### Images and dropdowns

Use [st.image](https://streamlit.io/docs/api.html#streamlit.image) to show images of cats, puppies, feature importance plots, tagged video frames, and so on.

Now for a bit of fun.""")

pics = {
    "Cat": "https://cdn.pixabay.com/photo/2016/09/24/22/20/cat-1692702_960_720.jpg",
    "Puppy": "https://cdn.pixabay.com/photo/2019/03/15/19/19/puppy-4057786_960_720.jpg",
    "Sci-fi city": "https://storage.needpix.com/rsynced_images/science-fiction-2971848_1280.jpg",
    "Cheetah": "img/running-cheetah.jpeg",
    "FT-Logo": "ft-logo.png"
}
pic = st.selectbox("Picture choices", list(pics.keys()), 0)
st.image(pics[pic], use_column_width=True, caption=pics[pic])

st.write("---")

select_col = st.selectbox("Select Columns", list(df.columns), 0)
st.write(f"Your selection is {select_col}")
