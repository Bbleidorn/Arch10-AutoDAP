import streamlit as st
import numpy as np
from styles import get_step_html

class Controller:

    def __init__(self, projects):
        self.projects = projects
        # Define steps for each project type
        self.project_steps = {
            "new_project": [
                "Select files",
                "Detection validation", 
                "Processing",
                "Modelling",
                "Hypothesis testing",
                "Analysis outline",
                "Report outline"
            ],
            "existing_project": [
                "Select files",
                "Detection validation", 
                "Processing",
                "Modelling",
                "Hypothesis testing",
                "Analysis outline",
                "Report outline"
            ]
        }
        self.initialize_session_state()
        self.render_sidebar()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "new_project"
        if 'current_step' not in st.session_state:
            st.session_state.current_step = 0

    def render_sidebar(self):
        with st.sidebar:
            st.markdown("# 🚀 Project Navigator")
            
            st.divider()

            if st.button("➕ New Project", 
                type="primary" if st.session_state.current_page == 'new_project' else "secondary",
                use_container_width=True):
                st.session_state.current_page = 'new_project'
                st.session_state.selected_project = None
                st.session_state.current_step = 0  # Reset step when switching pages
                st.rerun()

            if self.projects:
                st.markdown("### 📁 Existing Projects")
                for project in self.projects:
                    is_selected = (st.session_state.current_page == 'existing_project' and 
                    st.session_state.selected_project == project)
                    
                    button_type = "primary" if is_selected else "secondary"
                    
                    # Create button with project name
                    if st.button(f"📊 {project}", 
                               type=button_type,
                               use_container_width=True,
                               key=f"btn_{project}"):
                        st.session_state.current_page = 'existing_project'
                        st.session_state.selected_project = project
                        st.session_state.current_step = 0  # Reset step when switching projects
                        st.rerun()
            st.divider()

    def render_step_bar(self):
        """Render the step navigation bar at the bottom using external styles"""
        current_page = st.session_state.current_page
        current_step = st.session_state.current_step
        steps = self.project_steps.get(current_page, [])
        
        if not steps:
            return
        
        # Create the step navigation container
        st.markdown("---")
        
        # Navigation buttons and step bar
        col1, col2, col3 = st.columns([1, 6, 1])
        
        with col1:
            # Previous button
            if st.button("← Previous", 
                        disabled=(current_step == 0),
                        use_container_width=True):
                st.session_state.current_step = max(0, current_step - 1)
                st.rerun()
        
        with col2:
            # Step progress bar using external styles
            progress_container = st.container()
            with progress_container:
                # Create step indicators
                step_cols = st.columns(len(steps))
                
                for i, step in enumerate(steps):
                    with step_cols[i]:
                        if i == current_step:
                            # Current step
                            step_html = get_step_html(i+1, step, "current")
                        elif i < current_step:
                            # Completed steps
                            step_html = get_step_html(i+1, step, "completed")
                        else:
                            # Future steps
                            step_html = get_step_html(i+1, step, "future")
                        
                        st.markdown(step_html, unsafe_allow_html=True)
        
        with col3:
            # Next button
            if st.button("Next →", 
                        disabled=(current_step >= len(steps) - 1),
                        use_container_width=True):
                st.session_state.current_step = min(len(steps) - 1, current_step + 1)
                st.rerun()

    def get_current_step_name(self):
        """Get the name of the current step"""
        current_page = st.session_state.current_page
        current_step = st.session_state.current_step
        steps = self.project_steps.get(current_page, [])
        
        if current_step < len(steps):
            return steps[current_step]
        return "Unknown Step"

    def render_new_project(self):
        st.markdown("# New Project")
        
        # Get current step and display step-specific content
        step_name = self.get_current_step_name()
        current_step = st.session_state.current_step
        
        st.markdown(f"## Step {current_step + 1}: {step_name}")
        
        # Step-specific content
        if current_step == 0:  # Select files
            st.markdown("### Select your data files")
            st.file_uploader("Choose data files", type=['csv', 'xlsx', 'json', 'txt'], accept_multiple_files=True)
            st.text_input("Project Name", key="project_name")
            st.text_area("Project Description", key="project_description")
            
        elif current_step == 1:  # Detection validation
            st.markdown("### Validate data detection and format")
            st.selectbox("Data Format", ["CSV", "Excel", "JSON", "Text"], key="data_format")
            st.checkbox("Headers detected", value=True)
            st.checkbox("Data types detected", value=True)
            st.dataframe(np.random.randn(5, 4), use_container_width=True)
            
        elif current_step == 2:  # Processing
            st.markdown("### Data processing configuration")
            st.multiselect("Columns to include", ["Column 1", "Column 2", "Column 3", "Column 4"])
            st.selectbox("Missing value handling", ["Remove", "Fill with mean", "Fill with median", "Forward fill"])
            st.checkbox("Remove outliers")
            st.slider("Outlier threshold (IQR multiplier)", 1.0, 3.0, 1.5)
            
        elif current_step == 3:  # Modelling
            st.markdown("### Model configuration")
            st.selectbox("Analysis type", ["Descriptive", "Predictive", "Classification", "Clustering"])
            st.multiselect("Target variables", ["Variable 1", "Variable 2", "Variable 3"])
            st.multiselect("Feature variables", ["Feature A", "Feature B", "Feature C", "Feature D"])
            st.slider("Train/Test split", 0.6, 0.9, 0.8)
            
        elif current_step == 4:  # Hypothesis testing
            st.markdown("### Define hypotheses for testing")
            st.text_area("Null hypothesis (H0)", placeholder="e.g., There is no significant difference between groups")
            st.text_area("Alternative hypothesis (H1)", placeholder="e.g., There is a significant difference between groups")
            st.selectbox("Significance level (α)", [0.01, 0.05, 0.10], index=1)
            st.multiselect("Statistical tests to perform", ["T-test", "ANOVA", "Chi-square", "Correlation"])
            
        elif current_step == 5:  # Analysis outline
            st.markdown("### Define analysis structure")
            st.text_area("Research questions", placeholder="What questions will this analysis answer?")
            st.multiselect("Analysis methods", ["Descriptive statistics", "Inferential statistics", "Regression analysis", "Time series analysis"])
            st.text_area("Expected outcomes", placeholder="What results do you expect to find?")
            
        elif current_step == 6:  # Report outline
            st.markdown("### Report structure and format")
            st.selectbox("Report format", ["PDF", "HTML", "Word Document", "PowerPoint"])
            st.multiselect("Sections to include", ["Executive Summary", "Data Description", "Methodology", "Results", "Conclusions", "Recommendations"])
            st.checkbox("Include visualizations")
            st.checkbox("Include statistical tables")
            st.text_area("Additional notes", placeholder="Any specific requirements for the report?")

    def render_existing_project(self):
        project_name = st.session_state.selected_project
        st.markdown(f"# {project_name}")
        
        # Get current step and display step-specific content
        step_name = self.get_current_step_name()
        current_step = st.session_state.current_step
        
        st.markdown(f"## Step {current_step + 1}: {step_name}")
        
        # Step-specific content for existing projects
        if current_step == 0:  # Select files
            st.markdown("### Review selected files")
            st.info("Previously selected files:")
            st.write("📄 data_file_1.csv")
            st.write("📄 data_file_2.xlsx")
            st.file_uploader("Add additional files", type=['csv', 'xlsx', 'json', 'txt'], accept_multiple_files=True)
                
        elif current_step == 1:  # Detection validation
            st.markdown("### Review data detection results")
            st.success("Data format validation completed")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rows detected", "1,245")
                st.metric("Columns detected", "8")
            with col2:
                st.metric("Data quality score", "92%")
                st.metric("Missing values", "3.2%")
            
        elif current_step == 2:  # Processing
            st.markdown("### Review processing configuration")
            st.write("Current processing settings:")
            st.code("""
- Missing values: Fill with median
- Outliers: Remove (IQR > 1.5)
- Columns included: 6 of 8
- Data cleaning: Applied
            """)
            if st.button("Reprocess data"):
                st.success("Data reprocessed successfully!")
            
        elif current_step == 3:  # Modelling
            st.markdown("### Model results and configuration")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Model accuracy", "87.3%", "2.1%")
            with col2:
                st.metric("R² score", "0.82", "0.05")
            with col3:
                st.metric("Cross-validation", "85.1%", "-1.2%")
            st.line_chart(np.random.randn(20, 2))
                
        elif current_step == 4:  # Hypothesis testing
            st.markdown("### Hypothesis testing results")
            st.write("Test results:")
            test_results = {
                "Test": ["T-test", "ANOVA", "Chi-square"],
                "p-value": [0.023, 0.001, 0.045],
                "Result": ["Significant", "Significant", "Significant"]
            }
            st.dataframe(test_results)
            st.success("3 out of 3 tests show significant results")
            
        elif current_step == 5:  # Analysis outline
            st.markdown("### Analysis summary")
            st.write("**Research Questions Addressed:**")
            st.write("1. What factors influence the target variable?")
            st.write("2. Are there significant differences between groups?")
            st.write("3. Can we predict future outcomes?")
            st.bar_chart(np.random.randn(10, 3))
            
        elif current_step == 6:  # Report outline
            st.markdown("### Generated report")
            st.write("Report status: ✅ Generated")
            st.download_button("📄 Download PDF Report", "sample_report.pdf", "report.pdf")
            st.download_button("📊 Download Data Summary", "sample_data.csv", "data_summary.csv")
            st.download_button("📈 Download Visualizations", "visualizations.zip", "charts.zip")

    def render(self):
        st.title("AutoDAP")
        
        # Create a container for the main content that can scroll
        main_container = st.container()
        
        with main_container:
            # Render current page content
            current_page = st.session_state.current_page

            self.pages = {
                "new_project": self.render_new_project,
                "existing_project": self.render_existing_project
            }

            if current_page in self.pages:
                self.pages[current_page]()
        
        # Render step bar at the bottom (always visible)
        self.render_step_bar()