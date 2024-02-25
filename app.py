import streamlit as st
from twilio.rest import Client
from datetime import datetime
import processor,helper
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
# Function to send WhatsApp message



# Function for WhatsApp Message Scheduler
def whatsapp_scheduler():
    st.title("WhatsApp Message Scheduler")

    sender_number = st.text_input("Enter Receiver Number:")
    message = st.text_area("Message:")
    scheduled_date = st.date_input("Select Scheduled Date:")
    scheduled_time_input = st.time_input("Select Scheduled Time:")
    scheduled_time = datetime.combine(scheduled_date, scheduled_time_input)

    if st.button("Send"):
        if sender_number and message:
            message_sid = helper.send_whatsapp_message(sender_number, message, scheduled_time)
            st.success(f"Message scheduled Sucessfully")
        else:
            st.error("Receiver Number and Message cannot be empty.")
# Function for WhatsApp Chat Analyzer
def whatsapp_analyzer():
  st.title("whatsapp chat analyzer")

  uploaded_file=st.file_uploader("choose a file")
  if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    df=processor.process(data)
   #  st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.selectbox("show analysis with",user_list)
    

    if st.button("start analysis"):
       num_messages,num_media,links=helper.fetch_stats(selected_user,df) 
       col1, col2, col3 = st.columns(3)

       with col1:
          st.header("Total Messages")
          st.title(num_messages)
       with col2:
          st.header("Shared Media")
          st.title(num_media)
       with col3:
          st.header("Shared Link")
          st.title(links)

       st.title("Monthly timeline")
       timeline=helper.monthly_timeline(selected_user,df)
       fig,ax=plt.subplots()
       ax.plot(timeline['time'],timeline['msg'],color="purple")
       plt.xticks(rotation='vertical')
       st.pyplot(fig)


       st.title('Activity map')
       col1,col2=st.columns(2)
       with col1:
         st.header("Most busy day")
         busy_day=helper.week_activity_map(selected_user,df)
         fig,ax=plt.subplots()
         ax.bar(busy_day.index,busy_day.values,color="green")
         plt.xticks(rotation='vertical')
         st.pyplot(fig)
       with col2:
         st.header("Most busy month")
         busy_month=helper.month_activity_map(selected_user,df)
         fig,ax=plt.subplots()
         ax.bar(busy_month.index,busy_month.values,color="orange")
         plt.xticks(rotation='vertical')
         st.pyplot(fig)
 


       if selected_user=='overall':
          st.title('Most Active Users')
          x,new_df=helper.most_active_user(df)
          fig,ax=plt.subplots()
          col1,col2=st.columns(2)
          with col1:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation=90)
            st.pyplot(fig)
          with col2:
            st.dataframe(new_df)
    
       st.title("Word Cloud")
       df_wc=helper.create_cloud(selected_user,df)
       fig,ax=plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)


       emoji_df=helper.emoji_helper(selected_user,df)
       st.title("EMoji Analysis")
       col1,col2=st.columns(2)
       with col1:
          st.dataframe(emoji_df)
       with col2:
          fig,ax=plt.subplots()
          ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
          st.pyplot(fig)

       
       st.title("Weekly Activity Map")
       user_heatmap = helper.activity_heatmap(selected_user,df)
       fig,ax = plt.subplots()
       ax = sns.heatmap(user_heatmap)
       st.pyplot(fig)

# Main function
def main():
    st.sidebar.title("Chat Chrono")
    app_mode = st.sidebar.radio("",
        [ "Scheduler","Analyzer"])

    if app_mode == "Analyzer":
        whatsapp_analyzer()
    elif app_mode == "Scheduler":
        whatsapp_scheduler()

if __name__ == "__main__":
    main()
