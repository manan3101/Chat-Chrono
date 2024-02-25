import re                                #regular expression
import pandas as pd

def process(data):                                   # \s\w+  for am and pm 
    pattern="\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s"         #pattern for date and time 
    message=re.split(pattern,data)[1:]          #spilting the data according to pattern and neglecting date/time , taking name and messages only
    dates= re.findall(pattern,data)
    date=[]
    times=[]
    h=[]
    for i in dates:                   # spliting date and time
        date.append(i.split(", ")[0])
        times.append(i.split(", ")[1])

    time=[]
    for i in times:
        h.append(i.split(":")[0])                    # extracting time and neglect am/pm
        time.append(i.split(" -")[0])  #\u202f
    df=pd.DataFrame({
        'user_msg':message,
        'date':date,
        'time':time
    })
    user=[]
    msg=[]
    for i in df['user_msg']:
        x=re.split(": ",i)       #spliting name and message   ([\w\w]+?):\s
        if x[1:]:
            user.append(x[0])     #1
            msg.append(x[1])      #2
        else:
            user.append('Group Notification')
            msg.append(x[0])

    df['user']=user
    df['msg']=msg
    df.drop(columns=['user_msg'],inplace=True)
    df['date'] = pd.to_datetime(df['date'])  
    df['year']=df['date'].dt.year 
    df['month_num']=df['date'].dt.month
    df['month']=df['date'].dt.month_name() 
    df['day']=df['date'].dt.day_name()
    df['day_name']=df['date'].dt.day_name()
    df['date'] = df['date'].dt.date 
    df['hour']=h
    # df['minute']=df['dates'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
     if hour == 23:
        period.append(str(hour) + "-" + '00')
     elif hour == 0:
        period.append('00' + "-" + str(int(hour) + 1))
     else:
        period.append(str(hour) + "-" + str(int(hour) + 1))

    df['period'] = period
    

    return df 
