import streamlit as st
import pandas as pd
from io import BytesIO

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Student Assessment System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL CSS
# =========================================================
st.markdown("""
<style>

/* Main page */
.stApp {
    background-color: #f4f7fb;
}

/* Main container */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Header */
.main-header {
    background: linear-gradient(135deg, #0f172a, #1e3a8a);
    padding: 28px 32px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 8px 25px rgba(0,0,0,0.10);
}

.main-header h1 {
    color: white;
    margin: 0;
    font-size: 32px;
}

.main-header p {
    color: #dbeafe;
    margin-top: 7px;
    margin-bottom: 0px;
    font-size: 15px;
}

/* Section cards */
.section-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
    margin-bottom: 18px;
}

/* Winner box */
.winner-box {
    background: linear-gradient(135deg, #fff7d6, #ffffff);
    border: 2px solid #f2c94c;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 20px;
}

.winner-box h2 {
    margin: 0;
    color: #7a5200;
}

.winner-box h3 {
    margin-top: 10px;
    margin-bottom: 5px;
    color: #111827;
}

/* Streamlit metric cards */
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 15px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.05);
}

div[data-testid="stMetricLabel"] {
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

/* Download buttons */
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

section[data-testid="stSidebar"] * {
    color: white;
}

/* Hide Streamlit footer */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================
if "results" not in st.session_state:
    st.session_state.results = None


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.markdown("# 🎓 SAS")

    st.markdown("### Student Assessment System")

    st.divider()

    st.markdown("""
    **Teacher Portal**

    📊 Dashboard  
    📂 Student List  
    📝 Assessment Marks  
    🏆 Ranking  
    📥 Export Results
    """)

    st.divider()

    st.caption("Professional Student Assessment System")


# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Student Assessment System</h1>
    <p>Teacher Portal • Student Marks • Automatic Ranking • Results Management</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# UPLOAD SECTION
# =========================================================
st.subheader("📂 Student Data")

uploaded_file = st.file_uploader(
    "Upload Student Excel File",
    type=["xlsx"],
    help="Upload an Excel file containing student numbers and names."
)


# =========================================================
# PROCESS EXCEL
# =========================================================
if uploaded_file is not None:

    try:

        df = pd.read_excel(
            uploaded_file,
            header=None,
            names=["NO.", "STUDENT NAME"]
        )

        # Remove completely empty rows
        df = df.dropna(how="all")

        # Remove rows without student name
        df = df.dropna(subset=["STUDENT NAME"])

        # Reset row numbers
        df = df.reset_index(drop=True)

        # Convert names to text
        df["STUDENT NAME"] = df["STUDENT NAME"].astype(str)

        # =================================================
        # REMOVE POSSIBLE EXCEL HEADER ROW
        # =================================================
        if len(df) > 0:

            first_name = str(df.iloc[0]["STUDENT NAME"]).strip().upper()

            if first_name in [
                "STUDENT NAME",
                "NAME",
                "NAMA",
                "NAMA MURID",
                "NAMA PELAJAR"
            ]:
                df = df.iloc[1:].reset_index(drop=True)

        # =================================================
        # FIX STUDENT NUMBERS
        # =================================================
        df["NO."] = range(1, len(df) + 1)

        total_students = len(df)

        st.success(
            f"✅ Student list loaded successfully — {total_students} students found."
        )

        # =================================================
        # DASHBOARD BEFORE CALCULATION
        # =================================================
        st.subheader("📊 Dashboard")

        if st.session_state.results is None:

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "👨‍🎓 Total Students",
                total_students
            )

            c2.metric(
                "📈 Class Average",
                "—"
            )

            c3.metric(
                "⭐ Highest Score",
                "—"
            )

            c4.metric(
                "🏆 Winner",
                "Not calculated"
            )

        # =================================================
        # SEARCH
        # =================================================
        st.subheader("🔎 Student Search")

        search = st.text_input(
            "Search by student name",
            placeholder="Type a student's name..."
        )

        if search:

            searched_students = df[
                df["STUDENT NAME"]
                .str.contains(search, case=False, na=False)
            ]

            st.dataframe(
                searched_students,
                use_container_width=True,
                hide_index=True
            )

        # =================================================
        # MARK ENTRY
        # =================================================
        st.subheader("📝 Assessment Marks")

        st.caption(
            "Enter marks from 0–100. Student number and name are locked."
        )

        mark_df = df.copy()

        mark_df["MARK 1"] = 0
        mark_df["MARK 2"] = 0
        mark_df["MARK 3"] = 0

        edited_df = st.data_editor(
            mark_df,
            use_container_width=True,
            hide_index=True,
            disabled=[
                "NO.",
                "STUDENT NAME"
            ],
            column_config={

                "NO.": st.column_config.NumberColumn(
                    "NO.",
                    width="small"
                ),

                "STUDENT NAME": st.column_config.TextColumn(
                    "STUDENT NAME",
                    width="large"
                ),

                "MARK 1": st.column_config.NumberColumn(
                    "MARK 1",
                    min_value=0,
                    max_value=100,
                    step=1,
                    format="%d"
                ),

                "MARK 2": st.column_config.NumberColumn(
                    "MARK 2",
                    min_value=0,
                    max_value=100,
                    step=1,
                    format="%d"
                ),

                "MARK 3": st.column_config.NumberColumn(
                    "MARK 3",
                    min_value=0,
                    max_value=100,
                    step=1,
                    format="%d"
                )
            },
            key="marks_editor"
        )

        st.write("")

        button1, button2 = st.columns([3, 1])

        # =================================================
        # CALCULATE BUTTON
        # =================================================
        with button1:

            calculate = st.button(
                "🧮 KIRA / CALCULATE RESULTS",
                type="primary",
                use_container_width=True
            )

        # =================================================
        # RESET BUTTON
        # =================================================
        with button2:

            reset = st.button(
                "🔄 RESET",
                use_container_width=True
            )

        if reset:

            st.session_state.results = None

            if "marks_editor" in st.session_state:
                del st.session_state["marks_editor"]

            st.rerun()

        # =================================================
        # CALCULATE RESULTS
        # =================================================
        if calculate:

            result_df = edited_df.copy()

            # Ensure numeric values
            mark_columns = [
                "MARK 1",
                "MARK 2",
                "MARK 3"
            ]

            for column in mark_columns:
                result_df[column] = pd.to_numeric(
                    result_df[column],
                    errors="coerce"
                ).fillna(0)

            # Calculate total
            result_df["TOTAL"] = (
                result_df["MARK 1"]
                + result_df["MARK 2"]
                + result_df["MARK 3"]
            )

            # Calculate percentage
            result_df["AVERAGE"] = (
                result_df["TOTAL"] / 3
            ).round(2)

            # Ranking
            result_df["RANK"] = (
                result_df["TOTAL"]
                .rank(
                    method="min",
                    ascending=False
                )
                .astype(int)
            )

            # Position function
            def get_position(rank):

                if rank == 1:
                    return "🥇 1ST"

                elif rank == 2:
                    return "🥈 2ND"

                elif rank == 3:
                    return "🥉 3RD"

                else:
                    return f"{rank}TH"

            result_df["POSITION"] = (
                result_df["RANK"]
                .apply(get_position)
            )

            # Sort results
            result_df = result_df.sort_values(
                by=[
                    "TOTAL",
                    "STUDENT NAME"
                ],
                ascending=[
                    False,
                    True
                ]
            ).reset_index(drop=True)

            st.session_state.results = result_df


        # =================================================
        # DISPLAY RESULTS
        # =================================================
        if st.session_state.results is not None:

            result_df = st.session_state.results.copy()

            highest_score = result_df["TOTAL"].max()

            class_average = (
                result_df["TOTAL"].mean()
            )

            winners = result_df[
                result_df["TOTAL"] == highest_score
            ]["STUDENT NAME"].tolist()

            # =============================================
            # DASHBOARD RESULTS
            # =============================================
            st.divider()

            st.subheader("📊 Results Dashboard")

            d1, d2, d3, d4 = st.columns(4)

            d1.metric(
                "👨‍🎓 Total Students",
                len(result_df)
            )

            d2.metric(
                "📈 Class Average",
                f"{class_average:.2f} / 300"
            )

            d3.metric(
                "⭐ Highest Score",
                f"{highest_score:.0f} / 300"
            )

            if len(winners) == 1:

                d4.metric(
                    "🏆 Winner",
                    winners[0]
                )

            else:

                d4.metric(
                    "🏆 Winners",
                    f"{len(winners)} students"
                )

            # =============================================
            # WINNER
            # =============================================
            if len(winners) == 1:

                winner_text = winners[0]

            else:

                winner_text = " • ".join(winners)

            st.markdown(
                f"""
                <div class="winner-box">
                    <h2>🏆 CHAMPION</h2>
                    <h3>{winner_text}</h3>
                    <p>
                    Highest Score:
                    <strong>{highest_score:.0f} / 300</strong>
                </div>
                """,
                unsafe_allow_html=True
            )

            # =============================================
            # TOP 3
            # =============================================
            st.subheader("🏅 Leaderboard")

            top3 = result_df[
                result_df["RANK"] <= 3
            ]

            st.dataframe(
                top3[
                    [
                        "POSITION",
                        "STUDENT NAME",
                        "MARK 1",
                        "MARK 2",
                        "MARK 3",
                        "TOTAL",
                        "AVERAGE"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            # =============================================
            # FULL RESULTS
            # =============================================
            st.subheader("📋 Complete Ranking")

            st.dataframe(
                result_df[
                    [
                        "POSITION",
                        "NO.",
                        "STUDENT NAME",
                        "MARK 1",
                        "MARK 2",
                        "MARK 3",
                        "TOTAL",
                        "AVERAGE"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

            # =============================================
            # EXCEL EXPORT
            # =============================================
            output = BytesIO()

            with pd.ExcelWriter(
                output,
                engine="openpyxl"
            ) as writer:

                export_df = result_df[
                    [
                        "RANK",
                        "POSITION",
                        "NO.",
                        "STUDENT NAME",
                        "MARK 1",
                        "MARK 2",
                        "MARK 3",
                        "TOTAL",
                        "AVERAGE"
                    ]
                ]

                export_df.to_excel(
                    writer,
                    index=False,
                    sheet_name="Assessment Results"
                )

            st.subheader("📥 Export Results")

            st.download_button(
                label="📊 DOWNLOAD RESULTS AS EXCEL",
                data=output.getvalue(),
                file_name="Student_Assessment_Results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


    except Exception as e:

        st.error(
            "❌ Unable to read the Excel file."
        )

        st.code(str(e))


# =========================================================
# NO FILE UPLOADED
# =========================================================
else:

    st.info(
        "👆 Upload your student Excel file to start the assessment."
    )

    st.markdown("### System Features")

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
        **📂 Student Management**

        Upload student names directly from Excel.
        """)

    with f2:
        st.markdown("""
        **🧮 Automatic Calculation**

        Calculate totals, averages and rankings automatically.
        """)

    with f3:
        st.markdown("""
        **🏆 Winner Selection**

        Automatically identify top-performing students.
        """)