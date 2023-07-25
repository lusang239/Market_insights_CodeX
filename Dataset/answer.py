import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Reading .csv files
cities = pd.read_csv("dim_cities.csv")
respondent = pd.read_csv("dim_repondents.csv")
survey = pd.read_csv("fact_survey_responses.csv")
df_merge = pd.merge(respondent, survey, "inner", "Respondent_ID")
df = pd.merge(df_merge, cities, "left", "City_ID")

## Primary Insights

# 1.1 Who prefers energy drink more? (male/female/non-binary?)
# Answer: Male and female perfers energy drink more than non-binary; no big difference between male and female
# Method 1: The percentages across the gender groups for each consume frequency option
freq_by_gender = df.groupby(['Gender', 'Consume_frequency']).size().reset_index(name="counts")
freq_by_gender_pct = pd.pivot_table(freq_by_gender, values="counts", index="Gender", columns="Consume_frequency", aggfunc=np.sum, fill_value=0)
freq_by_gender_pct["Total"] = freq_by_gender_pct.sum(axis = 1)

for i in pd.unique(df["Consume_frequency"]):
    freq_by_gender_pct[i+"(%)"] = round(freq_by_gender_pct[i]/freq_by_gender_pct["Total"]*100,2)

freq_by_gender_pct = freq_by_gender_pct.iloc[:,6:]
freq_by_gender_pct = freq_by_gender_pct.T
print(freq_by_gender_pct)
freq_by_gender_pct.plot.barh(title="Percentage of Respondents Across Gender by Consume Frequency ", ylabel="");

# Method 2: Calculate average consume frequency by gender
frequency_mapping = {
    'Daily': 7,
    '2-3 times a week': 2.5,
    'Once a week': 1,
    '2-3 times a month': 0.5,
    'Rarely': 0
}

freq_by_gender_2 = df[["Gender"]]
freq_by_gender_2["freq_mapping"] = df["Consume_frequency"].map(frequency_mapping)
avg_freq_by_gender = round(freq_by_gender_2.groupby("Gender").mean(),2)
print(avg_freq_by_gender)

# Perform T-test to determine if there's a significant difference between male and female
# H0: The average consume frequency of male is same as female
male_data = freq_by_gender_2[freq_by_gender_2["Gender"] == "Male"]["freq_mapping"]
female_data = freq_by_gender_2[freq_by_gender_2["Gender"] == "Female"]["freq_mapping"]

alpha = 0.05
t_stat, p_value = ttest_ind(male_data, female_data, equal_var=False)
if p_value < alpha:
    print("The t-test result is statistically significant.")
    print(f"P-value: {p_value:.5f}")
else:
    print("The t-test result is not statistically significant.")
    print(f"P-value: {p_value:.5f}")

# 1.2 Which age group prefers energy drinks more?
# Answer: 31 - 45
# Method 1: The percentages across the age groups for each consume frequency option
freq_by_age = df.groupby(['Age', 'Consume_frequency']).size().reset_index(name="counts")
freq_by_age_pct = pd.pivot_table(freq_by_age, values="counts", index="Age", columns="Consume_frequency", aggfunc=np.sum, fill_value=0)
freq_by_age_pct["Total"] = freq_by_age_pct.sum(axis = 1)

for i in pd.unique(df["Consume_frequency"]):
    freq_by_age_pct[i+"(%)"] = round(freq_by_age_pct[i]/freq_by_age_pct["Total"]*100,2)

freq_by_age_pct = freq_by_age_pct.iloc[:,6:]
freq_by_age_pct = freq_by_age_pct.T
print(freq_by_age_pct)
freq_by_age_pct.plot.barh(title="Percentage of Respondents Across Age by Consume Frequency ", ylabel="");

# Method 2: Calculate average consume frequency by age
frequency_mapping = {
    'Daily': 7,
    '2-3 times a week': 2.5,
    'Once a week': 1,
    '2-3 times a month': 0.5,
    'Rarely': 0
}

freq_by_age_2 = df[["Age"]]
freq_by_age_2["freq_mapping"] = df["Consume_frequency"].map(frequency_mapping)
avg_freq_by_age = round(freq_by_age_2.groupby("Age").mean(),2)
print(avg_freq_by_age)

# 1.3 Which type of marketing reaches the most Youth (15-30)?
# Answer: Online ads
youth_mkt_count = df[df["Age"].isin(["15-18", "19-30"])]["Marketing_channels"].value_counts()
youth_mkt_count.plot.bar(rot = 45, title="Number of Youth (15-30) by Marketing Channels ",xlabel = "")

# 1.4 Which type of marketing reaches the most respondents age betweeen (31-45)?
# Answer: TV Commercials
youth_mkt_count = df[df["Age"] == "31-45"]["Marketing_channels"].value_counts()
print(youth_mkt_count)

# 1.5 What type of marketing reaches the most for each age group?
# Answer: Online Ads for Youth (15-30); TV Commercials for Adults (31 - 65+)
mkt_by_age = df[["Age", "Marketing_channels"]].value_counts().reset_index(name="counts")
mkt_by_age = pd.pivot_table(mkt_by_age, index="Age", columns="Marketing_channels", values="counts", aggfunc=np.sum, fill_value=0)
print(mkt_by_age)
mkt_by_age.plot.bar(title="Number of Respondents Reached Through Marketing Channels by Age", rot=0, xlabel="")

# 2.1 What are the preferred ingredients of energy drinks among respondents?
# Answer: Caffeine > Vitamins > Sugar > Guarana
df_ingradients = df["Ingredients_expected"].value_counts()
df_ingradients.plot.bar(rot = 0, title="Expected Ingredients Among Respondents",xlabel="")

# 2.2 What packaging preferences do respondents have for energy drinks?
# Answer: Compact and portable cans
df_packaging = df["Packaging_preference"].value_counts()
df_packaging.sort_values(ascending=True).plot.barh(title="Packaging Preferences for Energy Drinks", ylabel="")

# 2.3 Does most of respondents have concern about the health impact of energy drinks?
# Answer: Yes (60.45%)
health_concern = df["Health_concerns"].value_counts()
print(health_concern)

# 2.4  Will respondents be more interest in energy drinks with natural or organic ingredients?
# Answer: Yes (49.83%)
interest_in_natural = df["Interest_in_natural_or_organic"].value_counts()
print(interest_in_natural)

# 3.1 Who are the current market leaders?
#  Answer: Cola-Coka 
df_brands = df[["Current_brands"]].value_counts().reset_index(name="counts").set_index("Current_brands")
df_brands["Market_share(%)"] = round(df_brands["counts"]/sum(df_brands["counts"])*100,2)
print(df_brands)
df_brands["Market_share(%)"].plot.pie(title = "Current Marketing Leaders", label="")

# 3.2 What are the primary reasons consumers prefer those brands over ours?
# Answer: Brand reputation
reasons_over_us = df[df["Current_brands"] != "CodeX"]["Reasons_for_choosing_brands"].value_counts()
reasons_over_us

# 3.3 What are the primary reasons consumers prefer our brand?
# Answer: Brand reputation
reasons_on_us = df[(df["Tried_before"] == "Yes") & (df["Heard_before"] == "Yes") & (df["Current_brands"] == "CodeX")]["Reasons_for_choosing_brands"].value_counts()
reasons_on_us

# 4.1 Which marketing channel can be used to reach more customers?
# Answer: Online ads
mkt_channel = df['Marketing_channels'].value_counts()
mkt_channel

# 4.2 How effective are different marketing strategies and channels in reaching our customers?
# Answer: TV commercials (conversion rate = 46.76%)
# Conversion Rate (%) = (Number of Customers Converted via channel A who have "Heard_before" (Yes) / Number of Customers Reached via channel A) * 100
df_mkt_effectiveness = df[["Marketing_channels", "Heard_before"]].value_counts().reset_index(level="Heard_before", name="Counts")
df_mkt_effectiveness = pd.pivot_table(df_mkt_effectiveness, index="Marketing_channels",values="Counts", columns="Heard_before")
df_mkt_effectiveness["conversion_rate(%)"] = round(df_mkt_effectiveness["Yes"]/(df_mkt_effectiveness["Yes"]+df_mkt_effectiveness["No"])*100,2)
print(df_mkt_effectiveness.sort_values(by="conversion_rate(%)", ascending=False))

# 5.1 What do people think about our brand? (overall rating)
# Answer: 3.28 (Between Average and Good)
avg_rate = round(df[(df["Heard_before"] == "Yes") & (df["Tried_before"] == "Yes")]["Taste_experience"].mean(),2)
avg_rate

# 5.2 Which cities do we need to focus more on?
# Answer: Kolkata (Brand Awareness Index= 37.10%)
# Brand Awareness Index (%) = (Yes / Total Respondents in the city) * 100
city_awareness = df[["City", "Heard_before"]].value_counts().reset_index(name = "counts")
city_awareness = pd.pivot_table(city_awareness, index = "City", columns = "Heard_before", values = "counts", aggfunc=np.sum, fill_value=0)
city_awareness["Total"] = city_awareness.sum(axis = 1)
city_awareness["Awareness(%)"] =  round(city_awareness["Yes"]/city_awareness["Total"]*100,2)
print(city_awareness["Awareness(%)"].sort_values(ascending=False))
city_awareness["Awareness(%)"].sort_values().plot.barh(title="Brand Awareness(%) in City",ylabel="")

# 6.1 Where do respondents prefer to purchase energy drinks?
# Answer: Supermarkets
df_place = df["Purchase_location"].value_counts()
df_place.plot.bar(title="Ranking of Purchase location", xlabel="", rot=45)

# 6.2 What are the typical consumption situations for energy drinks among respondents?
# Answer: Sports/exercise
df_situation = df["Typical_consumption_situations"].value_counts()
df_situation.sort_values(ascending=True).plot.barh(title="Ranking of Typical Consumption Situation",ylabel="")

# 6.3 What factors influence respondents' purchase decisions, such as price range and limited edition packaging?
# Answer: Most reasonable price range is 50-99; 
df_price = df["Price_range"].value_counts()
print(df_price)
df_price.plot.bar(title="What is the most reasonable price?",xlabel="", rot=0)

# Limited edition packaging might be somewhat appealing to a significant portion of the surveyed population but might not be a decisive factor for everyone. 
df_limited_packaging = df["Limited_edition_packaging"].value_counts()
print(df_limited_packaging)
df_limited_packaging.plot.pie(title="Is Limited Edition Packaging appealing?",label="")

# 7.1 Which area of business should we focus more on our product development? (Branding/taste/availability)
# Answer: "Health concerns" and "Not interested in energy drinks"
df_prevent_reasons = df[(df["Heard_before"] == "Yes") & (df["Tried_before"] == "No")]["Reasons_preventing_trying"].value_counts()
print(df_prevent_reasons)
df_prevent_reasons.sort_values(ascending=True).plot.barh(title="What areas should we focus more on?",ylabel="")

# 7.2 What is the main improvement that respondents would like to see in the current energy drinks market?
# Answer: Reduced sugar content
expected_improvement = df["Improvements_desired"].value_counts()
print(expected_improvement)
expected_improvement.sort_values(ascending=True).plot.barh(title="Ranking of Expected Improvement for Current Energy Market",ylabel="")

# 7.3 What is the main reason to cause a “below average” rate of overall product experience?
# Answer: Health concerns, not interested in energy drinks, not available locally
low_rate_causation = df[df["Tried_before"] == "Yes"][["Taste_experience", "Reasons_preventing_trying"]].value_counts().reset_index(name = "counts")
low_rate_causation = pd.pivot_table(low_rate_causation, index = "Taste_experience", columns = "Reasons_preventing_trying", values="counts", fill_value=0, aggfunc=np.sum)
print(low_rate_causation)
low_rate_causation.plot.bar(title="What lead to the overall rating?",rot = 0)
