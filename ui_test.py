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
            st.rerun()
    
    def render_step_indicator(self):
        """Render visual step indicator bar"""
        if not st.session_state.survey_completed:
            steps = [
                {"number": 1, "title": "Personal Info", "icon": "👤"},
                {"number": 2, "title": "Professional Info", "icon": "💼"},
                {"number": 3, "title": "Feedback", "icon": "💬"}
            ]
            
            # Create columns for each step
            cols = st.columns(len(steps))
            
            for i, step in enumerate(steps):
                with cols[i]:
                    # Determine step status
                    if step["number"] < st.session_state.survey_step:
                        # Completed step
                        status_color = "#28a745"  # Green
                        status_icon = "✅"
                        text_color = "#28a745"
                    elif step["number"] == st.session_state.survey_step:
                        # Current step
                        status_color = "#007bff"  # Blue
                        status_icon = step["icon"]
                        text_color = "#007bff"
                    else:
                        # Future step
                        status_color = "#6c757d"  # Gray
                        status_icon = step["icon"]
                        text_color = "#6c757d"
                    
                    # Create step indicator
                    st.markdown(
                        f"""
                        <div style="text-align: center; margin-bottom: 20px;">
                            <div style="
                                width: 50px;
                                height: 50px;
                                border-radius: 50%;
                                background-color: {status_color};
                                color: white;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                margin: 0 auto 10px auto;
                                font-size: 20px;
                                font-weight: bold;
                            ">
                                {status_icon if step["number"] < st.session_state.survey_step else step["number"]}
                            </div>
                            <div style="
                                color: {text_color};
                                font-weight: {'bold' if step['number'] == st.session_state.survey_step else 'normal'};
                                font-size: 14px;
                            ">
                                {step["title"]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Add connector line (except for last step)
                    if i < len(steps) - 1:
                        line_color = "#28a745" if step["number"] < st.session_state.survey_step else "#dee2e6"
                        st.markdown(
                            f"""
                            <div style="
                                position: relative;
                                top: -35px;
                                left: 60%;
                                width: 80%;
                                height: 2px;
                                background-color: {line_color};
                                z-index: -1;
                            "></div>
                            """,
                            unsafe_allow_html=True
                        )
            
            st.markdown("---")  # Separator line
    
    def run(self):
        """Main controller method to run the survey"""
        st.title("📋 Employee Survey")
        
        if st.session_state.survey_completed:
            self.render_completion()
        else:
            self.render_step_indicator()
            
            # Render current step
            if st.session_state.survey_step == 1:
                self.render_step_1()
            elif st.session_state.survey_step == 2:
                self.render_step_2()
            elif st.session_state.survey_step == 3:
                self.render_step_3()

# Usage
if __name__ == "__main__":
    controller = SurveyController()
    controller.run()