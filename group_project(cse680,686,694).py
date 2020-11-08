# -*- coding: utf-8 -*-
"""Group Project(cse680,686,694).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-6Lq7ZuVLyLoD5O1yG12d47BpQ4fDqkU

<p align="center">
  <img src="https://entrackr.com/wp-content/uploads/2017/08/zomato-image.jpg"/>
</p>

**Zomato** is a restaurant search and discovery service founded in 2008 by Indian entrepreneurs Deepinder Goyal and Pankaj Chaddah. It currently operates in 23 countries. They've recently released this directory of all restaurants & eateries currently under its purview.
"""

import numpy as np
import pandas as pd
import plotly.express as px
px.set_mapbox_access_token("sk.eyJ1Ijoic3JpbmFnIiwiYSI6ImNrZ3JlMXU5MTA4NnAycHBsdGo4OHhoeHMifQ.3ccoE0mE6gXtIuBCCwsZjw")
import plotly.graph_objs as go 
from plotly.subplots import make_subplots

#our data dosnt have country names(for labels, visual understanding) so using country code to map name 
countryCode_toName = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zealand",
    162: "Phillipines",
    166: "Qatar",
    184: "Singapore",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "UAE",
    215: "United Kingdom",
    216: "United States",
}

"""<a id="section1"></a>
    
# Sneak Peak into the Dataset
"""

data = pd.read_csv("https://raw.githubusercontent.com/20171CSE0680/dv/main/zomato.csv", encoding = "latin-1")#zomato data from personal github rep
data['Country'] = data['Country Code'].apply(lambda x: countryCode_toName[x])#mapping country code to name
data.sample(5)

data.describe()

data.info()

data.shape

data.isnull().sum()

"""**Data is alredy clean**

<a id="section2"></a>

# Zomato's Presence across the Globe
"""

labels = list(data.Country.value_counts().index) #unique country
values = list(data.Country.value_counts().values)#each country count of resturents
fig = go.Figure(data=[
        {
            "labels" : labels,
            "values" : values,
            "hoverinfo" : 'label+percent',
            "domain": {"x": [0, .9]},
            "hole" : 0.6,
            "type" : "pie",
            "rotation":120,
        },
    ],layout={
        "title" : "Zomato's Presence around the World",
        "annotations": [
            {
                "font": {"size":20},
                "showarrow": True,
                "text": "Countries",
                "x":0.2,
                "y":0.9,
            },
        ]
    }) 
fig.show()
fig.write_html('countrypie.html')
# or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ...

st=['open-street-map', 'carto-positron', 'carto-darkmatter', 'stamen-terrain', 'stamen-toner', 'stamen-watercolor']
n=np.random.randint(0,7)
fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude", hover_name="Restaurant Name",
                        hover_data=["Cuisines"	,"Average Cost for two"], color="Rating text",zoom=3, height=700,)
fig.update_layout(mapbox_style='carto-darkmatter')#random style
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
fig.write_html('countryscat.html')

fig = px.density_mapbox(data, lat='Latitude', lon='Longitude', z='Aggregate rating', radius=10,
                        center=dict(lat=0, lon=180), zoom=0,
                        mapbox_style="carto-darkmatter")
fig.show()
fig.write_html('countryheat.html')

"""### Quick Inferences - 

1. Zomato's largest market is in India itself, no other country even comes close. 
2. Analysing data from India should give us a pretty accurate representation of the entire data.
3. One important thing that might vary across different regions is the **types of Cusinies**. So it should be interesting to see how many cusinies are served throughout the world.

<a id="section3"></a>

# Number of Cusinies Served in Zomato's Target Markets
(** Considering countries only where 50 or more Restaurants are registered with Zomato**)
"""

def number_of_cusines(temp):
    #print (temp)
    return len(temp.split())
data.Cuisines.fillna("zero", inplace=True)
data['Number of Cuisines Offered'] = data.Cuisines.apply(number_of_cusines)

trace = [
    go.Histogram(x=data.loc[data.Country.isin(['India'])]['Number of Cuisines Offered'],
                 visible=True,
                opacity = 0.7,
                 name="India",
                histnorm="percent",
                 hoverinfo="y",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(175, 200, 196)')
                ),
    go.Histogram(x=data.loc[data.Country.isin(['United States'])]['Number of Cuisines Offered'],
                 visible=False,
                opacity = 0.7,
                 name = "United States",
                 hoverinfo="y",
                histnorm="percent",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(155, 200, 196)')
                ),
    go.Histogram(x=data.loc[data.Country.isin(['United Kingdom'])]['Number of Cuisines Offered'],
                 visible=False,
                opacity = 0.7,
                 name = "United Kingdom",
                 hoverinfo="y",
                histnorm="percent",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(155, 220, 196)')
                ),
    go.Histogram(x=data.loc[data.Country.isin(['UAE'])]['Number of Cuisines Offered'],
                 visible=False,
                opacity = 0.7,
                 name = "United Arab Emirates",
                 hoverinfo="y",
                histnorm="percent",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(155, 200, 216)')
                ),
    go.Histogram(x=data.loc[data.Country.isin(['South Africa'])]['Number of Cuisines Offered'],
                 visible=False,
                opacity = 0.7,
                 name = "South Africa",
                 hoverinfo="y",
                histnorm="percent",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(195, 200, 196)')
                ),
    go.Histogram(x=data.loc[data.Country.isin(['Brazil'])]['Number of Cuisines Offered'],
                 visible=False,
                opacity = 0.7,
                 name = "Brazil",
                 hoverinfo="y",
                histnorm="percent",
                #nbinsx=10,
                 marker=dict(line=dict(width=1.6,
                                      color='rgb(75, 75, 75)',),
                            color='rgb(195, 250, 196)')
                ),
]

layout = go.Layout(autosize=True,
                   xaxis=dict(title="Number of Cuisines Offered",
                             titlefont=dict(size=20,),
                             tickmode="linear",),
                   yaxis=dict(title="Percentage of Restaurants <br> (Associated with Zomato)",
                             titlefont=dict(size=17,),),
                  )

updatemenus = list([
    dict(
    buttons=list([
        dict(
            args = [{'visible': [True, False, False, False, False, False]}],
            label="India",
            method='update',
        ),
        dict(
            args = [{'visible': [False, True, False, False, False, False]}],
            label="United States",
            method='update',
        ),
        dict(
            args = [{'visible': [False, False, True, False, False, False]}],
            label="United Kingdom",
            method='update',
        ),
        dict(
            args = [{'visible': [False, False, False, True, False, False]}],
            label="United Arab Emirates",
            method='update',
        ),
        dict(
            args = [{'visible': [False, False, False, False, True, False]}],
            label="South Africa",
            method='update',
        ),
        dict(
            args = [{'visible': [False, False, False, False, False, True]}],
            label="Brazil",
            method='update',
        ),
    ]),
        direction="down",
        pad = {'r':10, "t":10},
        showactive=True,
        x=0.29,
        y=1.15,
        yanchor='top',
    ),
])

annotations = list([
    dict(text='Country: ', x=0.0, y=1.1, yref='paper', align='left', showarrow=False,)
])

layout['updatemenus'] = updatemenus
layout['annotations'] = annotations

fig = go.Figure(data=trace, layout=layout)
fig.show()
fig.write_html('countrybar.html')

"""### Quick Inferences - 

1. Most retaurants seem to offer 1-3 types of cusinies.  
2. ### India & South Africa being the only ones to offer > 5 cuisines in a significant number of restaurants.

<a id="section4"></a>
# Are ratings affected by how cheap/expensive a restaurant is?

The following plot was created by aggrating the ratings & the **average cost of two** for eating at a particular place.
"""

import copy
data_india = copy.deepcopy(data[data.Country == "India"])

data_india['Text'] = data_india['Restaurant Name'] + "<br>" + data_india['Locality Verbose']
data_india_rest = data_india[['Restaurant Name','Aggregate rating','Average Cost for two']].groupby('Restaurant Name').mean()

data = [
    go.Scatter(x = data_india_rest['Average Cost for two'],
              y = data_india_rest['Aggregate rating'],
               text = data_india['Text'],
              mode = "markers",
               marker = dict(opacity = 0.7,
                            size = 10,
                            color = data_india_rest['Aggregate rating'], #Set color equalivant to rating
                            colorscale= 'Viridis',
                            showscale=True,
                             maxdisplayed=2500,
                            ),
                hoverinfo="text+x+y",
              )
]
layout = go.Layout(autosize=True,
                   xaxis=dict(title="Average Cost of Two (INR)",
                             #titlefont=dict(size=20,),
                             #tickmode="linear",
                             ),
                   yaxis=dict(title="Rating",
                             #titlefont=dict(size=17,),
                             ),
                  )
fig=go.Figure(dict(data=data, layout=layout))
fig.show()
fig.write_html('rating vs price.html')

"""### Quick Inference

As it seems, from a quick glance, there is **no** obseravable linear relationship. At almost every price point, there appears to be both **Good** and **Bad** restaurants.

<a id="section5"></a>

# Analysing Data from Delhi & its Neighbouring Areas

Since most of Zomato's business is concentrated in & around **New Delhi, India**, so I'll be looking for places to eat around the following areas -- 

1. New Delhi (National Capital Region, India)
2. Gurgaon
3. Noida
4. Faridabad
"""

ncr_data = data_india.loc[data_india.City.isin(['New Delhi','Gurgaon','Noida','Faridabad'])]

x_ax = ncr_data.City.value_counts().index
y_ax = ncr_data.City.value_counts().values

data = [
    go.Bar(x = x_ax,
          y = y_ax,
          text = y_ax,
          textposition='auto',
          marker = dict(color = 'rgb(80, 228, 188)',
                       line = dict(color='rgb(8, 48, 107)',
                                  width=1.5),
                       ),
          opacity=0.6,
        hoverinfo="none"
          )
]

layout = go.Layout(title = "Number of Restaurants Across Major Cities",
                   yaxis = dict(title = "Number of Restaurants/Eateries <br> (Associated with Zomato)"),
                   xaxis = dict(title="Cities",
                               titlefont=dict(size=30),),
                  )


fig = go.Figure(data=data, layout=layout)

fig.show()
fig.write_html('city_res_count.html')

"""The aforementioned **four cities** represent nearly 65% of the total data available in the dataset. Apart from the local restaurants, it'd be intersting to know where the **known-eateries** that are commonplace. The verticles across which these can be located are -

- **Breakfast**
- **American Fast Food**
- **Ice Creams, Shakes & Desserts**
"""

types = {
    "Breakfast and Coffee" : ["Cafe Coffee Day", "Starbucks", "Barista", "Costa Coffee", "Chaayos", "Dunkin' Donuts"],
    "American": ["Domino's Pizza", "McDonald's", "Burger King", "Subway", "Dunkin' Donuts", "Pizza Hut"],
    "Ice Creams and Shakes": ["Keventers", "Giani", "Giani's", "Starbucks", "Baskin Robbins", "Nirula's Ice Cream"]
}
breakfast = ncr_data.loc[ncr_data['Restaurant Name'].isin(types['Breakfast and Coffee'])]
american = ncr_data.loc[ncr_data['Restaurant Name'].isin(types['American'])]
ice_cream = ncr_data.loc[ncr_data['Restaurant Name'].isin(types['Ice Creams and Shakes'])]

print ("Breakfast: ", breakfast.shape, "\nFast Food: ", american.shape, "\nIce Cream: ", ice_cream.shape)

"""<a id="section6"></a>

# Breakfast & Coffee

Common places to have Breakfast & Coffee include **Starbucks**, **Barista** etc.

### Average Ratings of Common Coffee Shops
"""

breakfast_rating = breakfast[['Restaurant Name',
                              'Aggregate rating']].groupby('Restaurant Name').mean().reset_index().sort_values('Aggregate rating', 
                                                                                                               ascending=False)
x_ax = breakfast_rating['Restaurant Name']
y_ax = breakfast_rating['Aggregate rating'].apply(lambda x: round(x,2))

data = [
    go.Bar(x = x_ax,
          y = y_ax,
          text = y_ax,
          textposition='auto',
          marker = dict(color = 'rgb(159, 202, 220)',
                       line = dict(color='rgb(8, 48, 107)',
                                  width=1.5),
                       ),
          opacity=0.6,
        hoverinfo="none"
          )
]

layout = go.Layout(title = "Average Ratings: Breakfast & Coffee",
                  yaxis = dict(title="Average Rating",
                              titlefont=dict(size=20)),
                   xaxis = dict(title="Cafe",
                               titlefont=dict(size=20),),
                  )


fig = go.Figure(data=data, layout=layout)

fig.show()
fig.write_html('breakfast_rating.html')

"""### Where to find some good Breakfast & Coffee?

**Using the Mapbox API via PlotLy.**
"""

breakfast_locations = breakfast[['Restaurant Name','Locality Verbose','City',
                                'Longitude','Latitude','Average Cost for two','Aggregate rating',
                                'Rating text']].reset_index(drop=True)
breakfast_locations['Text'] = breakfast_locations['Restaurant Name'] + "<br>Rating: "+breakfast_locations['Rating text']+" ("+breakfast_locations['Aggregate rating'].astype(str)+")" + "<br>" + breakfast_locations['Locality Verbose']
#mapbox_access_token = #enter mapbox token here
#breakfast_locations.sample(5)

data = [
    go.Scattermapbox(lat= breakfast_locations.Latitude,
                    lon = breakfast_locations.Longitude,
                    text = breakfast_locations['Restaurant Name'],
                    opacity = 0.8,
                    marker = dict(
                                  size = 10,
                                 color="rgb(8, 48, 107)",
                                 opacity = 0.9,), 
                    hovertext = breakfast_locations['Text'], 
                    hoverlabel = dict(font = dict(size=15),),
                    mode = "markers+text",
                     
                    )
]

layout = go.Layout(autosize=True,
                   title = "Breakfast & Coffee in Delhi/Gurgaon & Neighbouring Areas<br>(Associated with Zomato)",
                   hovermode='closest',
                  mapbox = dict(
                  accesstoken = "sk.eyJ1Ijoic3JpbmFnIiwiYSI6ImNrZ3JlMXU5MTA4NnAycHBsdGo4OHhoeHMifQ.3ccoE0mE6gXtIuBCCwsZjw",
                  center = dict(lat = 28.63,
                               lon = 77.21,),
                  pitch = 0,
                zoom = 10,
                  style="open-street-map"),
    )
fig = go.Figure(data=data, layout=layout)
fig.show()
fig.write_html("map_for_breakfast&cofee.html")

"""<a id="section7"></a>

**Need more Starbucks outlets in Delhi...**

# American Fast Food

### Assessing Average Ratings of American Fast Food Chains like McDonald's, Subway etc
"""

lunch_rating = american[['Restaurant Name',
                              'Aggregate rating']].groupby('Restaurant Name').mean().reset_index().sort_values('Aggregate rating', 
                                                                                                               ascending=False)
x_ax = lunch_rating['Restaurant Name']
y_ax = lunch_rating['Aggregate rating'].apply(lambda x: round(x,2))

data = [
    go.Bar(x = x_ax,
          y = y_ax,
          text = y_ax,
          textposition='auto',
          marker = dict(color = 'red',
                       line = dict(color='rgb(8, 48, 107)',
                                  width=1.5),
                       ),
          opacity=0.6,
        hoverinfo="none",
          )
]

layout = go.Layout(title = "Average Ratings: Lunch",
                  yaxis = dict(title="Average Rating",
                              titlefont=dict(size=20)),
                   xaxis = dict(title="Restaurant",
                               titlefont=dict(size=20),),
                  )


fig = go.Figure(data=data, layout=layout)

fig.show()

"""**Quite surprising to see Burger King rated over McDonald's, or maybe it's just a personal bias!**

### Let's find some classic American Sandwiches
"""

lunch_locations = american[['Restaurant Name','Locality Verbose','City',
                                'Longitude','Latitude','Average Cost for two','Aggregate rating',
                                'Rating text']].reset_index(drop=True)
lunch_locations['Text'] = lunch_locations['Restaurant Name'] + "<br>Rating: "+lunch_locations['Rating text']+" ("+lunch_locations['Aggregate rating'].astype(str)+")" + "<br>" + lunch_locations['Locality Verbose']

data = [
    go.Scattermapbox(lat= lunch_locations.Latitude,
                    lon = lunch_locations.Longitude,
                    text = lunch_locations['Restaurant Name'],
                    opacity = 0.8,
                    marker = dict(
                                  size = 10,
                                 color="red", #does not work if the symbol isn't a circle
                                 opacity = 0.9,), 
                    hovertext = lunch_locations['Text'], 
                    hoverlabel = dict(font = dict(size=15),),
                    mode = "markers+text",
                     
                    )
]

layout = go.Layout(autosize=True,
                   title = "American Fast Food in Delhi/Gurgaon & Neighbouring Areas<br>(Associated with Zomato)",
                   hovermode='closest',
                  mapbox = dict(
                  accesstoken = "sk.eyJ1Ijoic3JpbmFnIiwiYSI6ImNrZ3JlMXU5MTA4NnAycHBsdGo4OHhoeHMifQ.3ccoE0mE6gXtIuBCCwsZjw",
                  center = dict(lat = 28.63,
                               lon = 77.21,),
                  pitch = 0,
                zoom = 10,
                 style="open-street-map" ),
    )
fig = go.Figure(data=data, layout=layout)
fig.show()
fig.write_html("map_for_American Fast Food.html")

"""<a id="section8"></a>

# Down for some Ice Creams & Shakes?

Though I'm not sure why **Giani's** is rated under 3, it clearly deserves more.
"""

des_rating = ice_cream[['Restaurant Name',
                              'Aggregate rating']].groupby('Restaurant Name').mean().reset_index().sort_values('Aggregate rating', 
                                                                                                               ascending=False)
x_ax = des_rating['Restaurant Name']
y_ax = des_rating['Aggregate rating'].apply(lambda x: round(x,2))

data = [
    go.Bar(x = x_ax,
          y = y_ax,
          text = y_ax,
          textposition='auto',
          marker = dict(color = 'pink',
                       line = dict(color='rgb(8, 48, 107)',
                                  width=1.5),
                       ),
          opacity=0.6,
        hoverinfo="none",
          )
]

layout = go.Layout(title = "Average Ratings: Ice Cream & Shakes",
                  yaxis = dict(title="Average Rating",
                              titlefont=dict(size=20)),
                   xaxis = dict(title="Parlour",
                               titlefont=dict(size=20),),
                  )


fig = go.Figure(data=data, layout=layout)
fig.show()

"""### Locations of Popular Ice Cream Parlours in & around Delhi"""

des_locations = ice_cream[['Restaurant Name','Locality Verbose','City',
                                'Longitude','Latitude','Average Cost for two','Aggregate rating',
                                'Rating text']].reset_index(drop=True)
des_locations['Text'] = des_locations['Restaurant Name'] + "<br>Rating: "+des_locations['Rating text']+" ("+des_locations['Aggregate rating'].astype(str)+")" + "<br>" + des_locations['Locality Verbose']

data = [
    go.Scattermapbox(lat= des_locations.Latitude,
                    lon = des_locations.Longitude,
                    text = des_locations['Restaurant Name'],
                    opacity = 0.8,
                    marker = dict(
                                  size = 10,
                                 color="teal", #does not work if the symbol isn't a circle
                                 opacity = 0.8,), 
                    hovertext = des_locations['Text'], 
                    hoverlabel = dict(font = dict(size=15),),
                    mode = "markers+text",
                     
                    )
]

layout = go.Layout(autosize=True,
                   title = "Ice Creams & Shakes Parlours in Delhi/Gurgaon & Neighbouring Areas<br>(Associated with Zomato)",
                   hovermode='closest',
                  mapbox = dict(
                  accesstoken ="sk.eyJ1Ijoic3JpbmFnIiwiYSI6ImNrZ3JlMXU5MTA4NnAycHBsdGo4OHhoeHMifQ.3ccoE0mE6gXtIuBCCwsZjw",
                  style="open-street-map" ,
                  center = dict(lat = 28.63,
                               lon = 77.21,),
                  pitch = 0,
                zoom = 10,
                  ),
    )
fig = go.Figure(data=data, layout=layout)
fig.show()
fig.write_html('Ice Creams & Shakes.html')

"""### Quick Inferences - 

A point of interest to see here would be that Zomato probably does NOT represent accurately the dessert scenario in the region as there are some popular kiosks operated ice cream vendors, most notably associated with **Mother Dairy Ice Creams, Kwality Walls etc** that are not represented here in the dataset.

### World pressence
"""

# frequency of Country
df = pd.read_csv("https://raw.githubusercontent.com/20171CSE0680/dv/main/zomato.csv",encoding='latin-1')
freq=df
freq = freq['Country Code'].value_counts().reset_index().rename(columns={"index": "x"})
freq['Country']=name=[countryCode_toName[x] for x in freq.x]
freq

# Initialize figure with subplots
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.6, 0.4],
    
    specs=[[{"type": "scattergeo", }, {"type": "bar"}],
           ])

# Add scattergeo globe map of volcano locations
fig.add_trace(
    go.Scattergeo(lat=df["Latitude"],
                  lon=df["Longitude"],
                  mode="markers",
                  hoverinfo="text",
                  showlegend=False,
                  marker=dict(color="crimson", size=4, opacity=0.8),),
    row=1, col=1,
)

# Add locations bar chart
fig.add_trace(
    go.Bar(x=freq["Country"][0:10],y=freq["Country Code"][0:10], marker=dict(color="crimson"), showlegend=False,),
    row=1, col=2
)



# Update geo subplot properties
fig.update_geos(
    projection_type="orthographic",
    landcolor="white",
    oceancolor="MidnightBlue",
    showocean=True,
    lakecolor="LightBlue"
)

# Rotate x-axis labels
fig.update_xaxes(tickangle=45,)

# Set theme, margin, and annotation in layout
fig.update_layout(
    template="plotly_dark",
    margin=dict(r=10, t=25, b=40, l=60),
    annotations=[
        dict(
            text="Source: NOAA",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0,
            y=0)
    ]
)

fig.show()
fig.write_html('homepage.html')

"""### That'd be all for now, We'll continue adding some more visuals as We explore this data. 
 
**Let us know what you guys think email us 201710100852@presidencyuniversity.in !**

### Project Details

**Group members:**


1.  SRINAG MANRI - 20171CSE0680
2.  SUJAYA V SHETTY - 20171CSE0686
3. SUSHMA S K - 20171CSE0694

**DataSet**:https://www.kaggle.com/shrutimehta/zomato-restaurants-data

**GitHub:**https://github.com/20171CSE0680/dv

**Check Our Website:**https://20171cse0680.github.io/dv/
"""