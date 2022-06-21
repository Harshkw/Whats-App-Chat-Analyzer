import re
import pandas as pd
def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    messages_df = pd.DataFrame({"messages": messages, "dates": dates})

    messages_df["dates"] = pd.to_datetime(messages_df["dates"], format = "%d/%m/%Y, %H:%M - ")

    # separate users and messages
    users = []
    message = []
    for text in messages_df["messages"]:
        splited = re.split("([\w\W]+?):\s", text)
        if splited[1:]:
            users.append(splited[1])
            message.append(splited[2])

        else:
            users.append("Group_Notification")
            message.append(splited[0])

    messages_df["users"] = users
    messages_df["message"] = message
    messages_df.drop(columns = ["messages"], inplace = True)
    messages_df["month"] = messages_df["dates"].dt.month_name()
    messages_df["month_num"] = messages_df["dates"].dt.month
    messages_df["day"] = messages_df["dates"].dt.day
    messages_df["hour"] = messages_df["dates"].dt.hour
    messages_df["minutes"] = messages_df["dates"].dt.minute
    messages_df["year"] = messages_df["dates"].dt.year
    messages_df["day_name"] = messages_df["dates"].dt.day_name()

    period = []
    for hour in messages_df[['day_name','hour']]['hour']:
        if hour == 23 :
            period.append (str(hour) + "-" + str('00'))

        elif hour == 0 :
            period.append(str('00') + "-" + str(hour + 1))

        else :
            period.append(str(hour) + "-" + str(hour + 1)) 

    messages_df["period"] = period

    return messages_df