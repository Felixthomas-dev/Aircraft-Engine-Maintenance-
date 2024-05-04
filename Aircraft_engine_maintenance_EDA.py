#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install missingno')


# In[2]:


# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import missingno as msno
import sklearn as sk
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[3]:


# Load the generated dataset
df = pd.read_csv("aircraft_engine_maintenance.csv")
Aircraft_engine = df
Aircraft_engine


# In[4]:


# Display the first few rows of the dataset
Aircraft_engine.head(10)


# In[5]:


Aircraft_engine.tail(10)


# In[6]:


Aircraft_engine.shape


# In[7]:


# Summary Statistics
Aircraft_engine.info()


# In[8]:


# Summary Statistics
Aircraft_engine.describe()


# ### Handle missing values

# In[9]:


# Check for missing values
Aircraft_engine.isnull().sum()


# In[10]:


# Display columns with missing values

msno.bar(Aircraft_engine, color="blue")


# In[11]:


#Visualize the missing data
sns.heatmap(Aircraft_engine.isnull())
plt.title("Missing Values")


# In[12]:


# Handling missing values (replace with median value)
numImputer = SimpleImputer(missing_values=np.nan, strategy='median')

numImputer = numImputer.fit(Aircraft_engine[['Temperature', 'Pressure']])

Aircraft_engine[['Temperature', 'Pressure']]=numImputer.transform(Aircraft_engine[['Temperature', 'Pressure']])


# In[13]:


# Check for missing values after filling it up with median value
Aircraft_engine.isnull().sum()


# In[14]:


# Check for duplicate values
Aircraft_engine.duplicated().sum()


# ### Handling outliers

# In[15]:


numerical_columns = ["Unnamed: 0", "Engine_ID", "Temperature", "Pressure", "Rotational_Speed", "Engine_Health"]


# In[16]:


# Calculate IQR for each column
q1 = Aircraft_engine[numerical_columns].quantile(0.25)
q3 = Aircraft_engine[numerical_columns].quantile(0.75)

iqr = q3 - q1

# Identify outliers using IQR
lower_bound = q1 - (1.5 * iqr)
upper_bound = q3 + (1.5 * iqr)

outliers = ((Aircraft_engine[numerical_columns] < lower_bound) | (Aircraft_engine[numerical_columns] > upper_bound)).any(axis=1)

# Display the number of outliers
print(outliers.sum())

# Display the outlier records
Aircraft_engine[outliers]


# In[17]:


# Remove outliers based on IQR
Aircraft_engine =  Aircraft_engine[~outliers]

# Display the dataset after handling outliers
Aircraft_engine


# ### Univariate Analysis:

# In[18]:


# Defining the columns for univariate analysis
columns_needed = ["Temperature", "Pressure", "Rotational_Speed", "Engine_Health"]


plt.figure(figsize=(15, 10))

for idx, column in enumerate(columns_needed, 1):
    plt.subplot(2, 2, idx)                                                                
    sns.histplot(data=Aircraft_engine[column], bins=20, kde=True)      
    plt.title(f"{column} Distribution")                                 
    plt.xlabel(column)                                                  
    plt.ylabel("Frequency")                                              

plt.tight_layout()
plt.show()


# In[ ]:





# ### Bivariate Analysis:

# In[19]:


# Bivariate analysis - Pairplot
Aircraft_engine_clean = Aircraft_engine.drop(columns=["Unnamed: 0", "Engine_ID"])

# Create a pairplot with the cleaned DataFrame
sns.pairplot(data=Aircraft_engine_clean, hue='Engine_Failure')
plt.suptitle("Pairplot of Features with Engine Failure", y=1.02)


# ### Multivariate Analysis:

# In[20]:


plt.figure(figsize=(10, 8))
correlation_matrix = Aircraft_engine[columns_needed].corr()
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()


# In[21]:


# Data visualization - Time Series of Engine Health
plt.figure(figsize=(15, 6))
sns.lineplot(x="Timestamp", y="Engine_Health", data=Aircraft_engine, hue="Engine_ID", marker="o", markersize=5)
plt.title("Time Series of Engine Health")
plt.xlabel("Timestamp")
plt.ylabel("Engine Health")
plt.legend(title="Engine ID", loc="upper right", bbox_to_anchor=(1.2, 1))
plt.show()


# In[39]:


# Data visualization - Time Series of "Temperature", "Pressure", "Rotational_Speed","Engine_Health"
# Sample columns for analysis
columns_needed = ["Temperature", "Pressure", "Rotational_Speed","Engine_Health"]
plt.figure(figsize=(15, 10))

for i, column in enumerate(columns_needed , 1):
    plt.subplot(2, 2, i)  
    sns.lineplot(x=Aircraft_engine['Timestamp'], y=Aircraft_engine[column])  
    plt.title(f"{column} Over Time")  
    plt.xlabel("Timestamp")  
    plt.ylabel(column) 

plt.tight_layout()

plt.show()


# ### Feature Engineering:

# #### Create a Time-Related Feature:
# #### Let's extract the hour of the day as a new feature.
# ##### Time-Related Feature (Hour_of_Day): Extracting the hour of the day allows the model to capture potential patterns related to specific times.

# In[23]:


Aircraft_engine = Aircraft_engine.copy()

Aircraft_engine['Timestamp'] = pd.to_datetime(Aircraft_engine['Timestamp'], errors='coerce')

Aircraft_engine = Aircraft_engine.dropna(subset=['Timestamp'])
Aircraft_engine['Hour_of_Day'] = Aircraft_engine['Timestamp'].dt.hour

#print(Aircraft_engine.dtypes)

print(Aircraft_engine.head())


# #### Create Rolling Averages:
# #### Rolling averages can capture trends and patterns over time.
# ##### Rolling Averages: Calculating rolling averages helps smooth out noise and capture trends over time, especially relevant for time-series data.

# In[24]:


# Feature engineering - Create rolling averages for 'Temperature', 'Rotational_Speed' and 'Engine_Health'
Aircraft_engine['Rolling_Avg_Temperature'] = Aircraft_engine.groupby('Engine_ID')['Temperature'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
Aircraft_engine['Rolling_Avg_Rotational_Speed'] = Aircraft_engine.groupby('Engine_ID')['Rotational_Speed'].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
Aircraft_engine['Rolling_Avg_Engine_Health'] = Aircraft_engine.groupby('Engine_ID')['Engine_Health'].transform(lambda x: x.rolling(window=10).mean())

# Display the dataset with the new features
Aircraft_engine.head()


# #### Binning 'Hour_of_Day':
# #### Binning can convert a continuous feature into categorical bins.
# ##### Binning 'Hour_of_Day': Grouping hours into categories ('Night', 'Morning', 'Afternoon', 'Evening') may help the model recognize patterns related to different parts of the day.
# 

# In[25]:


# Feature engineering - Binning 'Hour_of_Day'
bins = [-1, 6, 12, 18, 24]
labels = ['Night', 'Morning', 'Afternoon', 'Evening']
Aircraft_engine['Day_Part'] = pd.cut(Aircraft_engine['Hour_of_Day'], bins=bins, labels=labels, right=False)

# Display the dataset with the new feature
Aircraft_engine.head()


# #### Interaction Features:
# #### Create interaction features to capture relationships between existing features.
# ##### Interaction Feature: The product of 'Temperature' and 'Rotational_Speed' creates a new feature that captures the interaction between these two variables.
# 

# In[26]:


# Feature engineering - Interaction feature between 'Temperature' and 'Rotational_Speed'
Aircraft_engine['Temp_Rotational_Interaction'] = Aircraft_engine['Temperature'] * Aircraft_engine['Rotational_Speed']

# Display the dataset with the new feature
Aircraft_engine.head()


# ### Visualization

# In[27]:


# Set the plotting style
sns.set(style="whitegrid")

# Bar Chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Day_Part', y='Engine_Health', data=Aircraft_engine, ci=None)
plt.title('Bar Chart: Engine Health Across Day Parts')
plt.xlabel('Day Part')
plt.ylabel('Engine Health')
plt.show()


# In[28]:


# Box Plot
plt.figure(figsize=(10, 6))
sns.boxplot(x='Day_Part', y='Engine_Health', data=Aircraft_engine)
plt.title('Box Plot: Engine Health Across Day Parts')
plt.xlabel('Day Part')
plt.ylabel('Engine Health')
plt.show()


# In[29]:


# Violin Plot
plt.figure(figsize=(10, 6))
sns.violinplot(x='Day_Part', y='Engine_Health', data=Aircraft_engine)
plt.title('Violin Plot: Engine Health Across Day Parts')
plt.xlabel('Day Part')
plt.ylabel('Engine Health')
plt.show()


# In[30]:


# Histogram
plt.figure(figsize=(10, 6))
sns.histplot(x='Engine_Health', hue='Day_Part', data=Aircraft_engine, element="step", stat="density", common_norm=False)
plt.title('Histogram: Engine Health Across Day Parts')
plt.xlabel('Engine Health')
plt.ylabel('Density')
plt.show()


# In[31]:


# Line Chart
plt.figure(figsize=(10, 6))
sns.lineplot(x='Day_Part', y='Engine_Health', data=Aircraft_engine, ci=None)
plt.title('Line Chart: Engine Health Trends Across DayAircraft_engine Parts')
plt.xlabel('Day Part')
plt.ylabel('Engine Health')
plt.show()


# In[33]:


# Grouped Bar Chart
Aircraft_engine['Engine_Failure'] = Aircraft_engine['Engine_Failure'].astype(str)
Aircraft_engine['Day_Part'] = Aircraft_engine['Day_Part'].astype(str)


plt.figure(figsize=(10, 6))
sns.barplot(x='Day_Part', y='Engine_Health', data=Aircraft_engine, ci=None, hue='Engine_Failure')


plt.title('Grouped Bar Chart: Engine Health Across Day Parts with Engine_Failure')
plt.xlabel('Day Part')
plt.ylabel('Engine Health')
plt.legend(title='Engine_Failure', loc='upper right', bbox_to_anchor=(1.2, 1))
plt.show()


# In[34]:


# Summary of Engine Failure
engine_failure_summary = Aircraft_engine["Engine_Failure"].value_counts()
print("Summary of Engine Failure:")
engine_failure_summary


# In[ ]:




