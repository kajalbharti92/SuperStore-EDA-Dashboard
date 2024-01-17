import streamlit as st
import plotly.express as px   # Using the plotly we can generate the chart
import pandas as pd   # using the Pandas for data handling
import os   # for navigating the files
import warnings   # to ignore the warnings if in case we get any
warnings.filterwarnings("ignore")

# Setting the configuration for the Streamlit page, including title, icon, and layout.
st.set_page_config(page_title='Superstore',page_icon=':bar_chart:',layout='wide')   

st.title(':bar_chart: Sample Superstore EDA')   # using the st.title we are providing the title for the dashboard
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)   # Here we are using the st.markdown function and inside this we are using the block of html and css for styling

fl=st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))    # using this we are trying to upload the file
if fl is not None:
    filename=fl.name
    st.write(filename)
    df=pd.read_csv(filename,encoding="ISO-8859-1")
    # Check file type and use the appropriate pd.read_ method
    if filename.endswith('.csv'):
        df = pd.read_csv(fl, encoding="ISO-8859-1")
    elif filename.endswith('.xls') or filename.endswith('.xlsx'):
        df = pd.read_excel(fl, encoding="ISO-8859-1")
    elif filename.endswith('.txt'):
        df = pd.read_csv(fl, encoding="ISO-8859-1", delimiter='\t')
    else:
        st.error("Unsupported file format. Please upload a CSV, TXT, XLS, or XLSX file.")

else:
    os.chdir(r"C:\projects\Dashboard")
    df=pd.read_csv("Sample - Superstore.csv",encoding="ISO-8859-1")

col1,col2=st.columns(2)
df['Order Date']=pd.to_datetime(df['Order Date'])

# to get the min and max date

StartDate=pd.to_datetime(df['Order Date']).min()
EndDate=pd.to_datetime(df['Order Date']).max()

with col1:
    date1=pd.to_datetime(st.date_input("Start Date",StartDate))
with col2:
    date2=pd.to_datetime(st.date_input("End Date",EndDate))

# To filter the date
    
df=df[(df["Order Date"]>=date1) & (df["Order Date"]<=date2)].copy()

# We are creating the side filter bar to filter the data based on state, region and city.

st.sidebar.header("Select your Filter:")

# Creating filters based on region:
 
region=st.sidebar.multiselect("Pick your Region",df["Region"].unique())
if not region:
    df2=df.copy()
else:
    df2=df[df["Region"].isin(region)]

# Creating Filters based on State:
    
state=st.sidebar.multiselect("Pick your State",df2["State"].unique())
if not state:
    df3=df2.copy()
else:
    df3=df2[df2["State"].isin(state)]

# Creating the filters based on City:
    
city=st.sidebar.multiselect("Pick your City",df3["City"].unique())

# Filter the data based on Region, State and City:

if not region and not state and not city:
    filtered_df=df
elif not state and not city:
    filtered_df=df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df=df[df["State"].isin(state)]
elif state and city:
    filtered_df=df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df=df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df=df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df=df3[df3["City"].isin(city)]
else:
    filtered_df=df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Creating the column chart for category and region:
    
category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()   

with col1:
    st.subheader("Category wise Sales")     # Creating the subheader.
    fig=px.bar(category_df,x="Category",y="Sales",text=['${:,.2f}'.format(x) for x in category_df["Sales"]],template="seaborn")   # We are using plotly to create the bar chart
    st.plotly_chart(fig,use_container_width=True, height=200)     # In this we are displaying the bar chart

with col2:
    st.subheader("Region wise Sales")     # Creating the subheader.
    fig=px.pie(filtered_df,values="Sales",names="Region",hole=0.5)   # We are using plotly to create the pie chart
    fig.update_traces(text=filtered_df["Region"],textposition="outside")   # We are using the update_traces method to display the region names as text labels outside the pie chart slices
    st.plotly_chart(fig,use_container_width=True)    # In this we are displaying the pie chart

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Category.csv", mime = "text/csv", help = 'Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by = "Region", as_index = False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index = False).encode('utf-8')
        st.download_button("Download Data", data = csv, file_name = "Region.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')
            
# Visualisation of data using the time series analysis based on Month year.
            
filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart=pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y: %b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="month_year",y="Sales",labels={"Sales::Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View data od Time Series"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "TimeSeries.csv", mime ='text/csv')

# Creating treemap based on region, Category and Sub-Category
        
st.subheader("Hierarchical view of Sales using Treemap")
fig3=px.treemap(filtered_df,path=["Region","Category","Sub-Category"],values="Sales",hover_data=["Sales"],
                    color="Sub-Category")
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Segment", template = "plotly_dark")
    fig.update_traces(text = filtered_df["Segment"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_df, values = "Sales", names = "Category", template = "gridon")
    fig.update_traces(text = filtered_df["Category"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"] = filtered_df["Order Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_df, values = "Sales", index = ["Sub-Category"],columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Creating the scatter plot
data1 = px.scatter(filtered_df, x = "Sales", y = "Profit", size = "Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",titlefont = dict(size=20),xaxis = dict(title="Sales",titlefont=dict(size=19)),
            yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("View Data"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# For Downloading the orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")