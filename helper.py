from urlextract import URLExtract
extract = URLExtract()
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import emoji
from twilio.rest import Client


def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]

    num_media = df[df['msg'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['msg']:
        extracted_urls = extract.find_urls(message)
        links.extend(extracted_urls)
    return num_messages,num_media,len(links)

def most_active_user(df):
    x=df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percentage'})
    return x,df

def create_cloud(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='Group Notification']
    temp=temp[temp['msg']!='<Media omitted>\n']
    wc=WordCloud(width=1000,height=500,min_font_size=5,background_color='white')
    df_wc=wc.generate(temp['msg'].str.cat(sep=" "))
    return df_wc

def emoji_helper(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['msg']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df   

def monthly_timeline(selected_user,df):
     if selected_user!='overall':
        df=df[df['user']==selected_user]
     timeline=df.groupby(['year','month_num','month']).count()['msg'].reset_index()
     time=[]
     for  i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
     timeline['time']=time
     return timeline

def week_activity_map(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()


def activity_heatmap(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    user_heatmap = pd.pivot_table(df,index='day_name', columns='period', values='msg', aggfunc='count').fillna(0)
    return user_heatmap



def send_whatsapp_message(sender_number, message, scheduled_time):
    # Your Twilio credentials
    TWILIO_ACCOUNT_SID = 'Enter your account sid'
    TWILIO_AUTH_TOKEN = 'enter your auth token'

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        # Send message
        message = client.messages.create(
            body=message,  # The body of the message
            from_='whatsapp:enter your number',  # Twilio WhatsApp sandbox number
            to=f'whatsapp:+91{sender_number}',  # Recipient's WhatsApp number with country code
            messaging_service_sid='enter your message service sid',  # Messaging Service SID
            # Schedule message if scheduled_time is provided
            schedule_type='fixed',  # Type of schedule (fixed for one-time schedule)
            send_at=scheduled_time.strftime('%Y-%m-%dT%H:%M:%SZ')  # Scheduled time in UTC format
        )
        print(message.sid)
        return message.sid

    except Exception as e:
        print(f"Error occurred: {str(e)}")
     