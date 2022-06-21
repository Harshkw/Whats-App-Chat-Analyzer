import streamlit as st
import preprocessor    #we created this file
import helper          #we created this file
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whats App Analyzer")
file_upload = st.sidebar.file_uploader("Choose a File")

if file_upload is not None:
    byte_data_set = file_upload.getvalue()
    data = byte_data_set.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.title("Statistics")

    #fetch unique users
    user_list = list(df["users"].unique())
    user_list.remove("Group_Notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt:", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages,words,num_media, num_links = helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words Used")
            st.title(words)   

        with col3:
            st.header("Number of Media Files")
            st.title(num_media)      

        with col4:
            st.header("Number of Links Shared")
            st.title(num_links)

        #timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_chat(selected_user,df)
        fig4,ax4 = plt.subplots()
        ax4.plot(timeline["time"], timeline["message"], color = "green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig4)

        #Finding the most active user group level
        if selected_user == "Overall":
            st.title("Most Active Members")
            top5, new_df_per_messages = helper.most_active_user(df)

            col1,col2 = st.columns(2)  
            fig, ax = plt.subplots()

            with col1:
                plt.bar(top5.index,top5.values, color = "red")
                plt.xticks(rotation = "vertical")
                plt.ylabel("Number of Messages")
                plt.xlabel("Users")
                plt.style.use("ggplot")
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df_per_messages) 

        #activity map
        st.title("Activity Map")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Busy Day")
            busy_day = helper.active_day(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values,color ="purple")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)

        with col2:
            st.header("Month Busy")
            busy_month = helper.active_month(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color ="orange")
            plt.xticks(rotation = "vertical")
            st.pyplot(fig)
        
        #HeatMap
        st.title("Hourly Map")
        pivot = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(pivot)
        plt.xlabel("Time Interval")
        plt.ylabel("Day")
        st.pyplot(fig)

        #WordCloud
        st.title("Word Cloud")
        wc_df = helper.create_wordcloud(selected_user,df)  
        fig1, ax1 = plt.subplots()
        ax1.imshow(wc_df)
        st.pyplot(fig1)

        #Top Words
        top_words_df = helper.top_words(selected_user,df)
        st.title("Most Frequent Words")
 
        fig2,ax2 = plt.subplots()
        ax2.barh(top_words_df[0],top_words_df[1])
        plt.xticks(rotation = "vertical")
        st.pyplot(fig2)

        #Emojis
        num_emojis1 = helper.num_emojis(selected_user,df)
        st.title("Emoji Analysis")

        fig3,ax3 = plt.subplots()
        ax3.bar(num_emojis1[0],num_emojis1[1])
        st.pyplot(fig3)
