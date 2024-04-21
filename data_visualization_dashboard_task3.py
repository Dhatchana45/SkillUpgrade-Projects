# -*- coding: utf-8 -*-
"""Data Visualization Dashboard-Task3

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19ILD34PaOOeRcdT-zPP15IRqTN5_iU8G
"""

import dash
import numpy as np
from dash import dcc, html
import plotly.express as px
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_curve, roc_auc_score, confusion_matrix

# Load Iris dataset
df = pd.read_csv('/content/iris_flo.data.csv')
numeric_columns = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_columns].corr()

# Load Heart Disease dataset (replace with your dataset loading code)
heart_disease_df = pd.read_csv("/content/Heart Attack.csv")

# Preprocessing and modeling (replace with your actual preprocessing and modeling code)
x = heart_disease_df.drop(columns=['class'])
y = heart_disease_df['class'].apply(lambda x: 1 if x == 'positive' else 0)

df['petal_sepal_lratio'] = df['petal length'] / df['sepal length']
print(df[['petal_sepal_lratio']])
df['petal_sepal_wratio']= df['petal width'] / df['sepal width']
print(df[['petal_sepal_wratio']])


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
clf = DecisionTreeClassifier(random_state=42)
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Create the Dash app
app = dash.Dash(__name__)

# Scatter plot for petal_sepal_lratio and petal_sepal_wratio
scatter_plot_1 = px.scatter(df, x='petal_sepal_lratio', y='Species', color='Species', title='Petal/Sepal Length Ratio by Species', template='plotly_white')
scatter_plot_2 = px.scatter(df, x='petal_sepal_wratio', y='Species', color='Species', title='Petal/Sepal Width Ratio by Species', template='plotly_white')

# Violin plots
violin_plot_petal_width = px.violin(df, x='Species', y='petal width', title='Distribution of Petal Width by Species', template='plotly_white')
violin_plot_petal_length = px.violin(df, x='Species', y='petal length', title='Distribution of Petal Length by Species', template='plotly_white')
violin_plot_sepal_width = px.violin(df, x='Species', y='sepal width', title='Distribution of Sepal Width by Species', template='plotly_white')
violin_plot_sepal_length = px.violin(df, x='Species', y='sepal length', title='Distribution of Sepal Length by Species', template='plotly_white')

# Histogram of Sepal Length by Species
histogram_sepal_length = px.histogram(df, x='sepal length', color='Species', title='Histogram of Sepal Length by Species', template='plotly_white')

# Pie chart for species distribution
species_counts = df['Species'].value_counts()
pie_chart_species_distribution = px.pie(names=species_counts.index, values=species_counts.values, title='Distribution of Species', template='plotly_white')

# Correlation heatmap
corr_heatmap = px.imshow(corr_matrix, title='Correlation Matrix - Iris Dataset', template='plotly_white')

# Define layout
app.layout = html.Div([
    html.H1("Interactive Data Visualization Dashboard"),

    # Iris dataset section
    html.Div([
        html.H2("Exploratory Data Analysis (EDA) - Iris Dataset"),
        dcc.Graph(id='scatter_plot_1', figure=scatter_plot_1),
        dcc.Graph(id='scatter_plot_2', figure=scatter_plot_2),
        dcc.Graph(id='violin_plot_petal_width', figure=violin_plot_petal_width),
        dcc.Graph(id='violin_plot_petal_length', figure=violin_plot_petal_length),
        dcc.Graph(id='violin_plot_sepal_width', figure=violin_plot_sepal_width),
        dcc.Graph(id='violin_plot_sepal_length', figure=violin_plot_sepal_length),
        dcc.Graph(id='histogram_sepal_length', figure=histogram_sepal_length),
        dcc.Graph(id='pie_chart_species_distribution', figure=pie_chart_species_distribution),
        dcc.Graph(id='corr_heatmap', figure=corr_heatmap)
    ]),

    # Heart Disease dataset section
    html.Div([
        html.H2("Predictive Modeling Results - Heart Disease Dataset"),
        html.Div([
            html.P(f"Accuracy: {accuracy:.2f}"),
            html.P(f"Precision: {precision:.2f}"),
            html.P(f"Recall: {recall:.2f}")
        ]),
        dcc.Graph(
            id='heart-disease-roc-curve',
            figure=px.line(x=fpr, y=tpr, title='ROC Curve - Heart Disease Dataset', template='plotly_white')
        ),
        dcc.Graph(
            id='heart-disease-confusion-matrix',
            figure=px.imshow(conf_matrix, labels={'0': 'No Disease', '1': 'Disease'}, title='Confusion Matrix - Heart Disease Dataset', template='plotly_white')
        ),
        dcc.Graph(
            id='heart-disease-class-counts-bar-chart',
            figure=px.bar(heart_disease_df['class'].value_counts(), x=heart_disease_df['class'].value_counts().index, y=heart_disease_df['class'].value_counts().values, labels={'x': 'Class', 'y': 'Counts'}, title='Counts of Each Class in Heart Disease Dataset', template='plotly_white')
        )
    ]),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

print(df.columns)