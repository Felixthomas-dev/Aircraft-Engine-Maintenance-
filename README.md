## Aircraft Engine Maintenance Analysis

### Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Overview](#dataset-overview)
3. [Exploratory Data Analysis](#exploratory-data-analysis)
   1. [Data Cleaning](#data-cleaning)
   2. [Handling Missing Values](#handling-missing-values)
   3. [Handling Outliers](#handling-outliers)
   4. [Univariate Analysis](#univariate-analysis)
   5. [Bivariate Analysis](#bivariate-analysis)
   6. [Multivariate Analysis](#multivariate-analysis)
4. [Feature Engineering](#feature-engineering)
5. [Data Visualization](#data-visualization)
6. [Insights for Predictive Maintenance Model](#insights-for-predictive-maintenance-model)
7. [Contributions](#contributions)
8. [License](#license)

---

### Project Overview
This project involves a comprehensive analysis of a dataset representing aircraft engine health and operational parameters. The objective is to conduct exploratory data analysis (EDA), handle missing values, identify outliers, perform univariate, bivariate, and multivariate analysis, and implement feature engineering techniques to understand the data and inform predictive maintenance.

---

### Dataset Overview
The dataset contains records for aircraft engines at various points in time. Key attributes include temperature, pressure, rotational speed, engine health, and a binary indicator of engine failure.

**Data Dictionary:**
- `Engine_ID`: Unique identifier for each aircraft engine (Integer)
- `Timestamp`: Date and time when the data was recorded (Datetime)
- `Temperature`: Temperature in degrees Celsius (Float)
- `Pressure`: Pressure in units relevant to the dataset (Float)
- `Rotational_Speed`: Rotational speed in revolutions per minute (Float)
- `Engine_Health`: Overall health of the aircraft engine (Float, ranging from 0 to 1)
- `Engine_Failure`: Binary indicator of engine failure (Integer: 0 - No engine failure, 1 - Engine failure)

---

### Exploratory Data Analysis

--

#### Data Cleaning
- The dataset was cleaned to ensure data consistency and integrity. Initial data checks were conducted to understand the shape and summary statistics of the dataset.

#### Handling Missing Values
- To handle missing values, the median was used for imputation. The following steps were taken to identify and visualize missing data:

#### Visualize Missing Values
- **Bar plot with `missingno`**: To visualize columns with missing data.
- **Heatmap with `seaborn`**: To illustrate missing patterns.

#### Handle Missing Values
- Imputed Temperature and Pressure with the median.
- Validated that missing values were appropriately addressed.

#### Handling Outliers
Outliers were identified and removed using the Interquartile Range (IQR) method:

#### Calculate IQR
- **IQR = Q3 - Q1** for numerical columns.

#### Identify Outliers
- Outliers were those data points falling outside 1.5 times the IQR from Q1 and Q3.

#### Remove Outliers
- Rows with outliers were removed, resulting in a dataset with reduced noise.

#### Univariate Analysis
- To understand the distribution of key variables, univariate analysis was performed on `Temperature`, `Pressure`, `Rotational_Speed`, and `Engine_Health`. Histogram plots with KDE (Kernel Density Estimation) were used to visualize the distribution of these features.

#### Bivariate Analysis
- Bivariate analysis explored relationships between pairs of variables:

#### Pairplot
- **A pairplot with `seaborn`** to visualize relationships among features, colored by `Engine_Failure`.

#### Scatter Plots
- **Scatter plots** to identify any trends or correlations between key features.

#### Multivariate Analysis
- **Multivariate** analysis involved examining interactions among three or more variables:

#### Correlation Heatmap
- A heatmap to visualize correlations among `Temperature`, `Pressure`, `Rotational_Speed`, and `Engine_Health`.

#### Time Series Analysis
- A time-series line plot for `Engine_Health`, with lines representing individual `Engine_IDs`.

---

### Feature Engineering
Feature engineering was applied to enhance the predictive capabilities of the dataset:

--

#### Time-based Features
- Extracted the `Hour_of_Day` from the `Timestamp` to capture temporal patterns.

#### Rolling Averages
- Created rolling averages for `Temperature`, `Rotational_Speed`, and `Engine_Health` with a window of 10.

#### Binning
- Binned `Hour_of_Day` into `Night`, `Morning`, `Afternoon`, and `Evening` to categorize the day into parts.

#### Interaction Features
- Created an interaction feature by multiplying `Temperature` with `Rotational_Speed`.
---

### Data Visualization
Several types of visualizations were used to gain insights and communicate findings effectively:

--
- **Bar Charts:** Illustration of `Engine_Health` across different parts of the day.
- **Box Plots:** Demonstration of the spread of `Engine_Health` across `Day_Part`.
- **Violin Plots:** Visualization of the distribution of `Engine_Health` across `Day_Part`.
- **Histograms:** Display of the distribution of `Engine_Health`.
- **Line Charts:** Representation of trends in `Engine_Health` over time.
- **Grouped Bar Charts:** Visualization of `Engine_Health` across `Day_Part` with and without `Engine_Failure`.
---
### Insights for Predictive Maintenance Model
The exploratory data analysis provided several insights that could inform a predictive maintenance model:

--

- **Temporal Patterns:** The extraction of time-based features such as Hour_of_Day and subsequent binning into day parts can reveal potential times when engine health might decline.

- **Rolling Averages:** Rolling averages can smooth out short-term fluctuations and help identify longer-term trends, valuable for predicting maintenance needs.

- **Feature Interactions:** Interaction features like Temp_Rotational_Interaction suggest that a combination of factors might influence engine health, pointing to complex relationships for predictive models to consider.

- **Engine Failure Trends:** Analysis showed trends in engine health over time, indicating that predictive models might leverage this information to forecast future failures

---
### Contributions
Contributions are welcome! To contribute:
- **Create a new issue** with your suggestion.
- **Submit a pull request** with your proposed changes.

---

### License
This project is open source and available under the [MIT License](LICENSE), promoting free use, modification, and distribution of the software, ensuring that contributions are welcomed and recognized.









