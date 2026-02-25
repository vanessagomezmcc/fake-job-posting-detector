import streamlit as st
import pickle
import os
import re  # Added for validation function

# ==============================
# Load Model
# ==============================
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

try:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ==============================
# Helper: Validate Job Posting
# ==============================
def is_valid_job_posting(text):
    """
    Validates whether the input text appears to be a legitimate job posting.
    Returns: (is_valid: bool, error_message: str or None)
    """
    text_lower = text.lower()
    
    # Minimum length check
    if len(text.split()) < 40:
        return False, "The text is too short to be a full job description (minimum 40 words)."
    
    # Must contain job-related keywords
    job_keywords = [
        "responsibilities", "requirements", "qualifications", "experience",
        "skills", "salary", "benefits", "position", "role", "apply",
        "company", "job", "duties", "candidate", "team", "work"
    ]
    keyword_hits = sum(1 for word in job_keywords if word in text_lower)
    
    if keyword_hits < 2:
        return False, "The text does not appear to contain typical job description elements."
    
    # Sentence structure check
    if len(re.findall(r"[.!?]", text)) < 2:
        return False, "The input does not appear to be a structured job posting."
    
    return True, None

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Fake Job Posting Detector",
    page_icon="🔍",
    layout="wide"
)

# ==============================
# Page Title
# ==============================
st.title("Fake Job Posting Detector")
st.write("Paste a job posting below to analyze fraud risk.")

# =============================
# TRANSPARENCY SECTION (AT TOP)
# =============================
with st.expander("How to Interpret Results (Click to Expand)"):
    st.markdown("""
### 1. Fraud Probability
This score ranges from **0 to 1** and represents the model's confidence that the job posting is fraudulent.

- Closer to **1.0** → Higher fraud likelihood  
- Closer to **0.0** → More likely legitimate  

The model uses:
- Language patterns
- Word combinations (TF-IDF bigrams)
- Structural writing signals
- Patterns learned from thousands of labeled job postings

---

### 2. Risk Levels (Threshold = 0.67)

- **High Risk (≥ 0.67)**  
  Strong match to known fraud characteristics.

- **Medium Risk (0.40 – 0.66)**  
  Some suspicious signals detected. Manual review recommended.

- **Likely Legitimate (< 0.40)**  
  No strong fraud indicators detected.

---

### 3. Model Performance (Test Set)

- Fraud Recall: ~90%  
  → The model detects ~9 out of 10 fraudulent postings.

- Fraud Precision: ~65%  
  → About 65% of flagged postings are truly fraudulent.

- PR-AUC: ~0.89  
  → Strong performance on imbalanced fraud data.

---

### 4. Important Disclaimer

This tool is a **decision-support system**, not a final authority.

High-risk results should trigger **manual verification**, not automatic rejection.
""")

st.markdown("---")

# ==============================
# Input Section
# ==============================
job_text = st.text_area(
    "Job Posting Text",
    height=200,
    placeholder="Paste the full job description here...\n\nExample:\nJob Title: Senior Data Analyst\nResponsibilities: Analyze large datasets...\nRequirements: 3+ years experience..."
)

# Show word count
if job_text:
    word_count = len(job_text.split())
    if word_count < 40:
        st.caption(f"Word count: {word_count}/40 (minimum required)")
    else:
        st.caption(f"Word count: {word_count}")

# ==============================
# Analyze Button
# ==============================
if st.button("Analyze", type="primary"):
    
    if job_text.strip() == "":
        st.warning("Please paste a job posting to analyze.")
    
    else:
        #  VALIDATE INPUT FIRST
        is_valid, error_message = is_valid_job_posting(job_text)
        
        if not is_valid:
            st.error(error_message)
            st.info("""
**Tips for valid input:**
- Include at least 40 words
- Include job-related terms (responsibilities, requirements, qualifications, etc.)
- Use complete sentences with proper punctuation
            """)
        
        else:
            # INPUT IS VALID - PROCEED WITH ANALYSIS
            try:
                prob = model.predict_proba([job_text])[0][1]
                threshold = 0.67

                # Display Results
                st.success("Valid job posting detected - Analysis complete!")
                st.write("")
                
                # Fraud Probability
                st.metric(
                    label="Fraud Probability",
                    value=f"{prob:.2%}",
                    delta=None
                )

                # Risk Classification
                if prob >= threshold:
                    st.error("**High Risk of Fraud**")
                    st.write("This posting shows strong indicators of fraudulent activity. Proceed with extreme caution.")
                elif prob >= 0.40:
                    st.warning("**Medium Risk**")
                    st.write("Some suspicious signals detected. Manual review and verification recommended.")
                else:
                    st.success("**Likely Legitimate**")
                    st.write("No strong fraud indicators detected. This posting appears legitimate.")
                
                # Additional Details (Expandable)
                with st.expander("See detailed breakdown"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Risk Score Breakdown:**")
                        st.write(f"- Raw probability: {prob:.4f}")
                        st.write(f"- Threshold: {threshold}")
                        st.write(f"- Distance from threshold: {abs(prob - threshold):.4f}")
                    
                    with col2:
                        st.write("**Next Steps:**")
                        if prob >= threshold:
                            st.write("- Do NOT apply or share personal information")
                            st.write("- Research the company thoroughly")
                            st.write("- Verify contact information independently")
                        elif prob >= 0.40:
                            st.write("- ✓ Verify company exists and is legitimate")
                            st.write("- ✓ Check for similar scam reports online")
                            st.write("- ✓ Be cautious with personal information")
                        else:
                            st.write("- ✓ Verify company website and contact info")
                            st.write("- ✓ Research company reviews")
                            st.write("- ✓ Proceed with standard job search caution")
                
            except Exception as e:
                st.error(f"Error analyzing text: {e}")
                st.info("Please try again or contact support if the issue persists.")