import streamlit as st
import pandas as pd
import altair as alt
import datetime

coe_data = pd.read_csv('coe_data.csv')
coe_data['month'] = pd.to_datetime(coe_data['month']).dt.date

# Streamlit app layout
st.set_page_config(page_title='COE-A-Scope',layout='wide')
st.title("🚗 COE-A-Scope, An analysis of Singapore COE Premiums (Category A)")

bidding_rounds = st.multiselect('Select Bidding Rounds', [1,2], default=[1,2])
date_range = st.slider(
    'Select Date Range', 
    min_value=min(coe_data['month']), 
    max_value=max(coe_data['month']), 
    value=(min(coe_data['month']), max(coe_data['month'])), 
    format="YYYY-MM"
)
filtered_data = coe_data[
    (coe_data['bidding_no'].isin(bidding_rounds)) &
    (coe_data['month'].between(date_range[0], date_range[1]))
]

# First Visual
st.subheader("Visual (1)")
line = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('yearmonth(month):T'),
    y=alt.Y('adjusted_premium:Q', title='Adjusted Premium ($)'),
    color=alt.Color('bidding_no:N', scale=alt.Scale(domain=[1, 2], range=['#E9E9E9', '#B82E2E']))
)
bar = alt.Chart(filtered_data).mark_bar(opacity=0.3).encode(
    x=alt.X('yearmonth(month):T', axis=alt.Axis(format='%Y', title='Year')),
    y=alt.Y('mean(quota):Q', title='Average Quota', axis=alt.Axis(grid=False)),
    color=alt.value('#AAAAAA')
)
combined_chart = alt.layer(bar, line).resolve_scale(
    y='independent'
).properties(
    title='COE Premiums Over Time for Bidding Rounds 1 and 2 (Adjusted for Inflation) with Quota'
)
st.altair_chart(combined_chart, use_container_width=True)
st.write("- COE premiums exhibit a cyclical pattern, with significant peaks around 2013 and 2023, indicating a possible 10-year cycle.")
st.write("- This may be tied to the 10-year validity period of COEs, influencing renewal and bidding behaviors.")
st.write("- Bidding round 2 often shows higher premiums than round 1, particularly from 2020 onward, potentially due to bidders reacting to round 1 prices.")
st.write("- COE premiums and quotas seem to be inversely proportional. As the quota increases, premiums tend to decrease, and vice versa, particularly evident during periods of significant quota changes.")

# Second Visual
st.subheader("Visual (2)")
scatter = alt.Chart(filtered_data).mark_point().encode(
    x=alt.X('quota:Q', title='Quota'),
    y=alt.Y('adjusted_premium:Q', title='Adjusted COE Premium'),
    color=alt.Color('bidding_no:N', scale=alt.Scale(domain=[1, 2], range=['#E9E9E9', '#B82E2E'])),
    tooltip=['month:T', 'quota:Q', 'adjusted_premium:Q', 'bidding_no:N']
)
trend_line = scatter.transform_regression(
    'quota', 'adjusted_premium', groupby=['bidding_no']
).mark_line()
combined_chart = alt.layer(scatter, trend_line).properties(
    title='Scatterplot of COE Premium (Adjusted for Inflation) vs Quota with Trend Line'
)
st.altair_chart(combined_chart, use_container_width=True)
st.write('- This inverse relationship between quota and COE premiums is further evidenced by the scatter plot above.')

# Third Visual
st.subheader("Visual (3)")
chart2 = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X(
        'yearmonth(month):T', 
        axis=alt.Axis(format='%Y', title='Year')
    ),
    y=alt.Y('bid_ratio:Q', title='Bid Ratio (Bids Success/Bids Received)'),
    color=alt.Color('bidding_no:N', scale=alt.Scale(domain=[1, 2], range=['#E9E9E9', '#B82E2E']))
).properties(
    title='Bid Ratio (Bids Success/Bids Received) Over Time for Bidding Rounds 1 and 2'
)
st.altair_chart(chart2, use_container_width=True)
st.write("- Both rounds exhibit significant fluctuations in bid ratios, often synchronized, suggesting that they are influenced by similar factors.")
st.write("- The most notable dip in Bid Ratio occurred around 2013, a period marked by increased competition, which drove premiums to a sharp peak, as seen in the earlier visual.")

# Forth Visual
st.subheader("Visual (4)")
bar_chart = alt.Chart(filtered_data).mark_bar(color='#E9E9E9').encode(
    x=alt.X('month(month):N', title='Month', sort=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']),
    y=alt.Y('mean(relative_avg_premium):Q', title='Average of Relative Average Adjusted Premium', 
            scale=alt.Scale(domain=[0.8, 1.1])),
    tooltip=['mean(relative_avg_premium):Q']
).properties(
    title='Average of Relative Average Adjusted Premium by Month (Compared to Yearly Average)'
)
st.altair_chart(bar_chart, use_container_width=True)
st.write('- February typically has the lowest premiums relative to the yearly average, while December tends to see the highest premiums.')
st.write('- Additionally, there is a noticeable seasonal pattern, with the first half of the year (January to June) generally offering lower premiums than the latter half (July to December).')

st.text("Last Updated: 13/9/2024 (Updates Trimonthly)")
st.text("Filtered Category A for Singapore COE Premiums")
st.text("By: Hong Kai")