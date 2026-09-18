import streamlit as st
import pandas as pd
from io import BytesIO

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Student Assessment System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = None


# ============================================================
# PROFESSIONAL DESIGN / CSS
# ============================================================

st.markdown("""
<style>

/* =========================================================
   MAIN PAGE
   ========================================================= */

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1500px;
}

/* Normal main-page text */
.main .block-container {
    color: #111827;
}

.main .block-container h1,
.main .block-container h2,
.main .block-container h3,
.main .block-container h4,
.main .block-container p,
.main .block-container label {
    color: #111827;
}


/* =========================================================
   HEADER
   ========================================================= */

.main-header {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #172554 45%,
        #1d4ed8 100%
    );

    padding: 30px 35px;
    border-radius: 18px;

    margin-bottom: 28px;

    box-shadow:
        0px 10px 30px
        rgba(15, 23, 42, 0.15);
}

.main-header h1 {
    color: white !important;
    margin: 0;
    font-size: 34px;
    font-weight: 800;
}

.main-header p {
    color: #dbeafe !important;
    margin-top: 8px;
    margin-bottom: 0;
    font-size: 15px;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0f172a,
            #172554
        );
}

/* Only sidebar text becomes white */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: white !important;
}


/* =========================================================
   METRIC CARDS
   ========================================================= */

div[data-testid="stMetric"] {

    background-color: white;

    border:
        1px solid
        #e5e7eb;

    padding: 20px;

    border-radius: 16px;

    box-shadow:
        0px 4px 15px
        rgba(15, 23, 42, 0.06);
}

div[data-testid="stMetric"] * {
    color: #111827 !important;
}

div[data-testid="stMetricLabel"] {
    font-weight: 700;
}


/* =========================================================
   WINNER CARD
   ========================================================= */

.winner-box {

    background:
        linear-gradient(
            135deg,
            #fff7d6,
            #ffffff
        );

    border:
        2px solid
        #f2c94c;

    padding: 28px;

    border-radius: 18px;

    text-align: center;

    margin-top: 20px;
    margin-bottom: 25px;

    box-shadow:
        0px 5px 18px
        rgba(242, 201, 76, 0.18);
}

.winner-box h2 {
    color: #8a6100 !important;
    margin: 0;
}

.winner-box h3 {
    color: #111827 !important;
    margin-top: 10px;
    margin-bottom: 5px;
}

.winner-box p {
    color: #374151 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {

    min-height: 48px;

    border-radius: 11px;

    font-weight: 700;
}

.stDownloadButton > button {

    min-height: 48px;

    border-radius: 11px;

    font-weight: 700;
}


/* =========================================================
   DATA EDITOR
   ========================================================= */

div[data-testid="stDataFrame"] {

    background: white;

    border-radius: 12px;
}


/* =========================================================
   FILE UPLOADER
   ========================================================= */

div[data-testid="stFileUploader"] {

    background-color: white;

    border-radius: 14px;

    padding: 5px;
}


/* =========================================================
   HIDE STREAMLIT FOOTER
   ========================================================= */

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("# 🎓 SAS")

    st.markdown(
        "### Student Assessment System"
    )

    st.divider()

    st.markdown("""
**👨‍🏫 Teacher Portal**

📊 Dashboard

📂 Student List

📝 Assessment Marks

🏆 Ranking

📥 Export Results
""")

    st.divider()

    st.caption(
        "Professional Student Assessment System"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown("""
<div class="main-header">

<h1>🎓 Student Assessment System</h1>

<p>
Teacher Portal • Student Marks • Automatic Ranking •
Winner Selection • Results Management
</p>

</div>
""", unsafe_allow_html=True)


# ============================================================
# STUDENT DATA
# ============================================================

st.subheader("📂 Student Data")

st.write(
    "Upload the Excel file containing your student names."
)

uploaded_file = st.file_uploader(
    "Upload Student Excel File",
    type=["xlsx"],
    help="Upload an .xlsx Excel file containing student names."
)


# ============================================================
# FILE UPLOADED
# ============================================================

if uploaded_file is not None:

    try:

        # ----------------------------------------------------
        # READ EXCEL
        # ----------------------------------------------------

        df = pd.read_excel(
            uploaded_file,
            header=None,
            names=[
                "NO.",
                "STUDENT NAME"
            ]
        )

        # Remove empty rows
        df = df.dropna(
            how="all"
        )

        # Remove rows without names
        df = df.dropna(
            subset=[
                "STUDENT NAME"
            ]
        )

        df = df.reset_index(
            drop=True
        )

        # Student name as text
        df["STUDENT NAME"] = (
            df["STUDENT NAME"]
            .astype(str)
            .str.strip()
        )


        # ----------------------------------------------------
        # REMOVE HEADER IF EXCEL ALREADY HAS ONE
        # ----------------------------------------------------

        if len(df) > 0:

            first_name = str(
                df.iloc[0]["STUDENT NAME"]
            ).strip().upper()

            possible_headers = [

                "STUDENT NAME",

                "NAME",

                "NAMA",

                "NAMA MURID",

                "NAMA PELAJAR",

                "NAMA MURID / PELAJAR"
            ]

            if first_name in possible_headers:

                df = (
                    df.iloc[1:]
                    .reset_index(drop=True)
                )


        # ----------------------------------------------------
        # NUMBER STUDENTS
        # ----------------------------------------------------

        df["NO."] = range(
            1,
            len(df) + 1
        )

        total_students = len(df)


        # ----------------------------------------------------
        # SUCCESS MESSAGE
        # ----------------------------------------------------

        st.success(
            f"✅ Student list loaded successfully — "
            f"{total_students} students found."
        )


        # ====================================================
        # DASHBOARD
        # ====================================================

        st.subheader(
            "📊 Dashboard"
        )

        if st.session_state.results is None:

            col1, col2, col3, col4 = (
                st.columns(4)
            )

            col1.metric(
                "👨‍🎓 Total Students",
                total_students
            )

            col2.metric(
                "📈 Class Average",
                "—"
            )

            col3.metric(
                "⭐ Highest Score",
                "—"
            )

            col4.metric(
                "🏆 Winner",
                "Not calculated"
            )


        # ====================================================
        # STUDENT SEARCH
        # ====================================================

        st.subheader(
            "🔎 Student Search"
        )

        search = st.text_input(
            "Search by student name",
            placeholder=
            "Type a student's name..."
        )

        if search:

            searched_students = df[
                df["STUDENT NAME"]
                .str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]

            if len(searched_students) > 0:

                st.dataframe(
                    searched_students,
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.warning(
                    "No student found."
                )


        # ====================================================
        # STUDENT LIST
        # ====================================================

        with st.expander(
            "👨‍🎓 View Student List"
        ):

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )


        # ====================================================
        # ASSESSMENT MARKS
        # ====================================================

        st.subheader(
            "📝 Assessment Marks"
        )

        st.caption(
            "Enter marks between 0 and 100. "
            "Student names and numbers are locked."
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

                "NO.":

                    st.column_config.NumberColumn(
                        "NO.",
                        width="small"
                    ),

                "STUDENT NAME":

                    st.column_config.TextColumn(
                        "STUDENT NAME",
                        width="large"
                    ),

                "MARK 1":

                    st.column_config.NumberColumn(
                        "MARK 1",
                        min_value=0,
                        max_value=100,
                        step=1,
                        format="%d"
                    ),

                "MARK 2":

                    st.column_config.NumberColumn(
                        "MARK 2",
                        min_value=0,
                        max_value=100,
                        step=1,
                        format="%d"
                    ),

                "MARK 3":

                    st.column_config.NumberColumn(
                        "MARK 3",
                        min_value=0,
                        max_value=100,
                        step=1,
                        format="%d"
                    )
            },

            key="marks_editor"
        )


        # ====================================================
        # BUTTONS
        # ====================================================

        st.write("")

        calculate_col, reset_col = (
            st.columns(
                [3, 1]
            )
        )


        # ----------------------------------------------------
        # CALCULATE
        # ----------------------------------------------------

        with calculate_col:

            calculate = st.button(

                "🧮 KIRA / CALCULATE RESULTS",

                type="primary",

                use_container_width=True
            )


        # ----------------------------------------------------
        # RESET
        # ----------------------------------------------------

        with reset_col:

            reset = st.button(

                "🔄 RESET",

                use_container_width=True
            )


        # ====================================================
        # RESET FUNCTION
        # ====================================================

        if reset:

            st.session_state.results = None

            if "marks_editor" in st.session_state:

                del st.session_state[
                    "marks_editor"
                ]

            st.rerun()


        # ====================================================
        # CALCULATION
        # ====================================================

        if calculate:

            result_df = (
                edited_df.copy()
            )

            mark_columns = [

                "MARK 1",

                "MARK 2",

                "MARK 3"
            ]


            # Make sure marks are numeric
            for column in mark_columns:

                result_df[column] = (
                    pd.to_numeric(
                        result_df[column],
                        errors="coerce"
                    )
                    .fillna(0)
                )


            # ------------------------------------------------
            # TOTAL
            # ------------------------------------------------

            result_df["TOTAL"] = (

                result_df["MARK 1"]

                + result_df["MARK 2"]

                + result_df["MARK 3"]
            )


            # ------------------------------------------------
            # AVERAGE
            # ------------------------------------------------

            result_df["AVERAGE"] = (

                result_df["TOTAL"] / 3

            ).round(2)


            # ------------------------------------------------
            # RANK
            # ------------------------------------------------

            result_df["RANK"] = (

                result_df["TOTAL"]

                .rank(
                    method="min",
                    ascending=False
                )

                .astype(int)
            )


            # ------------------------------------------------
            # POSITION LABEL
            # ------------------------------------------------

            def position_label(rank):

                if rank == 1:

                    return "🥇 1ST"

                elif rank == 2:

                    return "🥈 2ND"

                elif rank == 3:

                    return "🥉 3RD"

                else:

                    return str(rank)


            result_df["POSITION"] = (

                result_df["RANK"]
                .apply(
                    position_label
                )
            )


            # ------------------------------------------------
            # SORT BY HIGHEST SCORE
            # ------------------------------------------------

            result_df = (

                result_df

                .sort_values(

                    by=[
                        "TOTAL",
                        "STUDENT NAME"
                    ],

                    ascending=[
                        False,
                        True
                    ]
                )

                .reset_index(
                    drop=True
                )
            )


            st.session_state.results = (
                result_df
            )


        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        if (
            st.session_state.results
            is not None
        ):

            result_df = (
                st.session_state.results
                .copy()
            )


            # ------------------------------------------------
            # STATISTICS
            # ------------------------------------------------

            highest_score = (
                result_df["TOTAL"].max()
            )

            class_average = (
                result_df["TOTAL"].mean()
            )

            average_percentage = (
                class_average / 3
            )

            winners = (

                result_df[
                    result_df["TOTAL"]
                    == highest_score
                ]

                ["STUDENT NAME"]

                .tolist()
            )


            # =================================================
            # RESULT DASHBOARD
            # =================================================

            st.divider()

            st.subheader(
                "📊 Results Dashboard"
            )

            r1, r2, r3, r4 = (
                st.columns(4)
            )


            r1.metric(

                "👨‍🎓 Total Students",

                len(result_df)
            )


            r2.metric(

                "📈 Class Average",

                f"{average_percentage:.2f}%"
            )


            r3.metric(

                "⭐ Highest Score",

                f"{highest_score:.0f} / 300"
            )


            if len(winners) == 1:

                r4.metric(

                    "🏆 Winner",

                    winners[0]
                )

            else:

                r4.metric(

                    "🏆 Joint Winners",

                    len(winners)
                )


            # =================================================
            # WINNER CARD
            # =================================================

            if len(winners) == 1:

                winner_text = (
                    winners[0]
                )

                winner_title = (
                    "🏆 CHAMPION"
                )

            else:

                winner_text = (
                    " • ".join(winners)
                )

                winner_title = (
                    "🏆 JOINT CHAMPIONS"
                )


            st.markdown(
                f"""
<div class="winner-box">

<h2>{winner_title}</h2>

<h3>{winner_text}</h3>

<p>
Highest Score:
<strong>
{highest_score:.0f} / 300
</strong>
</p>

</div>
""",
                unsafe_allow_html=True
            )


            # =================================================
            # TOP 3 LEADERBOARD
            # =================================================

            st.subheader(
                "🏅 Top 3 Leaderboard"
            )

            top_three = result_df[
                result_df["RANK"] <= 3
            ]


            st.dataframe(

                top_three[
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


            # =================================================
            # COMPLETE RANKING
            # =================================================

            st.subheader(
                "📋 Complete Student Ranking"
            )


            final_display = result_df[
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
            ]


            st.dataframe(

                final_display,

                use_container_width=True,

                hide_index=True
            )


            # =================================================
            # EXCEL DOWNLOAD
            # =================================================

            st.subheader(
                "📥 Export Results"
            )

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

                    sheet_name=
                    "Assessment Results"
                )


            st.download_button(

                label=
                "📊 DOWNLOAD RESULTS AS EXCEL",

                data=
                output.getvalue(),

                file_name=
                "Student_Assessment_Results.xlsx",

                mime=
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True
            )


            st.success(
                "✅ Assessment completed successfully."
            )


    # ========================================================
    # ERROR HANDLING
    # ========================================================

    except Exception as e:

        st.error(
            "❌ Unable to process the Excel file."
        )

        st.write(
            "Please check that your Excel file "
            "contains the student number and student name."
        )

        with st.expander(
            "Technical Error Details"
        ):

            st.code(
                str(e)
            )


# ============================================================
# NO FILE YET
# ============================================================

else:

    st.info(
        "👆 Upload your student Excel file "
        "to begin the assessment."
    )

    st.write("")

    st.subheader(
        "✨ System Features"
    )

    feature1, feature2, feature3 = (
        st.columns(3)
    )


    with feature1:

        st.markdown("""
### 📂 Student Management

Upload the student list directly from an Excel file.

Search and view students from the teacher dashboard.
""")


    with feature2:

        st.markdown("""
### 🧮 Automatic Calculation

Enter three assessment marks.

The system calculates totals, averages and rankings automatically.
""")


    with feature3:

        st.markdown("""
### 🏆 Automatic Winner

Automatically identifies the highest-scoring student.

Includes Top 3 leaderboard and complete ranking.
""")


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🎓 Student Assessment System • Teacher Portal"
)
