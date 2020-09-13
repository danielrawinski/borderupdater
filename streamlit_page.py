import pandas as pd
import pickle
import streamlit as st
import altair as alt

poland = pickle.load(open("cases_pickle.p", "rb" ))
ratios = pickle.load(open("ratios.p", "rb" ))

now = pd.to_datetime("today").date()
today = pd.to_datetime(poland["Date"].iloc[-1])
  
currentratio = (poland["Count"].iloc[-1] - poland["Count"].iloc[-15])/384
# print(currentratio)
todaycases = poland["Count"].iloc[-1] - poland["Count"].iloc[-2]

if today.dayofweek == 0:
    thisThursday25 = (poland["Count"].iloc[-12] + 9600 - poland["Count"].iloc[-1])/3
    nextThursday25 = (poland["Count"].iloc[-5] + 9600 - poland["Count"].iloc[-1])/10
elif today.dayofweek == 1:
    thisThursday25 = (poland["Count"].iloc[-13] + 9600 - poland["Count"].iloc[-1])/2
    nextThursday25 = (poland["Count"].iloc[-6] + 9600 - poland["Count"].iloc[-1])/9    
elif today.dayofweek == 2:
    thisThursday25 = (poland["Count"].iloc[-14] + 9600 - poland["Count"].iloc[-1])
    nextThursday25 = (poland["Count"].iloc[-7] + 9600 - poland["Count"].iloc[-1])/8   
elif today.dayofweek == 3:
    if currentratio > 25:
        thisThursday25 = "Mandatory self-isolation is to be imposed"
    else:
        thisThursday25 = "Open borders next week"
    nextThursday25 = (poland["Count"].iloc[-8] + 9600 - poland["Count"].iloc[-1])/7
elif today.dayofweek == 4:
    thisThursday25 = (poland["Count"].iloc[-9] + 9600 - poland["Count"].iloc[-1])/6
    nextThursday25 = (poland["Count"].iloc[-2] + 9600 - poland["Count"].iloc[-1])/13
elif today.dayofweek == 5:
    thisThursday25 = (poland["Count"].iloc[-10] + 9600 - poland["Count"].iloc[-1])/5
    nextThursday25 = (poland["Count"].iloc[-3] + 9600 - poland["Count"].iloc[-1])/12
elif today.dayofweek == 6:
    thisThursday25 = (poland["Count"].iloc[-11] + 9600 - poland["Count"].iloc[-1])/4
    nextThursday25 = (poland["Count"].iloc[-4] + 9600 - poland["Count"].iloc[-1])/11
    
# =============================================================================
# Body
# =============================================================================

st.title("Can I cross Polish-Lithuanian border?")
st.write("""Due to ongoing COVID-19 pandemic Lithuania has closed borders with some of neighbours.
The list of countries with restricted status is reviewed every week.
Since September 14th, restrictions are partially relaxed. Entry from Poland to Lithuania is free from Monday, but this may change later.
Note that this page is **not** an official source and you should always double-check for official information before making any decisions.""")
        
st.header("So, now the borders are open, and they will not be closed again?")
st.write(f"""It depends on a situation in Poland on Thursday every week (Lithuania makes decisions for Poland based on Thursdays data). 
If there are less than 25 new COVID-19 cases for 100 thousand people in Poland in the last 14 days, border is open for the next week.
If the number of cases is higher than that, people entering Lithuania will need to go through 14 days long self-isolation (10 days if there is a negative test result).
As of {today.date()}, this ratio stands at **{round(currentratio, 1)}**.""")

st.header("What's going to happen in the next week?")
st.write(f"On {today.date()}, Poland recorded {todaycases} new cases.")

try:
    if thisThursday25 < 0:
        st.write("Mandatory self-isolation is going to be required for those arriving next week.")
    else:
        st.write(f"For borders to be open next week, no more than {round(thisThursday25, 1)} new cases daily must be registered on average by Friday.")
except:
    st.write(thisThursday25)
    
st.header("And the week after the next week?")

try:    
    if nextThursday25 < 0:
        st.write("Mandatory self-isolation is going to be required for those arriving the week after next week.")
    else:
        st.write(f"For borders to be open the week after next week, no more than {round(nextThursday25, 1)} new cases daily must be registered on average by Friday next week.")
except:
    st.write(nextThursday25)
    
st.header("How did this ratio change over time?")
# st.line_chart(ratios["Ratio"])

chart = alt.Chart(ratios).mark_line().encode(
    x = "Date",
    y = "Ratio"
) #st wrap over altair is not too good for this purpose, had to use this directly

st.altair_chart(chart, use_container_width=True)

st.subheader("Sources:")
st.write("""[Lithuanian government coronavirus information](https://koronastop.lrv.lt/)  
[Polish Ministry of Health coronavirus page](https://www.gov.pl/web/koronawirus)  
[CSSE at John Hopkins University - COVID time series](https://github.com/CSSEGISandData/COVID-19)  
[Up to date Polish COVID-19 stats](https://koronawirusunas.pl/)""")

