# -*- coding: utf-8 -*-
"""PTDL-Credit risk

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eKbH8Yaz_fIhKHsiBuaow4MVoDXZicUP
"""

#Liêu Hoài Phúc K224141735 (Nhóm trưởng)
#Trần Đức Duy K224141717
#Phạm Hữu Khương K224141725
#Nguyễn Nhật Nam K224141728
#Nguyễn Quang Duy K224141716

#1. Import Libraries & Read data

import pandas as pd
import numpy as np
import warnings

# Ignoring warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split, cross_val_predict, KFold
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression


url = 'https://drive.google.com/file/d/1b9DbTBcm8NX95vHu_dJ4k-MlIbhlf53I/view?usp=sharing'
url = 'https://drive.google.com/uc?id=' + url.split('/')[-2]
data = pd.read_csv(url)
data

#2. Explore Data

#2.1 Overview

data.head()

data.tail()

data.describe()

data.info()

data.nunique()

num_data=data.drop(['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file'], axis=1)
num_data.corr()

import seaborn as sns
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
fig.set_size_inches(15,8)
sns.heatmap( num_data.corr(), vmax =.8, square = True, annot = True,cmap='Blues' )
plt.title('Correlation Matrix',fontsize=15);

#2.2 Detail

min_ = data['person_age'].min()
max_ = data['person_age'].max()
print(f"maximum Age {max_}")
print(f"minimum Age {min_}")

# people with an age between x and y
def age_group(arr):
    lenarr = len(arr)
    for i in range(0,lenarr-1):
        next = arr[i]+1
        num_people = data['person_age'].between(next,arr[i+1]).sum()
        print(f'Age between {next} and {arr[i+1]}: Number of people {num_people}')

age_group([0 ,18, 26, 36, 46, 56, 66])

def age_group(data, bounds):
    counts = []
    age_ranges = []
    len_bounds = len(bounds)
    for i in range(len_bounds - 1):
        next_age = bounds[i] + 1
        count = data['person_age'].between(next_age, bounds[i+1]).sum()
        age_ranges.append(f"{next_age}-{bounds[i+1]}")
        counts.append(count)
    return age_ranges, counts

age_bounds = [0, 18, 26, 36, 46, 56, 66]

age_ranges, counts = age_group(data, age_bounds)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(age_ranges, counts, color='skyblue')
plt.xlabel('Age Ranges')
plt.ylabel('Number of People')
plt.title('Person_age')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

max_ = data['person_income'].max()
min_ = data['person_income'].min()

print(f"maximum Income {max_}")
print(f"minimum Income {min_}")

#people with an income between x and y
def income_group(arr):
    lenarr = len(arr)
    for i in range(0,lenarr-1):
        next = arr[i]+1
        num_people = data['person_income'].between(next,arr[i+1]).sum()
        print(f'Income between {next} and {arr[i+1]}: Number of people {num_people}')

income_group([0, 25000, 50000, 75000, 100000, 6000000])

def income_group(data, ranges):
    counts = []
    income_ranges = []
    len_ranges = len(ranges)
    for i in range(len_ranges - 1):
        next_income = ranges[i] + 1
        count = data['person_income'].between(next_income, ranges[i+1]).sum()
        income_ranges.append(f"${next_income}-{ranges[i+1]}")
        counts.append(count)
    return income_ranges, counts

# Define income bounds
income_bounds = [0, 25000, 50000, 75000, 100000, 6000000]

# Extract data
income_ranges, counts = income_group(data, income_bounds)

# Plotting
plt.figure(figsize=(12, 8))
plt.bar(income_ranges, counts, color='lightgreen')
plt.xlabel('Income Ranges')
plt.ylabel('Number of People')
plt.title('Income')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

import plotly.express as px

# Calculate the counts for the 'person_home_ownership' column
home_ownership_distribution = data['person_home_ownership'].value_counts()

# Create a pie chart with Plotly Express
fig = px.pie(
    values=home_ownership_distribution.values,
    names=home_ownership_distribution.index,
    color_discrete_sequence=px.colors.sequential.Mint,
    title='Home Ownership Distribution'
)

# Add labels with percentage and value, and set font size
fig.update_traces(
    textinfo='label+percent+value',
    textfont=dict(size=15),
    marker=dict(line=dict(color='black', width=2))
)

# Display the pie chart
fig.show()

max_loan_amount = data['loan_amnt'].max()
min_loan_amount = data['loan_amnt'].min()

print(f"maximum Loan Amount {max_loan_amount}")
print(f"minimum Loan Amount {min_loan_amount}")

# people with an income between x and y
def loan_amount_group(arr):
    lenarr = len(arr)
    for i in range(0,lenarr-1):
        next = arr[i]+1
        num_people = data['loan_amnt'].between(next,arr[i+1]).sum()
        print(f'Loan Amount between {next} and {arr[i+1]}: Number of people {num_people}')

loan_amount_group([0, 5000, 10000, 15000, 35000])

def loan_amount_group(data, ranges):
    counts = []
    loan_ranges = []
    len_ranges = len(ranges)
    for i in range(len_ranges - 1):
        next_loan = ranges[i] + 1
        count = data['loan_amnt'].between(next_loan, ranges[i+1]).sum()
        loan_ranges.append(f"${next_loan}-{ranges[i+1]}")
        counts.append(count)
    return loan_ranges, counts

# Define loan amount bounds
loan_bounds = [0, 5000, 10000, 15000, 35000]

# Extract data
loan_ranges, counts = loan_amount_group(data, loan_bounds)

# Plotting
plt.figure(figsize=(10, 6))
plt.bar(loan_ranges, counts, color='royalblue')
plt.xlabel('Loan Amount Ranges')
plt.ylabel('Number of Loans')
plt.title('Loan_amount')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

fig=px.histogram(data, x = 'loan_intent',histnorm = 'percent', text_auto = '.2f',template = 'presentation', title = 'Loan intent',color_discrete_sequence=px.colors.sequential.Mint)
fig.update_layout()
fig.show()

fig=px.histogram(data, x = 'cb_person_cred_hist_length', text_auto = '.2f',template = 'presentation', title = 'Credit history length',color_discrete_sequence=px.colors.sequential.Mint)
fig.update_layout()
fig.show()

level_counts=data.loan_grade.value_counts()
fig=px.pie(values=level_counts.values,
          names=level_counts.index,
          color_discrete_sequence=px.colors.sequential.Mint,
          title= 'loan_grade'
          )
fig.update_traces(textinfo='label+percent+value', textfont_size=13,
                  marker=dict(line=dict(color='#102000', width=0.2)))

fig.data[0].marker.line.width = 2
fig.data[0].marker.line.color='gray'
fig.show()

# Create loan-to-income ratio
data['loan_to_income_ratio'] = data['loan_amnt'] / data['person_income']

# Create loan-to-employment length ratio
data['loan_to_emp_length_ratio'] =  data['person_emp_length']/ data['loan_amnt']

# Create interest rate-to-loan amount ratio
data['int_rate_to_loan_amt_ratio'] = data['loan_int_rate'] / data['loan_amnt']
data

#3 dealing with the messing data

#3.1 NaN/Null ( drop )

data.isnull().sum()

original_count = data.shape[0]

data_clean = data.dropna(axis=0)

clean_count = data_clean.shape[0]

dropped_count = original_count - clean_count

print('Số lượng dòng đã xóa là: ', dropped_count)
data.dropna(axis=0,inplace=True)
data.isnull().sum()

#3.2 Outliers

plt.figure(figsize=(12, 6))
sns.boxplot(data, orient='h')  # Horizontal box plot for all columns
plt.title(' Showing Outliers in Each Column')
plt.show()

from sklearn.ensemble import IsolationForest

# Khởi tạo mô hình Isolation Forest
iso = IsolationForest(n_estimators=100, contamination='auto', random_state=42)

# Huấn luyện mô hình trên dữ liệu
iso.fit(data[['person_income']])

# Dự đoán: -1 cho ngoại lai, 1 cho dữ liệu bình thường
outliers = iso.predict(data[['person_income']])

# Thêm kết quả vào DataFrame
data['outlier'] = outliers

# Lọc để loại bỏ các ngoại lai
filtered_data = data[data['outlier'] == 1]

# In số lượng dữ liệu sau khi lọc và trước khi lọc
print(f"Số dữ liệu ban đầu: {len(data)}")
print(f"Số dữ liệu sau khi lọc: {len(filtered_data)}")
data = filtered_data

import seaborn as sns
import matplotlib.pyplot as plt

# Assuming df is your DataFrame
# Select the column 'person_income' for the box plot
column_name = 'person_income'

# Create a box plot of the 'person_income' column
plt.figure(figsize=(8, 6))
sns.boxplot(x=filtered_data[column_name])

# Set the title and labels
plt.title(f'Box Plot of {column_name}')
plt.xlabel(column_name)
plt.show()

from sklearn.ensemble import IsolationForest

# Khởi tạo mô hình Isolation Forest
iso = IsolationForest(n_estimators=100, contamination='auto', random_state=42)

# Huấn luyện mô hình trên dữ liệu
iso.fit(data[['person_age']])

# Dự đoán: -1 cho ngoại lai, 1 cho dữ liệu bình thường
outliers = iso.predict(data[['person_age']])

# Thêm kết quả vào DataFrame
data['outlier'] = outliers

# Lọc để loại bỏ các ngoại lai
filtered_data = data[data['outlier'] == 1]

# In số lượng dữ liệu sau khi lọc và trước khi lọc
print(f"Số dữ liệu ban đầu: {len(data)}")
print(f"Số dữ liệu sau khi lọc: {len(filtered_data)}")
data=filtered_data

column_name = 'person_age'

# Create a box plot of the 'person_income' column
plt.figure(figsize=(8, 6))
sns.boxplot(x=filtered_data[column_name])

# Set the title and labels
plt.title(f'Box Plot of {column_name}')
plt.xlabel(column_name)
plt.show()

#4 encode + model

import pandas as pd
from sklearn.preprocessing import LabelEncoder
X = data.drop('loan_grade', axis=1)
y = data['loan_grade'].values.reshape(-1,1)
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=12)

print(x_train.shape,x_test.shape)
print(y_train.shape,y_test.shape)

x_train.reset_index(inplace = True)
x_test.reset_index(inplace = True)

x_train.columns

import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# Dữ liệu dạng một chiều
loan_intent = ['DEBTCONSOLIDATION', 'EDUCATION', 'HOMEIMPROVEMENT', 'PERSONAL', 'VENTURE']

# Chuyển đổi sang DataFrame hoặc mảng 2D
loan_intent_reshaped = pd.Series(loan_intent).values.reshape(-1, 1)

# Tạo bộ mã hóa OneHotEncoder
ohe = OneHotEncoder()

# Thực hiện "fit" với mảng hai chiều
ohe.fit(loan_intent_reshaped)

data.columns

from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler, LabelEncoder

# Các danh sách cột cần chuẩn hóa
normal_col = ['person_income', 'person_age', 'person_emp_length', 'loan_amnt', 'loan_int_rate', 'cb_person_cred_hist_length', 'loan_percent_income', 'loan_to_emp_length_ratio', 'int_rate_to_loan_amt_ratio']
label_col = ['person_home_ownership', 'loan_intent','cb_person_default_on_file']

# DataFrame có thể là dữ liệu tập huấn luyện và tập kiểm tra
X_scaled = x_train
X_scaled_test = x_test

# Khởi tạo các scaler
scaler_uniform = MinMaxScaler()  # Dành cho các cột có phân phối đồng đều
scaler_normal = StandardScaler()  # Dành cho các cột có phân phối gần phân phối chuẩn
scaler_bimodal = RobustScaler()  # Dành cho các cột có phân phối hai đỉnh
scaler_label = LabelEncoder()  # Dành cho các cột danh mục

# Kiểm tra và áp dụng chuẩn hóa chỉ cho các cột có sẵn
existing_normal_cols = [col for col in normal_col if col in X_scaled.columns]  # Chỉ lấy các cột có sẵn
existing_label_cols = [col for col in label_col if col in X_scaled.columns]  # Chỉ lấy các cột có sẵn

X_scaled.loc[:, existing_normal_cols] = scaler_normal.fit_transform(X_scaled.loc[:, existing_normal_cols])
X_scaled_test.loc[:, existing_normal_cols] = scaler_normal.transform(X_scaled_test.loc[:, existing_normal_cols])

# Áp dụng Label Encoding cho các cột có sẵn
for col in existing_label_cols:
    scaler_label.fit(X_scaled.loc[:, [col]])  # Fit Label Encoder với dữ liệu huấn luyện
    X_scaled.loc[:, col] = scaler_label.transform(X_scaled.loc[:, [col]])  # Mã hóa dữ liệu huấn luyện
    X_scaled_test.loc[:, col] = scaler_label.transform(X_scaled_test.loc[:, [col]])  # Mã hóa dữ liệu kiểm tra

data1 = pd.concat([X_scaled,  X_scaled_test], ignore_index=True)

X = data1

X_scaled

from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Khởi tạo LabelEncoder
label_encoder = LabelEncoder()

# Áp dụng Label Encoding cho cột
data['loan_grade'] = label_encoder.fit_transform(data['loan_grade'])
y = data['loan_grade']

y

# các giá trị cúa y
y = pd.to_numeric(y, errors='coerce')
unique_labels = y.unique()
print(unique_labels)

# kiểm tra có mất cân bằng không
import pandas as pd
target_counts = data['loan_grade'].value_counts()
print("Số lượng mẫu trong mỗi lớp:")
print(target_counts)

# Kiểm tra hình dạng của DataFrame
print("Hình dạng của DataFrame trước khi áp dụng SMOTE:")
print(X.shape)  # X là DataFrame trước khi áp dụng SMOTE

# Kiểm tra các cột trong DataFrame
print("Các cột trong DataFrame:")
print(X.columns)  # X là DataFrame trước khi áp dụng SMOTE

from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
# Khởi tạo SMOTE
smote = SMOTE(random_state=42)

# Cân bằng lớp của X và y

# Áp dụng SMOTE sau khi điền giá trị bị thiếu
X_balanced, y_balanced = smote.fit_resample(X, y)

y = y_balanced
X = X_balanced
import pandas as pd

# Hiển thị số lượng các lớp sau khi cân bằng
class_counts = pd.Series(y_balanced).value_counts()
print("Số lượng lớp 0 sau khi cân bằng:", class_counts[0])
print("Số lượng lớp 1 sau khi cân bằng:", class_counts[1])
print("Số lượng lớp 2 sau khi cân bằng:", class_counts[2])
print("Số lượng lớp 3 sau khi cân bằng:", class_counts[3])
print("Số lượng lớp 4 sau khi cân bằng:", class_counts[4])
print("Số lượng lớp 5 sau khi cân bằng:", class_counts[5])
print("Số lượng lớp 6 sau khi cân bằng:", class_counts[6])

y

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier

# Function to perform frequency encoding
def frequency_encoding(df, column):
    frequency_map = df[column].value_counts(normalize=True)
    df[column + '_freq_encoded'] = df[column].map(frequency_map)
    return df

X

y

from sklearn.preprocessing import StandardScaler

# Khởi tạo StandardScaler
scaler = StandardScaler()

# Chuẩn hóa dữ liệu cho X_balanced (hoặc bất kỳ ma trận nào bạn muốn chuẩn hóa)
X_balanced_scaled = scaler.fit_transform(X)
X = X_balanced_scaled
X

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
# Function to perform frequency encoding
def frequency_encoding(data, column):
    frequency_map = data[column].value_counts(normalize=True)
    data[column + '_freq_encoded'] = data[column].map(frequency_map)
    return data

instances_to_predict = pd.DataFrame({
    'person_age': [15],
    'person_income': [1000],
    'person_home_ownership': ['RENT'],
    'person_emp_length': [8],
    'loan_intent': ['HOMEIMPROVEMENT'],
    'loan_amnt': [5500],
    'loan_int_rate': [12.87],
    'loan_status': [0],
    'loan_percent_income': [0.46],
    'cb_person_default_on_file': ['N'],
    'cb_person_cred_hist_length': [10]
})
# Columns to be frequency encoded
columns_to_encode = ['person_age', 'person_income', 'person_home_ownership',
       'person_emp_length', 'loan_intent', 'loan_amnt', 'loan_int_rate',
       'loan_status', 'loan_percent_income', 'cb_person_default_on_file',
       'cb_person_cred_hist_length',]

# Perform frequency encoding for each column
for column in columns_to_encode:
    instances_to_predict = frequency_encoding(instances_to_predict, column)

# Drop the original categorical columns
instances_to_predict.drop(columns=columns_to_encode, inplace=True)

# Standardize the features
scaler = StandardScaler()
instances_to_predict_scaled = scaler.fit_transform(instances_to_predict)

# Simulated training data and labels
# Replace these with your actual training data and labels
X_train = np.random.rand(10, instances_to_predict_scaled.shape[1])
y_train = np.random.randint(0, 2, 10)  # Random binary labels

# Train the AdaBoostClassifier model
gb_model1 = AdaBoostClassifier()
gb_model1.fit(X_train, y_train)
gb_model2 = DecisionTreeClassifier()
gb_model2.fit(X_train, y_train)
# Predict Trust Level
predictions1 = gb_model1.predict(instances_to_predict_scaled)
predictions2 = gb_model2.predict(instances_to_predict_scaled)

# Print the predictions
print("Case 1: Predicted Loan grade is", predictions1)
print("Case 2: Predicted Loan grade is", predictions2)

import pickle

model_path = 'https://colab.research.google.com/drive/1eKbH8Yaz_fIhKHsiBuaow4MVoDXZicUP?usp=sharing'
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

model_path = 'model_path = '/content/drive/My Drive/model.pkl'
with open(model_path, 'rb') as file:
    loaded_model = pickle.load(file)

# Sử dụng mô hình để dự đoán
predictions = loaded_model.predict(X_test)
print(predictions)
'
with open(model_path, 'rb') as file:
    loaded_model = pickle.load(file)

# Sử dụng mô hình để dự đoán
predictions = loaded_model.predict(X_test)
print(predictions)