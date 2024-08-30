import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import textwrap
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")
# Custom styles for each section

st.markdown(
    """
    <style>
    /* Set the background color */
    .stApp {
        background-color: #f5f5f5;
    }

    /* Add red outline around the multiselect and selectbox components */
    .stMultiSelect > div, .stSelectbox > div {
        border: 2px solid black;  /* Add a red outline */
        border-radius: 5px;
        padding: 5px;
        background-color: #f5f5f5;  /* Optional: set the background inside the input */
    }



    /* Style the labels of the multiselect and selectbox components */
        div[class^='stMultiSelect'] label, div[class^='stSelectbox'] label {
            font-size: 18px;  /* Increase font size */
            font-weight: bold;  /* Make the text bold */
            color: black;  /* Optional: set label color to black */
        }



     /* Custom title style */
    .custom-title {
        font-size: 36px;  /* Increase font size */
        font-weight: bold;
        color: black;
        text-align: center;  /* Center-align the title */
        margin-bottom: 20px;  /* Add space below the title */
    }
   /* Larger text for intro section */
    .intro-text {
        font-size: 19px;  /* Increase font size */
        line-height: 1.6;  /* Increase line height for better readability */
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="custom-title">🎓  Degrees of Distinction: Visualizing the Data of Academic Majors 🎓</div>', unsafe_allow_html=True)

# Set the title of the page
# st.title("Degrees of Distinction: Visualizing the Data of Academic Majors")

st.markdown("""
    <div class="intro-text">
    <strong>Here you can explore the world of academic majors. Our interactive dashboard allows you to navigate through various major categories and take a deep dive into specific majors within each category. Explore the gender composition of each degree, and gain insights into the average salaries earned by graduates, as well as the types of jobs they pursue.</strong>
    <br>
    <strong>Whether you're a student, educator, or simply curious about different fields of study, our platform provides the data-driven insights you need to make informed decisions.</strong><br>
    <br><strong>Tips and Tricks for a better experience:</strong>
    <ul>
        <li><strong>Hover Over Data:</strong> Move your mouse over any bar or segment to see precise information about gender distribution, job counts, or salaries.</li>
        <li><strong>Zoom In:</strong> Click and drag to zoom into any section of the graph for a closer look at specific data points.</li>
        <li><strong>Reset View:</strong> Double-click the graph to return to the original zoom level and view.</li>
        <li><strong>Use the Slider:</strong> When drilling down into specific categories, use the slider to scroll through different majors within the selected category, allowing for easy exploration of detailed data.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid #ddd;'>", unsafe_allow_html=True)

### FIRST VISU ####

# Load the data
data = pd.read_csv(r'/Users/rubenchocron/Documents/Data Science BSC/year3/recent-grads (1).csv')

st.markdown("""
    <div style="font-size:30px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">
    Section 1: Understanding Gender Dynamics Across Academic Majors
    </div>
""", unsafe_allow_html=True)

# Descriptive Text
st.markdown("""
    <div class="intro-text">
    In this section, you can explore the gender distribution within various academic majors, revealing trends and insights into the representation of men and women across different fields of study. Use these visualizations to compare the gender makeup of each major and uncover patterns that may influence educational and career choices.
    </div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

selected_majors = st.multiselect('Select Major Categories', options=sorted(data['Major_category'].unique()), default=sorted(data['Major_category'].unique())[:5], max_selections=8, key = 'majors_category')

# Filter data based on selected majors
filtered_data = data[data['Major_category'].isin(selected_majors)]

# Calculate the total number of men and women for each selected major
gender_data = filtered_data.groupby('Major_category').agg({
    'Men': 'sum',
    'Women': 'sum'
}).reset_index()

# Calculate the percentage of men and women in each major
gender_data['Total'] = gender_data['Men'] + gender_data['Women']
gender_data['Male_Percentage'] = gender_data['Men'] / gender_data['Total']
gender_data['Female_Percentage'] = gender_data['Women'] / gender_data['Total']
col1, col2 = st.columns([1, 1])  # Equal width columns

# Add "None" option to the selectbox for drill-down
select_options = ['None'] + gender_data['Major_category'].tolist()
selected_category = col2.selectbox('Select a Major Category to Drill Down', select_options)

# Adjust opacity for the original graph
opacity_values = [1.0] * len(gender_data)  # Default to full opacity for all bars
if selected_category and selected_category != 'None':
    opacity_values = [1.0 if cat == selected_category else 0.2 for cat in gender_data['Major_category']]


# Create the normalized stacked bar chart
fig = go.Figure()

# Function to set text color with adjusted opacity
def get_text_color(opacity):
    return f'rgba(0, 0, 0, {opacity})'


# Bar for Male Percentage
fig.add_trace(go.Bar(
    x=gender_data['Major_category'],
    y=gender_data['Male_Percentage'],
    name='Male',
    marker=dict(color='#1f77b4', opacity=opacity_values),
    text=gender_data['Male_Percentage'].apply(lambda x: f'{x:.1%}'),
    textposition='auto',
    hovertemplate = 'Count: %{customdata}<extra></extra>',
    customdata = gender_data['Men'],
    hoverlabel=dict(namelength=0)

))

# Bar for Female Percentage
fig.add_trace(go.Bar(
    x=gender_data['Major_category'],
    y=gender_data['Female_Percentage'],
    name='Female',
    marker=dict(color='pink', opacity=opacity_values),
    text=gender_data['Female_Percentage'].apply(lambda x: f'{x:.1%}'),
    textposition='auto',
    hovertemplate='Count: %{customdata}<extra></extra>',
    customdata=gender_data['Women'],
    hoverlabel=dict(namelength=0)

))

# Center the title and legend in the main chart
fig.update_layout(
    title={
        'text': 'Gender Distribution by Major Category',
        'x': 0.5,  # Center the title
        'xanchor': 'center',
        'yanchor': 'top'
    },
    legend=dict(
        orientation="v",
        yanchor="middle",
        y=0.5,
        xanchor="right",
        x=1.15  # Center the legend
    ),
    xaxis_title='Major Category',
    yaxis_title='Percentage',
    yaxis=dict(range=[0, 1], tickformat=".0%"),
    barmode='stack'
)


# Display the chart
with col1:
    st.plotly_chart(fig, use_container_width=True)

# selected_category = col2.selectbox('Select a major category to drill down on:', gender_data['Major_category'])


with col2:    # If a category is selected, display the drill-down chart in the second column
    if selected_category and selected_category != 'None':
        # Filter data based on the selected Major_category
        major_filtered_data = data[data['Major_category'] == selected_category]

        # Aggregate the total number of men and women for each major in the selected category
        major_gender_data = major_filtered_data.groupby('Major').agg({
            'Men': 'sum',
            'Women': 'sum'
        }).reset_index()


        def wrap_and_truncate_label(label, width=15, max_lines=2):
            wrapped = textwrap.wrap(label, width)
            if len(wrapped) > max_lines:
                wrapped = wrapped[:max_lines]  # Limit to max_lines
                wrapped[-1] += "..."  # Add ellipsis to indicate truncation
            return "<br>".join(wrapped)

        # Calculate the percentage of men and women in each major
        major_gender_data['Total'] = major_gender_data['Men'] + major_gender_data['Women']
        major_gender_data['Male_Percentage'] = major_gender_data['Men'] / major_gender_data['Total']
        major_gender_data['Female_Percentage'] = major_gender_data['Women'] / major_gender_data['Total']
        major_gender_data['Short_Major'] = major_gender_data['Major'].apply(lambda x: wrap_and_truncate_label(x))




        # Create the drill-down bar chart
        drill_fig = go.Figure()

        # Bar for Male Percentage in the selected major category
        drill_fig.add_trace(go.Bar(
            x=major_gender_data['Short_Major'],
            y=major_gender_data['Male_Percentage'],
            name='Male',
            marker=dict(color='#1f77b4'),
            hovertemplate='%{customdata[1]}<br>Male: %{y:.1%}<br>Count: %{customdata[0]}<extra></extra>',
            customdata=list(zip(major_gender_data['Men'], major_gender_data['Major'])),
            hoverlabel=dict(namelength=0)
        ))

        # Bar for Female Percentage in the selected major category
        drill_fig.add_trace(go.Bar(
            x=major_gender_data['Short_Major'],
            y=major_gender_data['Female_Percentage'],
            name='Female',
            marker=dict(color='pink'),
            hovertemplate='%{customdata[1]}<br>Female: %{y:.1%}<br>Count: %{customdata[0]}<extra></extra>',
            customdata=list(zip(major_gender_data['Women'], major_gender_data['Major'])),
            hoverlabel=dict(namelength=0)
        ))

        # Update layout for the drill-down stacked bar chart
        drill_fig.update_layout(
            title={
                'text': f'Gender Distribution in {selected_category} majors',
                'x': 0.5,  # Center the title
                'xanchor': 'center',
                'yanchor': 'top'
            },
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="right",
                x=1.15  # Center the legend
            ),
            xaxis_title='Major',
            yaxis_title='Percentage',
            yaxis=dict(range=[0, 1], tickformat=".0%"),
            xaxis=dict(
                rangeslider=dict(
                    visible=True,
                    thickness=0.05,
                    bgcolor="#E0E0E0",  # Set background color to gray
                    borderwidth=0
                ),
                fixedrange=True,  # Allow zooming and scrolling
                range=[-0.5,  min(len(major_filtered_data['Major'].unique()), 7.5)],
                autorange=False,  # Disable auto-ranging to keep the range fixed

            ),
            barmode='stack',

        )

        # Display the drill-down chart in the second column
        st.plotly_chart(drill_fig, use_container_width=True)

### END OF FIRST VISU ####

st.markdown("<hr style='border: 0.5px solid #ddd;'>", unsafe_allow_html=True)

st.markdown("""
    <div style="font-size:30px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">
    Section 2: Understanding Salary Trends Across Academic Majors
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="intro-text">
    This interactive graph displays the median salaries for various academic majors, with an option to group by major category. The chart helps you compare the earning potential of different fields of study, highlighting the highest and lowest paying degrees.
    This tool is designed to help you make informed decisions by visualizing the financial prospects of different academic paths.
<br><br>
    <strong>How to Use the Graph:</strong>
    <ul>
        <li><strong>Sort Options:</strong> Use the radio buttons to sort the data by salary or major category, and switch between ascending and descending order.</li>
        <li><strong>Color Coding:</strong> Toggle the "Color Code by Major Category" checkbox to highlight majors based on their respective categories.</li>
        <li><strong>Hover for Details:</strong> Hover over the bars to see specific information, including the exact median salary and original category for grouped majors.</li>
    </ul>
    </div>
""", unsafe_allow_html=True)
######### SECOND VISU #######################

# Extract relevant columns for the chart
filtered_data = data[['Major', 'Median', 'Major_category']]

# Define the categories to keep based on size (top 7 by number of entries)
categories_to_keep = [
    'Engineering', 'Social Science', 'Physical Sciences',
    'Agriculture & Natural Resources', 'Business', 'Law & Public Policy', 'Computers & Mathematics'
]

# Group all other categories into 'Other'
filtered_data['Major_category_grouped'] = filtered_data['Major_category'].apply(
    lambda x: x if x in categories_to_keep else 'Other'
)

# Calculate the height of the chart to fit all rows (25 pixels per row)
chart_height = max(800, 25 * len(filtered_data)//10)
st.markdown(
    """
    <style>
    .stRadio > div {
        border: 2px solid #d3d3d3; /* Add border */
        padding: 10px; /* Add padding around radio buttons */
        border-radius: 5px; /* Rounded corners */
        background-color: #f5f5f5; /* Light background color */
        font-size: 18px; /* Larger font size for options */
    }

    .stCheckbox > div {
        border: 2px solid #d3d3d3; /* Add border */
        padding: 10px; /* Add padding around checkbox */
        border-radius: 5px; /* Rounded corners */
        background-color: #f5f5f5; /* Light background color */
        font-size: 18px; /* Larger font size for options */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Place the radio buttons below the legend
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)  # Add some space

# Create columns for the radio buttons to appear side by side
col1, col2, col3 = st.columns(3)

# Place the sorting field radio button in the first column
with col1:
    sort_field = st.radio(
        'Sort by:',
        options=['Salary', 'Salary and Major Category'],
        index=0  # Default to 'Salary'
    )

# Determine sorting order based on the first radio button
ascending = True  # Default sorting order

# Create a disabled version of the radio button when sorting by Major Category
with col2:
    # if sort_field == 'Salary':
        sort_order = st.radio(
            'Order by:',
            options=['Descending', 'Ascending'],
            index=1
        )
        ascending = True if sort_order == 'Ascending' else False
    # else:
    #     # st.markdown(
    #     #     """
    #     #     <style>
    #     #     .disabled-radio {
    #     #         color: grey;
    #     #         opacity: 0.5;
    #     #         pointer-events: none;
    #     #     }
    #     #     </style>
    #     #     """, unsafe_allow_html=True
    #     # )
    #     st.radio(
    #         'Order:',
    #         options=['Descending', 'Ascending'],
    #         index=1,  # Default to 'Descending'
    #         disabled=False,  # Disable the radio button
    #         key='disabled_radio'
    #     )
    #     ascending = True if sort_order == 'Ascending' else False


# Checkbox to enable or disable color coding by Major Category
with col3:
    st.markdown("<div style='height: 45px;'></div>", unsafe_allow_html=True)  # Add vertical space
    color_by_category = st.checkbox('Color Code by Major Category', value=True)  # Default to not checked

# Set the column for color coding based on the checkbox value
color_arg = 'Major_category_grouped' if color_by_category else None

# Sort the filtered data based on the user's selection
if sort_field == 'Salary':
    sorted_data = filtered_data.sort_values(by='Median', ascending=ascending)
else:
    sorted_data = filtered_data.sort_values(by=['Major_category_grouped','Median'], ascending=[True, ascending])

# Define the color mapping, including the grouped 'Other' category
color_discrete_map = {
    'Engineering': 'blue',
    'Business': 'red',
    'Law & Public Policy': 'orange',
    'Computers & Mathematics': 'purple',
    'Agriculture & Natural Resources': 'green',
    'Social Science': 'pink',
    'Physical Sciences': 'yellow',
    'Other': 'turquoise'  # Assign a color to the 'Other' category
}

# Recreate the horizontal bar chart with sorted data
fig = px.bar(
    sorted_data,
    x='Median',
    y='Major',
    color=color_arg,  # Conditionally apply color coding
    color_discrete_map=color_discrete_map if color_by_category else None,  # Use the fixed color mapping if applicable
    orientation='h',
    title='Median Salaries by Major',
    labels={'Median': 'Median Salary (per thousand dollars)', 'Major': 'Academic Major', 'Major_category_grouped': 'Major Category'},
    height=chart_height,
    custom_data=['Major_category'],  # Include the original category in custom data,

)

fig.update_traces(
    hovertemplate='<b>Major:</b> %{y}<br><b>Median Salary:</b> %{x}<br>' +
                  '<b>Major Category:</b> %{customdata[0]}<extra></extra>',
)

fig.update_layout(title={'text': 'Median Salaries by Major', 'x': 0.5, 'xanchor': 'center'},
                  legend=dict(
                      orientation='v',
                      yanchor='top',
                      y=1,
                      xanchor='left',
                      x=1.05,
                      font=dict(size=14),
                      traceorder='reversed',
                      title=dict(text='Major Categories', font=dict(size=16, color='black', family='Arial')),),

                  xaxis=dict(
                      showgrid=True,  # Show vertical grid lines
                      gridcolor='darkgray',  # Set the color of the grid lines
                      gridwidth=1,  # Set the width of the grid lines
                      range=[0, 115000]  # Limit the x-axis range to 0 to 100

                  ),
                  plot_bgcolor='white',  # Set the background color of the plot area

                  )  # Center the title


# Update layout to enforce sorting if sorted by Median (Salary)
if sort_field == 'Salary':
    fig.update_layout(
        yaxis=dict(categoryorder='total ascending' if ascending else 'total descending'),
    )
# Display the updated bar chart
st.plotly_chart(fig, use_container_width=True)

########## END OF SECOND VISU ##################


st.markdown("<hr style='border: 0.5px solid #ddd;'>", unsafe_allow_html=True)

########## THIRD VISU ##################


data = pd.read_csv(r'/Users/rubenchocron/Documents/Data Science BSC/year3/recent-grads (1).csv')

st.markdown("""
    <div style="font-size:30px; font-weight: bold; margin-top: 30px; margin-bottom: 10px;">
    Section 3: Understanding Employment Distribution Across Major Categories
    </div>
""", unsafe_allow_html=True)

# Title for the Streamlit app

st.markdown("""
    <div class="intro-text">
    In this section, you can explore the distribution of job types among different major categories, providing a comprehensive overview of what jobs graduates tend to work based on their field of study. The visualization highlights the number of graduates in college-level jobs, non-college jobs, and low-wage service jobs for each major category.
    <br>
    By analyzing this data, you can gain insights into the career paths associated with various fields, helping you understand the alignment between academic training and employment outcomes. Use these visualizations to compare the types of jobs graduates secure across different majors and uncover trends that may influence career planning and educational choices.
    <br></div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Group data by Major Category and sum the job counts
grouped_data = data.groupby('Major_category').agg({
    'College_jobs': 'sum',
    'Non_college_jobs': 'sum',
    'Low_wage_jobs': 'sum'
}).reset_index()

grouped_data = grouped_data[grouped_data['Major_category'] != 'Interdisciplinary']

# Create the figure
fig = go.Figure()

# Add bars for each job type
fig.add_trace(go.Bar(
    x=grouped_data['Major_category'],
    y=grouped_data['College_jobs'],
    name='College Jobs',
    marker=dict(color='darkgray'),
    hovertemplate='<b>Count:</b> %{y}<extra></extra>'  # Show only the count

))

fig.add_trace(go.Bar(
    x=grouped_data['Major_category'],
    y=grouped_data['Non_college_jobs'],
    name='Non-College Jobs',
    marker=dict(color='rgba(26, 118, 255, 0.7)'),
    hovertemplate='<b>Count:</b> %{y}<extra></extra>'  # Show only the count

))

fig.add_trace(go.Bar(
    x=grouped_data['Major_category'],
    y=grouped_data['Low_wage_jobs'],
    name='Low Wage Service Jobs',
    marker=dict(color='orange'),
    hovertemplate='<b>Count:</b> %{y}<extra></extra>'  # Show only the count

))

# Update layout for better visibility and styling
fig.update_layout(
    title={
        'text': 'Employment Types by Major Category: College, Non-College, and Service Jobs',
        'x': 0.5,  # Center the title horizontally
        'xanchor': 'center'  # Align the title to the center
    },
    xaxis_title='Major Category',
    yaxis_title='Number of Jobs',
    barmode='group',  # Group bars side by side
    template='plotly_white'
)

# Display the figure in Streamlit
st.plotly_chart(fig, use_container_width=True)

########## END OF THIRD VISU ##################




