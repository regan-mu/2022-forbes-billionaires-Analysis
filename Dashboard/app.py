import plotly.graph_objects as go
import plotly.express as px
from data_prep import *


# Sidebar
st.sidebar.header("Project Description".upper())
st.sidebar.write("This project seeks to analyse the 2022 billionaire list data from Forbes and"
                 " provide meaningful insights about the distribution of Billionaires and their wealth in the world.")
names = df["Name"].dropna(axis=0).values
name = st.sidebar.selectbox(label="Check your favorite Billionaire Rank (2022)", options=names)
columns = df.loc[:, ["Name", "Rank", "Networth", "Country"]]
favorite_billionaire = columns[columns["Name"] == name]
st.sidebar.subheader(f"RANK: {favorite_billionaire['Rank'].values[0]}")
st.sidebar.subheader(f"NETWORTH: {favorite_billionaire['Networth'].values[0]}")
st.sidebar.subheader(f"Country: {favorite_billionaire['Country'].values[0]}")

container = st.container()
with container:
    st.title("Forbes 2022 Billionaire List Analysis".upper())

# Row 1
tab1, tab2 = st.columns(2, gap="large")
with tab1:
    st.subheader("Sectors with the most of Billionaires")
    trace = go.Bar(
        x=top_10_categories["Industries"],
        y=top_10_categories["count"],
        marker=dict(
            color=top_10_categories["count"],
            colorscale="sunset",
        )
    )
    layout = dict(
        title=dict(
            text="Top 10 Sectors with the highest number of Billionaires",
            font=dict(color="#9C9C9C"),
            x=0.1
        ),
        xaxis=dict(
            color="#9C9C9C",
            title="Industry",
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            color="#9C9C9C",
            title="Number of Billionaires"
        ),
        margin=dict(l=50, r=50, t=50, b=50, pad=15),
        paper_bgcolor="#F5F5F5",
        plot_bgcolor="#F5F5F5",
        width=800,
        height=400
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width="200px")
    st.write("Finance and Investments Sector had the highest number of Billionaires.")

with tab2:
    st.subheader("Sectors with most Female Billionaires")
    trace = go.Bar(
        x=category_female["Industries"],
        y=category_female["count"],
        marker=dict(
            color=category_female["count"],
            colorscale="teal",
        )
    )
    layout = dict(
        title=dict(
            text="Distribution of Female Billionaires by Sector",
            font=dict(color="#9C9C9C"),
            x=0.1
        ),
        xaxis=dict(
            color="#9C9C9C",
            title="Sector",
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            color="#9C9C9C",
            title="Number of Female Billionaires"
        ),
        margin=dict(l=50, r=50, t=50, b=50, pad=15),
        paper_bgcolor="#F5F5F5",
        plot_bgcolor="#F5F5F5",
        width=800,
        height=400
    )

    fig = go.Figure(data=[trace], layout=layout)
    st.plotly_chart(fig, theme="streamlit", use_container_width=True, width="200px")
    st.write("The Manufacturing sector had the most Female Billionaires in 2022")

# Row 2
tab3, tab4 = st.columns(2, gap="large")
with tab3:
    st.subheader("Distribution of Billionaires by Country")
    country = go.Pie(
        labels=countries_agg["Country"],
        values=countries_agg["Number of Billionaires"],
        marker=dict(colors=["#007F8E", "#FF834C", "#458F54", "#E6AD20", "#6514FF"]),
        hole=0.5,
        direction="clockwise",
        rotation=0
    )
    layout = dict(
        title=dict(
            text="Top countries by number of billionaires".title(),
            font=dict(color="#9C9C9C")
        ),
        paper_bgcolor="#F5F5F5",
        plot_bgcolor="#F5F5F5",
        width=800,
        height=400
    )

    fig = go.Figure(data=[country], layout=layout)
    st.plotly_chart(fig,  theme=None, use_container_width=True, width="200px")
    st.write("Four countries, USA, CHINA, GERMANY and INDIA had more than 50% of Billionaires in Forbes")


with tab4:
    st.subheader("Comparing Male and Female Billionaires")
    gender = go.Pie(
        labels=by_gender["Gender"],
        values=by_gender["count"],
        marker=dict(colors=["#E05F19", "#007F8E"]),
        hole=0.5
    )
    layout = dict(
        title=dict(
            text="Male vs Female Billionaires",
            font=dict(color="#9C9C9C")
        ),
        paper_bgcolor="#F5F5F5",
        plot_bgcolor="#F5F5F5",
        width=800,
        height=400
    )

    fig = go.Figure(data=[gender], layout=layout)
    st.plotly_chart(fig, theme=None, use_container_width=True, width="200px")
    st.write("There were significantly more MALE billionaires than Female Billionaires")

# Row 4
container2 = st.container()
with container2:
    st.subheader("Map Distribution of Billionaires in the World")
    fig = px.choropleth(
        combined,
        locations='Country',
        locationmode="country names",
        color='Number of Billionaires',
        hover_name='Country',
        projection='natural earth1',
        hover_data=["Number of Billionaires", "Female Billionaires"],
        color_continuous_scale="viridis",
        title='Distribution of Billionaires by Country',
    )
    fig.update_layout(
        title=dict(
            font=dict(color="#9C9C9C"),
            x=0.33
        ),
        paper_bgcolor="#F5F5F5",
        geo_bgcolor="#F5F5F5",
        margin=dict(l=100, r=100),
        width=1120,
        height=400
    )
    st.plotly_chart(fig)

st.subheader("Conclusion")
st.write("In conclusion, this EDA project on the World's Richest People 2022 as listed by Forbes provides "
         "an insightful analysis of the current state of wealth distribution in the world. "
         "We have seen the countries with the highest number of billionaires, the economic sectors they come from. "
         "We've also seen the Female representation in the Billionaires club is low."
         "Overall, the EDA project on the World's Richest People 2022 as listed by Forbes offers valuable insights "
         "into the state of global wealth among the top 1%."
         )
