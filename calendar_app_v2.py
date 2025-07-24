
import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from streamlit_calendar import calendar
import os
from streamlit_autorefresh import st_autorefresh

CSV_PATH = "calendar_data.csv"

# 자동 새로고침 (30초 간격)
st_autorefresh(interval=30 * 1000, key="datarefresh")

# CSV 파일 불러오기
if os.path.exists(CSV_PATH): "C:\Users\hsukkim\OneDrive - Smilegate\인재문화실\92. 교육운영지원\calendar_data.csv
    calendar_df = pd.read_csv(CSV_PATH, parse_dates=["시작일시", "종료일시"])
else:
    calendar_df = pd.DataFrame(columns=["이름", "업무제목", "시작일시", "종료일시", "내용"])

st.title("📅 팀 업무 달력")

# 페이지 선택
page = st.sidebar.radio("페이지 선택", ["일정 등록", "일정 달력 보기"])

if page == "일정 등록":
    st.header("📝 일정 등록 페이지")
    with st.form("일정 등록"):
        name = st.text_input("이름")
        title = st.text_input("업무 제목")
        task_date = st.date_input("날짜", date.today())
        start_time = st.time_input("시작 시간", time(9, 0))
        end_time = st.time_input("종료 시간", time(18, 0))
        content = st.text_area("내용", height=100)
        submitted = st.form_submit_button("등록")

        if submitted:
            start_datetime = datetime.combine(task_date, start_time)
            end_datetime = datetime.combine(task_date, end_time)
            new_row = pd.DataFrame([[name, title, start_datetime, end_datetime, content]],
                                   columns=["이름", "업무제목", "시작일시", "종료일시", "내용"])
            calendar_df = pd.concat([calendar_df, new_row], ignore_index=True)
            calendar_df.to_csv(CSV_PATH, index=False)
            st.success("✅ 일정이 저장되었습니다!")

elif page == "일정 달력 보기":
    st.header("📆 일정 확인 페이지")

    # 이름별 고유 색상 생성
    unique_names = calendar_df["이름"].dropna().unique().tolist()
    color_palette = [
        "#1E90FF", "#FF6347", "#32CD32", "#FFD700", "#9370DB",
        "#00CED1", "#FF69B4", "#8B0000", "#2E8B57", "#DAA520"
    ]
    color_map = {name: color_palette[i % len(color_palette)] for i, name in enumerate(unique_names)}

    # 달력에 표시할 이벤트 생성
    events = []
    for _, row in calendar_df.iterrows():
        events.append({
            "title": f"{row['업무제목']} - {row['이름']}",
            "start": row["시작일시"].isoformat(),
            "end": row["종료일시"].isoformat(),
            "description": row["내용"],
            "color": color_map.get(row["이름"], "#1E90FF")
        })

    calendar_options = {
        "initialView": "dayGridMonth",
        "editable": False,
        "height": 650,
        "locale": "ko"
    }

    calendar(events=events, options=calendar_options)
