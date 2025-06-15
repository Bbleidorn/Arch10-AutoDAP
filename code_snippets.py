import streamlit as st
from datetime import datetime
import pandas as pd

class SurveyController:
    """Controller for managing survey/form workflow and state"""
    
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize session state variables"""
        if 'survey_step' not in st.session_state:
            st.session_state.survey_step = 1
        if 'survey_data' not in st.session_state:
            st.session_state.survey_data = {}
        if 'survey_completed' not in st.session_state:
            st.session_state.survey_completed = False
    
    def validate_step(self, step_data, step_number):
        """Validate current step data"""
        validation_rules = {
            1: lambda d: d.get('name', '').strip() != '' and d.get('email', '').strip() != '',
            2: lambda d: d.get('experience') is not None and d.get('department') is not None,
            3: lambda d: d.get('satisfaction') is not None and d.get('feedback', '').strip() != ''
        }
        
        return validation_rules.get(step_number, lambda d: True)(step_data)
    
    def next_step(self):
        """Move to next step"""
        if st.session_state.survey_step < 3:
            st.session_state.survey_step += 1
    
    def previous_step(self):
        """Move to previous step"""
        if st.session_state.survey_step > 1:
            st.session_state.survey_step -= 1
    
    def submit_survey(self):
        """Handle survey submission"""
        st.session_state.survey_data['submission_time'] = datetime.now()
        st.session_state.survey_completed = True
        # Here you would typically save to database
        self.save_survey_data()
    
    def save_survey_data(self):
        """Save survey data (mock implementation)"""
        # In real app, this would save to database
        st.success("Survey data saved successfully!")
    
    def reset_survey(self):
        """Reset survey to start"""
        st.session_state.survey_step = 1
        st.session_state.survey_data = {}
        st.session_state.survey_completed = False
    
    def render_step_1(self):
        """Render personal information step"""
        st.header("Step 1: Personal Information")
        
        with st.form("step1_form"):
            name = st.text_input("Full Name*", value=st.session_state.survey_data.get('name', ''))
            email = st.text_input("Email Address*", value=st.session_state.survey_data.get('email', ''))
            phone = st.text_input("Phone Number", value=st.session_state.survey_data.get('phone', ''))
            
            col1, col2 = st.columns([1, 1])
            with col2:
                next_clicked = st.form_submit_button("Next →", use_container_width=True)
            
            if next_clicked:
                step_data = {'name': name, 'email': email, 'phone': phone}
                if self.validate_step(step_data, 1):
                    st.session_state.survey_data.update(step_data)
                    self.next_step()
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    def render_step_2(self):
        """Render professional information step"""
        st.header("Step 2: Professional Information")
        
        with st.form("step2_form"):
            experience = st.selectbox(
                "Years of Experience*",
                options=[None, "0-2 years", "3-5 years", "6-10 years", "10+ years"],
                index=0 if st.session_state.survey_data.get('experience') is None else 
                      ["0-2 years", "3-5 years", "6-10 years", "10+ years"].index(st.session_state.survey_data.get('experience')) + 1
            )
            
            department = st.selectbox(
                "Department*",
                options=[None, "Engineering", "Marketing", "Sales", "HR", "Finance", "Other"],
                index=0 if st.session_state.survey_data.get('department') is None else
                      ["Engineering", "Marketing", "Sales", "HR", "Finance", "Other"].index(st.session_state.survey_data.get('department')) + 1
            )
            
            skills = st.multiselect(
                "Technical Skills",
                options=["Python", "JavaScript", "SQL", "Data Analysis", "Machine Learning", "Web Development"],
                default=st.session_state.survey_data.get('skills', [])
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                prev_clicked = st.form_submit_button("← Previous", use_container_width=True)
            with col2:
                next_clicked = st.form_submit_button("Next →", use_container_width=True)
            
            if prev_clicked:
                self.previous_step()
                st.rerun()
            
            if next_clicked:
                step_data = {'experience': experience, 'department': department, 'skills': skills}
                if self.validate_step(step_data, 2):
                    st.session_state.survey_data.update(step_data)
                    self.next_step()
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    def render_step_3(self):
        """Render feedback step"""
        st.header("Step 3: Feedback")
        
        with st.form("step3_form"):
            satisfaction = st.select_slider(
                "Overall Satisfaction*",
                options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                value=st.session_state.survey_data.get('satisfaction', "Neutral")
            )
            
            feedback = st.text_area(
                "Additional Comments*",
                value=st.session_state.survey_data.get('feedback', ''),
                height=100
            )
            
            newsletter = st.checkbox(
                "Subscribe to newsletter",
                value=st.session_state.survey_data.get('newsletter', False)
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                prev_clicked = st.form_submit_button("← Previous", use_container_width=True)
            with col2:
                submit_clicked = st.form_submit_button("Submit Survey", type="primary", use_container_width=True)
            
            if prev_clicked:
                self.previous_step()
                st.rerun()
            
            if submit_clicked:
                step_data = {'satisfaction': satisfaction, 'feedback': feedback, 'newsletter': newsletter}
                if self.validate_step(step_data, 3):
                    st.session_state.survey_data.update(step_data)
                    self.submit_survey()
                    st.rerun()
                else:
                    st.error("Please fill in all required fields (marked with *)")
    
    def render_completion(self):
        """Render completion page"""
        st.success("🎉 Survey Completed Successfully!")
        st.balloons()
        
        st.subheader("Thank you for your feedback!")
        st.write(f"Submitted on: {st.session_state.survey_data['submission_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Show summary
        with st.expander("View Your Responses"):
            data = st.session_state.survey_data.copy()
            data.pop('submission_time', None)  # Remove timestamp for display
            st.json(data)
        
        if st.button("Take Another Survey"):
            self.reset_survey()
            st.re




import streamlit as st
from datetime import datetime
import pandas as pd

class SurveyController:
    """Controller for managing survey/form page logic"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'survey_submitted' not in st.session_state:
            st.session_state.survey_submitted = False
        if 'survey_data' not in st.session_state:
            st.session_state.survey_data = {}
        if 'form_errors' not in st.session_state:
            st.session_state.form_errors = {}
    
    def validate_form(self, form_data):
        """Validate form inputs"""
        errors = {}
        
        if not form_data.get('name', '').strip():
            errors['name'] = "Name is required"
        
        if not form_data.get('email', '').strip():
            errors['email'] = "Email is required"
        elif '@' not in form_data.get('email', ''):
            errors['email'] = "Please enter a valid email"
        
        if not form_data.get('satisfaction'):
            errors['satisfaction'] = "Please rate your satisfaction"
        
        return errors
    
    def collect_form_data(self):
        """Collect data from form widgets"""
        return {
            'name': st.session_state.get('user_name', ''),
            'email': st.session_state.get('user_email', ''),
            'age': st.session_state.get('user_age', 18),
            'satisfaction': st.session_state.get('satisfaction_rating'),
            'services': st.session_state.get('services_used', []),
            'feedback': st.session_state.get('user_feedback', ''),
            'recommend': st.session_state.get('would_recommend', False),
            'timestamp': datetime.now()
        }
    
    def submit_survey(self):
        """Handle survey submission"""
        form_data = self.collect_form_data()
        errors = self.validate_form(form_data)
        
        if errors:
            st.session_state.form_errors = errors
            return False
        else:
            st.session_state.form_errors = {}
            st.session_state.survey_data = form_data
            st.session_state.survey_submitted = True
            return True
    
    def reset_survey(self):
        """Reset survey to initial state"""
        keys_to_clear = [
            'user_name', 'user_email', 'user_age', 'satisfaction_rating',
            'services_used', 'user_feedback', 'would_recommend'
        ]
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.survey_submitted = False
        st.session_state.survey_data = {}
        st.session_state.form_errors = {}
    
    def render_form(self):
        """Render the survey form"""
        st.title("📋 Customer Satisfaction Survey")
        
        if st.session_state.survey_submitted:
            self.render_success_page()
            return
        
        with st.form("customer_survey"):
            st.subheader("Personal Information")
            
            # Name field with error handling
            name_error = st.session_state.form_errors.get('name')
            st.text_input(
                "Full Name *", 
                key="user_name",
                help="Enter your full name",
                placeholder="John Doe"
            )
            if name_error:
                st.error(name_error)
            
            # Email field with error handling
            email_error = st.session_state.form_errors.get('email')
            st.text_input(
                "Email Address *", 
                key="user_email",
                help="We'll use this to follow up if needed",
                placeholder="john.doe@example.com"
            )
            if email_error:
                st.error(email_error)
            
            # Age slider
            st.slider(
                "Age", 
                min_value=18, 
                max_value=100, 
                value=30, 
                key="user_age"
            )
            
            st.subheader("Feedback")
            
            # Satisfaction rating with error handling
            satisfaction_error = st.session_state.form_errors.get('satisfaction')
            st.select_slider(
                "Overall Satisfaction *",
                options=["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"],
                key="satisfaction_rating"
            )
            if satisfaction_error:
                st.error(satisfaction_error)
            
            # Multi-select for services
            st.multiselect(
                "Which services have you used?",
                options=["Customer Support", "Online Portal", "Mobile App", "In-Store Service", "Delivery"],
                key="services_used"
            )
            
            # Text area for feedback
            st.text_area(
                "Additional Comments",
                key="user_feedback",
                help="Tell us more about your experience",
                placeholder="Share your thoughts..."
            )
            
            # Checkbox for recommendation
            st.checkbox(
                "Would you recommend us to others?",
                key="would_recommend"
            )
            
            # Form submission buttons
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Submit Survey", type="primary")
            with col2:
                if st.form_submit_button("Clear Form"):
                    self.reset_survey()
                    st.rerun()
            
            if submitted:
                if self.submit_survey():
                    st.rerun()
    
    def render_success_page(self):
        """Render success page after submission"""
        st.success("🎉 Thank you for your feedback!")
        
        # Display submitted data
        st.subheader("Your Submission:")
        data = st.session_state.survey_data
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Name:** {data['name']}")
            st.write(f"**Email:** {data['email']}")
            st.write(f"**Age:** {data['age']}")
        
        with col2:
            st.write(f"**Satisfaction:** {data['satisfaction']}")
            st.write(f"**Would Recommend:** {'Yes' if data['recommend'] else 'No'}")
            st.write(f"**Services Used:** {', '.join(data['services']) if data['services'] else 'None'}")
        
        if data['feedback']:
            st.write(f"**Comments:** {data['feedback']}")
        
        # Option to submit another survey
        if st.button("Submit Another Survey"):
            self.reset_survey()
            st.rerun()

# Usage
def main():
    survey_controller = SurveyController()
    survey_controller.render_form()

if __name__ == "__main__":
    main()



import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

class SidebarController:
    """Controller for managing sidebar-based navigation and filtering"""
    
    def __init__(self):
        self.initialize_session_state()
        self.pages = {
            "Dashboard": self.render_dashboard,
            "Data Analysis": self.render_analysis,
            "Settings": self.render_settings,
            "About": self.render_about
        }
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
        if 'data_filters' not in st.session_state:
            st.session_state.data_filters = {}
        if 'user_preferences' not in st.session_state:
            st.session_state.user_preferences = {
                'theme': 'Light',
                'auto_refresh': False,
                'notifications': True
            }
    
    @st.cache_data
    def load_sample_data():
        """Generate sample data for demonstration"""
        np.random.seed(42)
        dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
        data = {
            'date': dates,
            'sales': np.random.normal(1000, 200, len(dates)),
            'visitors': np.random.normal(500, 100, len(dates)),
            'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Food'], len(dates)),
            'region': np.random.choice(['North', 'South', 'East', 'West'], len(dates))
        }
        return pd.DataFrame(data)
    
    def render_sidebar(self):
        """Render sidebar with navigation and filters"""
        st.sidebar.title("🚀 Analytics Dashboard")
        
        # Navigation
        st.sidebar.subheader("Navigation")
        selected_page = st.sidebar.radio(
            "Go to:",
            list(self.pages.keys()),
            key="page_selector"
        )
        
        # Update current page
        if selected_page != st.session_state.current_page:
            st.session_state.current_page = selected_page
        
        st.sidebar.divider()
        
        # Page-specific sidebar content
        if st.session_state.current_page in ["Dashboard", "Data Analysis"]:
            self.render_data_filters()
        elif st.session_state.current_page == "Settings":
            self.render_settings_sidebar()
        
        # Global sidebar elements
        st.sidebar.divider()
        self.render_sidebar_info()
    
    def render_data_filters(self):
        """Render data filtering controls in sidebar"""
        st.sidebar.subheader("📊 Data Filters")
        
        # Date range filter
        st.sidebar.write("**Date Range**")
        date_range = st.sidebar.date_input(
            "Select dates:",
            value=(datetime(2024, 1, 1), datetime(2024, 12, 31)),
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2024, 12, 31),
            key="date_filter"
        )
        
        # Category filter
        categories = ['All', 'Electronics', 'Clothing', 'Books', 'Food']
        selected_category = st.sidebar.selectbox(
            "Category:",
            categories,
            key="category_filter"
        )
        
        # Region filter
        regions = ['All', 'North', 'South', 'East', 'West']
        selected_regions = st.sidebar.multiselect(
            "Regions:",
            regions[1:],  # Exclude 'All' from multiselect
            default=regions[1:],
            key="region_filter"
        )
        
        # Metric selection
        metrics = st.sidebar.multiselect(
            "Metrics to display:",
            ['Sales', 'Visitors', 'Conversion Rate'],
            default=['Sales', 'Visitors'],
            key="metrics_filter"
        )
        
        # Store filters in session state
        st.session_state.data_filters = {
            'date_range': date_range,
            'category': selected_category,
            'regions': selected_regions,
            'metrics': metrics
        }
        
        # Filter actions
        if st.sidebar.button("Reset Filters"):
            self.reset_filters()
    
    def render_settings_sidebar(self):
        """Render settings-specific sidebar controls"""
        st.sidebar.subheader("⚙️ Quick Settings")
        
        # Theme toggle
        st.session_state.user_preferences['theme'] = st.sidebar.selectbox(
            "Theme:",
            ['Light', 'Dark'],
            index=0 if st.session_state.user_preferences['theme'] == 'Light' else 1
        )
        
        # Auto-refresh toggle
        st.session_state.user_preferences['auto_refresh'] = st.sidebar.toggle(
            "Auto-refresh data",
            value=st.session_state.user_preferences['auto_refresh']
        )
        
        # Notifications toggle
        st.session_state.user_preferences['notifications'] = st.sidebar.toggle(
            "Enable notifications",
            value=st.session_state.user_preferences['notifications']
        )
    
    def render_sidebar_info(self):
        """Render informational sidebar content"""
        st.sidebar.subheader("ℹ️ Info")
        st.sidebar.info(f"Current page: {st.session_state.current_page}")
        st.sidebar.info(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
        
        # Quick stats
        if st.session_state.current_page in ["Dashboard", "Data Analysis"]:
            data = self.load_sample_data()
            filtered_data = self.apply_filters(data)
            
            st.sidebar.metric(
                "Total Records",
                len(filtered_data),
                delta=len(filtered_data) - len(data)
            )
    
    def apply_filters(self, data):
        """Apply sidebar filters to data"""
        filtered_data = data.copy()
        filters = st.session_state.data_filters
        
        # Apply date filter
        if 'date_range' in filters and len(filters['date_range']) == 2:
            start_date, end_date = filters['date_range']
            filtered_data = filtered_data[
                (filtered_data['date'] >= pd.Timestamp(start_date)) &
                (filtered_data['date'] <= pd.Timestamp(end_date))
            ]
        
        # Apply category filter
        if filters.get('category') and filters['category'] != 'All':
            filtered_data = filtered_data[filtered_data['category'] == filters['category']]
        
        # Apply region filter
        if filters.get('regions'):
            filtered_data = filtered_data[filtered_data['region'].isin(filters['regions'])]
        
        return filtered_data
    
    def reset_filters(self):
        """Reset all filters to default values"""
        st.session_state.data_filters = {}
        st.rerun()
    
    def render_dashboard(self):
        """Render dashboard page"""
        st.title("📈 Dashboard")
        
        data = self.load_sample_data()
        filtered_data = self.apply_filters(data)
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_sales = filtered_data['sales'].mean()
            st.metric("Avg Daily Sales", f"${avg_sales:,.0f}")
        
        with col2:
            total_visitors = filtered_data['visitors'].sum()
            st.metric("Total Visitors", f"{total_visitors:,.0f}")
        
        with col3:
            conversion_rate = (filtered_data['sales'].sum() / filtered_data['visitors'].sum()) * 100
            st.metric("Conversion Rate", f"{conversion_rate:.2f}%")
        
        with col4:
            active_regions = filtered_data['region'].nunique()
            st.metric("Active Regions", active_regions)
        
        # Charts
        st.subheader("Sales Trend")
        daily_sales = filtered_data.groupby('date')['sales'].sum().reset_index()
        fig = px.line(daily_sales, x='date', y='sales', title="Daily Sales Over Time")
        st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            category_sales = filtered_data.groupby('category')['sales'].sum().reset_index()
            fig = px.pie(category_sales, values='sales', names='category', title="Sales by Category")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            region_sales = filtered_data.groupby('region')['sales'].sum().reset_index()
            fig = px.bar(region_sales, x='region', y='sales', title="Sales by Region")
            st.plotly_chart(fig, use_container_width=True)
    
    def render_analysis(self):
        """Render data analysis page"""
        st.title("🔍 Data Analysis")
        
        data = self.load_sample_data()
        filtered_data = self.apply_filters(data)
        
        # Analysis options
        analysis_type = st.selectbox(
            "Choose analysis type:",
            ["Statistical Summary", "Correlation Analysis", "Trend Analysis"]
        )
        
        if analysis_type == "Statistical Summary":
            st.subheader("Statistical Summary")
            st.dataframe(filtered_data.describe())
            
        elif analysis_type == "Correlation Analysis":
            st.subheader("Correlation Matrix")
            numeric_cols = filtered_data.select_dtypes(include=[np.number])
            corr_matrix = numeric_cols.corr()
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
            
        elif analysis_type == "Trend Analysis":
            st.subheader("Trend Analysis")
            monthly_data = filtered_data.groupby(filtered_data['date'].dt.to_period('M')).agg({
                'sales': 'sum',
                'visitors': 'sum'
            }).reset_index()
            monthly_data['date'] = monthly_data['date'].astype(str)
            
            fig = px.line(monthly_data, x='date', y=['sales', 'visitors'], 
                         title="Monthly Trends")
            st.plotly_chart(fig, use_container_width=True)
        
        # Raw data table
        st.subheader("Filtered Data Preview")
        st.dataframe(filtered_data.head(100))
    
    def render_settings(self):
        """Render settings page"""
        st.title("⚙️ Settings")
        
        # User preferences
        st.subheader("User Preferences")
        prefs = st.session_state.user_preferences
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Theme:** {prefs['theme']}")
            st.write(f"**Auto-refresh:** {'Enabled' if prefs['auto_refresh'] else 'Disabled'}")
            st.write(f"**Notifications:** {'Enabled' if prefs['notifications'] else 'Disabled'}")
        
        with col2:
            if st.button("Export Settings"):
                st.download_button(
                    "Download settings.json",
                    data=str(prefs),
                    file_name="settings.json"
                )
        
        # Data management
        st.subheader("Data Management")
        
        if st.button("Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
        
        if st.button("Reset All Filters"):
            self.reset_filters()
            st.success("Filters reset!")
    
    def render_about(self):
        """Render about page"""
        st.title("ℹ️ About")
        
        st.markdown("""
        ## Analytics Dashboard
        
        This dashboard provides comprehensive analytics and data visualization capabilities.
        
        ### Features:
        - **Interactive filtering** through the sidebar
        - **Real-time data updates**
        - **Multiple visualization types**
        - **Customizable settings**
        
        ### Navigation:
        Use the sidebar to navigate between different sections and apply filters to your data.
        
        ### Support:
        For questions or support, contact the development team.
        """)
        
        # System info
        st.subheader("System Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Version:** 1.0.0")
            st.write("**Last Updated:** 2024-01-15")
        
        with col2:
            st.write("**Active Filters:**", len(st.session_state.data_filters))
            st.write("**Current Theme:**", st.session_state.user_preferences['theme'])
    
    def run(self):
        """Main controller method to run the app"""
        # Set page config
        st.set_page_config(
            page_title="Analytics Dashboard",
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Render sidebar
        self.render_sidebar()
        
        # Render current page
        current_page = st.session_state.current_page
        if current_page in self.pages:
            self.pages[current_page]()

# Usage
def main():
    sidebar_controller = SidebarController()
    sidebar_controller.run()

if __name__ == "__main__":
    main()