
import altair as alt
import pandas as pd
import streamlit as st
import kmeans as km
import app_k as k
import mona as m
import matplotlib.pyplot as plt
import seaborn as sns

source = pd.read_csv('./refined_insurance.csv')
source2 = pd.read_csv('./refined_insurance_2.csv')
source3 = pd.read_csv('./refined_insurance_3.csv')



source = pd.read_csv('./refined_insurance.csv')

input_dropdown = alt.binding_select(options=[True,False,[True&False]], name='Smoker')
selection = alt.selection_single(fields=['smoker'], bind=input_dropdown)


TotalPPP_age_bmi = alt.Chart(source).mark_bar().encode(
    x=alt.X('BMI Category:O',sort=['<25','26 - 35','36+']),
    y='mean(Total 2022 PPP expenses):Q',
    color= alt.Color("smoker:N", type="nominal",scale=alt.Scale(range=['#800000', ' #63ba97']),legend=alt.Legend(columns=2)),
    column=alt.Column('Age Category:N',header=alt.Header(titleFontSize=20,titleColor='White',labelColor='White',labelFontSize=25)),
    tooltip=alt.Tooltip('smoker:N', title='smoker:N'),
).interactive().properties(width=200,height=300).configure_axis(
    grid=False, labelFontSize=20, titleFontSize = 20
).configure_legend(labelFontSize = 15,titleFontSize=15).configure_view(
    strokeWidth=0
)

Forward_age_bmi = alt.Chart(source).mark_bar().encode(
    x=alt.X('BMI Category:O',sort=['<25','26 - 35','36+']),
    y='mean(Forward PPP expenses):Q',
    color= alt.Color("smoker:N", type="nominal",scale=alt.Scale(range=['#800000', ' #63ba97']),legend=alt.Legend(columns=2)),
    column=alt.Column('Age Category:N',header=alt.Header(titleFontSize=20,titleColor='White',labelColor='White',labelFontSize=25)),
    tooltip=alt.Tooltip('smoker:N', title='smoker:N'),
).interactive().properties(width=200,height=300).configure_axis(
    grid=False, labelFontSize=20, titleFontSize = 20
).configure_legend(labelFontSize = 15,titleFontSize=15).configure_view(
    strokeWidth=0
)

ProPrice_age_bmi = alt.Chart(source).mark_bar().encode(
    x=alt.X('BMI Category:N',sort=['<25','26 - 35','36+']),
    y=alt.Y('mean(proposed_price):Q',scale=alt.Scale(domain=[0, 12000])),
    color= alt.Color("smoker:N", type="nominal",scale=alt.Scale(range=['#800000', ' #63ba97']),legend=alt.Legend(columns=2)),
    column=alt.Column('Age Category:N',header=alt.Header(titleFontSize=20,titleColor='White',labelColor='White',labelFontSize=25)),
    tooltip=alt.Tooltip('smoker:N', title='smoker:N'),
).interactive().properties(width=200,height=300).configure_axis(
    grid=False, labelFontSize=20, titleFontSize = 20
).configure_legend(labelFontSize = 15,titleFontSize=15).configure_view(
    strokeWidth=0
)

slider = alt.binding_range(min=.1, max=.4, step=.1)
select_margin = alt.selection_single(name='Operating Margin', fields=['Operating Margin'],
                                   bind=slider, init={'Operating Margin': .4})

base = alt.Chart(source3).add_selection(
    select_margin
).transform_filter(select_margin).properties(
    width=250
)

left = base.encode(
    x=alt.X('Revenue Impact:Q',scale=alt.Scale(domain=(-160000,0)),axis=alt.Axis(grid=False,domain=False,tickSize=0,title='Revenue Impact',titleFontSize= 20,labelFontSize= 15)),
    y=alt.Y('Rev_scale:N',axis= alt.Axis(title='',grid=False,domain=False,tickSize=0,offset=10,labels=False)),
    color = alt.value('maroon')
).mark_bar(size=60).interactive()

right = base.encode(
    x=alt.X('Net Profit Impact:Q',scale=alt.Scale(domain=(0,160000)),axis=alt.Axis(grid=False,domain=False,tickSize=0,title='Net Profit Impact',titleFontSize= 20,labelFontSize= 15)),
    y=alt.Y('NP_scale:N',axis= alt.Axis(title='',grid=False,domain=False,tickSize=0,offset=10,labels=False)),
    color = alt.value('green')
).mark_bar(size=60)

### APP
st.image('./Forward Pic.jpg')

new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">TEAM SLAM DUNKS FORWARD</p>'
st.markdown(new_title, unsafe_allow_html=True)

st.markdown('''
## Problem Statement

US healthcare lacks a preventative approach and costs are rising.

Background: 
1. Currently Americans spend \\$2,437 (See Chart Below)  on average per capita on Primary, Preventative, and Prescription(PPP) care and GoForward.com provides PPP care for only \\$1788 annually per capita. 
2. Currently GoForwards \\$1,788 is an additional subscription based fee on top of regular insurance fees.
3. Goforward presents a solution that does not tailor to individual circumstances so we wanted to propose a pricing methodology that would decrease individual PPP expenses, and increase revenue for companies like GoForward through government tax breaks and category based pricing.
4. Our proposed pricing methodology improves PPP accessibility for people by decreasing rates for younger, lower BMI, and non-smokers and many would pay less than forwards 149/month model

''')

st.markdown('''
## Proposal

See chart for proposed pricing schema to replace GoForwards current \\$149/month. Proposed price is ~\\$1,701 on Average Per Capita and would be paid through income tax deduction in liu of current PPP insurance plan:

''')
p_c = pd.read_csv('ppc.csv')

st.table(p_c)

st.altair_chart(k.Benefit_by_age)

# Forward_title = '<p style="font-family:sans-serif; color:White; font-size: 18px;">Forward\'s $1,788 annual price (see below chart) is not cost effective per capita as an additional subscription expense and reduces opportunity to increase Forwards Revenue with government sponsored tax breaks </p>'
# st.markdown(Forward_title, unsafe_allow_html=True)



st.altair_chart(k.ben_age_bmi)


st.markdown('''
## Business Impact Analysis

From a business standpoint, a forward model with our proposed pricing model definitely results in a lower top-line. We identified this during our analysis but it was generally to the tune of 5%.

To address potentially decreased incentive, we additionally propose that the government provided a tax cut depending on how efficient a company is at managing its expenses. 
Along those lines, we think the tax rate cut should be 25%, 50%, 75%, and 100 percent if the company in question achieved 10%, 20%, 30%, or 40% Operating Margin, respectively.

The chart below showcases that, while companies would see a general decline in top-line, such tax rate cuts would result in a substantial increase to bottom-line - more than compensating for the decline in revenues.


''')


col1, col2 = st.columns(2)

with col1:
    st.altair_chart(alt.concat(left,right,spacing = 0).configure_view(width=250,height=200,strokeWidth = 0))

    source3.loc[:, "Operating Margin"] =source3["Operating Margin"].map('{:.2%}'.format)
    source3 = source3.set_index('Operating Margin')

with col2:

    st.write(source3[['Revenue Impact','Net Profit Impact']],use_container_width = True)

st.sidebar.image(image='./slam.jpg',width=200)

team_title = '<p style="font-family:sans-serif; color:Green; font-size: 18px;">TEAM MEMBERS</p>'
st.sidebar.markdown(team_title,unsafe_allow_html=True)
st.sidebar.write('*Khalid Almasri*')
st.sidebar.write('*Sid Beck*')
st.sidebar.write('*Monali Sheetal*')

about_title = '<p style="font-family:sans-serif; color:Green; font-size: 14px;">About:</p>'
st.sidebar.markdown(about_title, unsafe_allow_html= True)
st.sidebar.markdown('''##### People pay too much for healthcare in america.
##### This project aims to propose government tax breaks for insurance free medical provider networks.
##### Decreasing Primary, Preventative, and Prescription (PPP) care costs for all Americans through a split pricing schema dependent on age, bmi, and smoker status for companies like GoForward.com.''')

st.sidebar.markdown('## Sources')
source_title = '<p style="font-family:sans-serif; color:LightBlue; font-size: 14px;">https://www.kaggle.com/datasets/annetxu/health-insurance-cost-prediction</p>'
st.sidebar.markdown(source_title, unsafe_allow_html= True)
source_title = '<p style="font-family:sans-serif; color:LightBlue; font-size: 14px;">https://goforward.com/</p>'
st.sidebar.markdown(source_title, unsafe_allow_html= True)

st.markdown('''## Kmeans Clustering (3 Groups identified)
The Cluster models below compare age and bmi to healthcare costs. The three groups identified are likely Healthy (at the bottom in white), midgrade health group which
would account for those sick or potentially soon to be cronically ill (light blue), the last group with the highest bills seems to identify cronically ill people with the 
highests expenses (dark blue).''')

st.altair_chart(km.cluster1)

st.markdown('''## Kmeans Clustering(identify where smokers fit in the groups, and who benifits from new price)
The Cluster below show the age group from above with two separate color encodings, one the left is showing smokers in orange and on
the right orange depicts those who would financially benifit from our proposed price for Forward-like PPP care.''')

st.altair_chart(km.cluster2)


st.pyplot(m.age_smoker_bar)
st.pyplot(m.smoker_age_box)
st.pyplot(m.smoker_bmi_box)
st.pyplot(m.smoker_expense_box)









