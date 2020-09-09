import pandas as pd
import pickle
import streamlit as st
import altair as alt

poland = pickle.load(open("cases_pickle.p", "rb" ))
ratios = pickle.load(open("ratios.p", "rb" ))

now = pd.to_datetime("today").date()
today = pd.to_datetime(now)
# today.dayofweek
  
currentratio = (poland["Count"].iloc[-1] - poland["Count"].iloc[-15])/384
# print(currentratio)
todaycases = poland["Count"].iloc[-1] - poland["Count"].iloc[-2]

if today.dayofweek == 0:
    thisThursday16 = (poland["Count"].iloc[-12] + 6144 - poland["Count"].iloc[-1])/3
    nextThursday16 = (poland["Count"].iloc[-5] + 6144 - poland["Count"].iloc[-1])/10
    thisThursday25 = (poland["Count"].iloc[-12] + 9600 - poland["Count"].iloc[-1])/3
    nextThursday25 = (poland["Count"].iloc[-5] + 9600 - poland["Count"].iloc[-1])/10
elif today.dayofweek == 1:
    thisThursday16 = (poland["Count"].iloc[-13] + 6144 - poland["Count"].iloc[-1])/2
    nextThursday16 = (poland["Count"].iloc[-6] + 6144 - poland["Count"].iloc[-1])/9
    thisThursday25 = (poland["Count"].iloc[-13] + 9600 - poland["Count"].iloc[-1])/2
    nextThursday25 = (poland["Count"].iloc[-6] + 9600 - poland["Count"].iloc[-1])/9    
elif today.dayofweek == 2:
    thisThursday16 = (poland["Count"].iloc[-14] + 6144 - poland["Count"].iloc[-1])
    nextThursday16 = (poland["Count"].iloc[-7] + 6144 - poland["Count"].iloc[-1])/8
    thisThursday25 = (poland["Count"].iloc[-14] + 9600 - poland["Count"].iloc[-1])
    nextThursday25 = (poland["Count"].iloc[-7] + 9600 - poland["Count"].iloc[-1])/8   
elif today.dayofweek == 3:
    if currentratio > 25:
        thisThursday16 = "Border will be closed for non-Lithuanians next week, mandatory self-isolation for Lithuanians imposed"
        thisThursday25 = "Border will be closed for non-Lithuanians next week, mandatory self-isolation for Lithuanians imposed"
    elif currentratio < 16:
        thisThursday16 = "Borders will be open next week"
        thisThursday25 = "Borders will be open next week"
    else:
        thisThursday16 = "Mandatory self-isolation upon arrival to Lithuania next week"
        thisThursday25 = "Mandatory self-isolation upon arrival to Lithuania next week"
    nextThursday16 = (poland["Count"].iloc[-8] + 6144 - poland["Count"].iloc[-1])/7
    nextThursday25 = (poland["Count"].iloc[-8] + 9600 - poland["Count"].iloc[-1])/7
elif today.dayofweek == 4:
    thisThursday16 = (poland["Count"].iloc[-9] + 6144 - poland["Count"].iloc[-1])/6
    nextThursday16 = (poland["Count"].iloc[-2] + 6144 - poland["Count"].iloc[-1])/13
    thisThursday25 = (poland["Count"].iloc[-9] + 9600 - poland["Count"].iloc[-1])/6
    nextThursday25 = (poland["Count"].iloc[-2] + 9600 - poland["Count"].iloc[-1])/13
elif today.dayofweek == 5:
    thisThursday16 = (poland["Count"].iloc[-10] + 6144 - poland["Count"].iloc[-1])/5
    nextThursday16 = (poland["Count"].iloc[-3] + 6144 - poland["Count"].iloc[-1])/12
    thisThursday25 = (poland["Count"].iloc[-10] + 9600 - poland["Count"].iloc[-1])/5
    nextThursday25 = (poland["Count"].iloc[-3] + 9600 - poland["Count"].iloc[-1])/12
elif today.dayofweek == 6:
    thisThursday16 = (poland["Count"].iloc[-11] + 6144 - poland["Count"].iloc[-1])/4
    nextThursday16 = (poland["Count"].iloc[-4] + 6144 - poland["Count"].iloc[-1])/11
    thisThursday25 = (poland["Count"].iloc[-11] + 9600 - poland["Count"].iloc[-1])/4
    nextThursday25 = (poland["Count"].iloc[-4] + 9600 - poland["Count"].iloc[-1])/11
    
# print(thisThursday16)
# print(nextThursday16)
# print(thisThursday25)
# print(nextThursday25)

# =============================================================================
# Body
# =============================================================================

st.header("Can I cross Polish-Lithuanian border?")
st.write("""Due to ongoing COVID-19 pandemic Lithuania has closed borders with some of neighbours.
The list of countries with restricted status is reviewed every week.
Since August 10th, mandatory self-isolation was reintroduced for those coming from Poland.
In addition to this, at the moment, those coming from Poland to Lithuania need to have a negative Covid-19 test, done before (for foreigners) or after (for Lithuanians) crossing the border. Exceptions apply.""")
        
st.header("So, when I will be able to come to Lithuania without restrictions?")
st.write(f"""It depends on a situation in Poland. 
If there are less than 16 new COVID-19 cases for 100 thousand people in the last 14 days, border restrictions are removed.
If the number of cases is between 16 and 25 per 100 thousand people in the last 14 days, self-isolation period upon arrival is mandatory.
If the number of cases is above 25 per 100 thousand people in the last 14 days, in addition to self-isolation, mandatory testing is introduced; for foreigners, test should be done prior to crossing the border, Lithuanian citizens may do it after coming.
As of {today.date()}, this ratio stands at *{currentratio}*""")

st.header("What's going to happen in the next week?")
st.write(f"Today, Poland recorded {todaycases} new cases.")

if thisThursday16 < 0:
    st.write("There is no chance of complete border opening next week.")
else: 
    st.write(f"For borders to be open without restrictions next week, no more than {thisThursday16} new cases daily must be registered on average by Friday.")
    
if thisThursday25 < 0:
    st.write("Mandatory self-isolation + testing next week")
else:
    st.write(f"For testing not to be mandatory next week, no more than {thisThursday25} new cases daily must be registered on average by Friday.")

st.header("And week after the next week?")

if nextThursday16 < 0:
    st.write("There is no chance of complete border opening the week after next week.")
else: 
    st.write(f"For borders to be open without restrictions the week after next week, no more than {nextThursday16} new cases daily must be registered on average by Friday next week.")

if nextThursday25 < 0:
    st.write("Mandatory self isolation + testing the week after next week.")
else:
    st.write(f"For testing not to be mandatory the week after next week, no more than {nextThursday25} new cases daily must be registered on average by Friday next week.")

st.header("How did this ratio change over time?")
# st.line_chart(ratios["Ratio"])

chart = alt.Chart(ratios).mark_line().encode(
    x = "Date",
    y = "Ratio"
) #st wrap over altair is not too good for this purpose, had to use this directly

st.altair_chart(chart, use_container_width=True)
