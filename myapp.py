import pandas as pd
import streamlit as st
import plotly.express as px 


st.set_page_config(
    page_title='Analytics Portal',
    page_icon='analysis.png'
    
)
st.header(':rainbow[Rohit]')
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':gray[Explore data with ease]',divider='rainbow')


file=st.file_uploader('Drop csv or excel file' , type =['csv','xlsx'] )

if(file!=None):
    if(file.name.endswith('csv')):
        data=pd.read_csv(file)
    else:
        data=pd.read_excel(file)
    
    st.dataframe(data)
    st.info('File Uploaded Successfully',icon="🚨")
        
    st.subheader(':rainbow[Basic Summary of dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4=st.tabs(['Summary','Top And Bottom Row','Data Types','Columns'])
    
    with tab1:
        st.write(f'There are {data.shape[0]} rows and {data.shape[1]} columns in the dataset')
        st.subheader(':gray[Statistical Summary Of Data]')
        st.dataframe(data.describe())
        
    with tab2:
        st.subheader(':gray[Top Rows]')
        toprows=st.slider('Number of rows you want',1,data.shape[0],key='toprows')
        st.dataframe(data.head(toprows))
        
        st.subheader(':gray[Bottom Rows]')
        bottomrows=st.slider('Number of rows you want',1,data.shape[0],key='bottomrow')
        st.dataframe(data.tail(bottomrows))
        
    
    with tab3:
        st.subheader(':gray[Data Types of data]')
        st.dataframe(data.dtypes)
        
    with tab4:
        st.subheader('Column Names in Dataset')
        st.dataframe(list(data.columns))
        
    st.subheader(':rainbow[Column Values to count]',divider='rainbow')
    with st.expander('Value Count'):
        col1,col2=st.columns(2)
        with col1:
            column = st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows= st.number_input('Top rows',min_value=1,step=1)
        
        count =st.button('Count')
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)    
            st.subheader('Visualization',divider='gray')
            fig=px.bar(data_frame=result,x=column , y='count',text='count')
            st.plotly_chart(fig)
            
            fig=px.line(data_frame=result,x=column , y='count',text='count')
            st.plotly_chart(fig)
            
            fig=px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)
            
    
    st.subheader(':rainbow[Groupby : Simply your data Analysis]',divider='rainbow')
    
    with st.expander('Group By your column'):
        col1,col2,col3=st.columns(3)
        
        with col1:
            groupby_cols=st.multiselect('Choose your column to groupby',options=list(data.columns))
        with col2:
            operation_col=st.selectbox(' Choose Column for operation',options=list(data.columns))
        with col3:
            operation = st.selectbox('Choose operation',options=['sum','max','min','mean','meadian'])
            
            
        if(groupby_cols):
            result1 = data.groupby(groupby_cols).agg(
                newcol = (operation_col,operation)
            ).reset_index()
            st.dataframe(result1)
            
            st.subheader(':gray[Data Visualization]', divider='gray')
            graphs = st.selectbox('Choose your graphs', options=['line', 'bar', 'scatter', 'pie', 'sunburst'])
            if graphs == 'line':
                x_axis = st.selectbox('Choose X axis', options=list(result1.columns))
                y_axis = st.selectbox('Choose Y axis', options=list(result1.columns))
                color = st.selectbox('Color Information', options=[None] + list(result1.columns))
                fig = px.line(data_frame=result1, x=x_axis, y=y_axis, color=color, markers='o')
                st.plotly_chart(fig)
            elif graphs == 'bar':
               x_axis = st.selectbox('Choose X axis', options=list(result1.columns))
               y_axis = st.selectbox('Choose Y axis', options=list(result1.columns))
               color = st.selectbox('Color Information', options=[None] + list(result1.columns))
               facet_col = st.selectbox('Column Information', options=[None] + list(result1.columns))
               fig = px.bar(data_frame=result1, x=x_axis, y=y_axis, color=color, facet_col=facet_col, barmode='group')
               st.plotly_chart(fig)
            elif graphs == 'scatter':
               x_axis = st.selectbox('Choose X axis', options=list(result1.columns))
               y_axis = st.selectbox('Choose Y axis', options=list(result1.columns))
               color = st.selectbox('Color Information', options=[None] + list(result1.columns))
               size = st.selectbox('Size Column', options=[None] + list(result1.columns))
               fig = px.scatter(data_frame=result1, x=x_axis, y=y_axis, color=color, size=size)
               st.plotly_chart(fig)
            elif graphs == 'pie':
               values = st.selectbox('Choose Numerical Values', options=list(result1.columns))
               names = st.selectbox('Choose labels', options=list(result1.columns))
               fig = px.pie(data_frame=result1, values=values, names=names)
               st.plotly_chart(fig)
            elif graphs == 'sunburst':
                path = st.multiselect('Choose your Path', options=list(result1.columns))
                fig = px.sunburst(data_frame=result1, path=path, values='newcol')
                st.plotly_chart(fig)
          
           
        
        
