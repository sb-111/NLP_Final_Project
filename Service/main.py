# streamlit run main.py --server.port 30001 --server.fileWatcherType none
import streamlit as st
from predict import inference_store_name

st.set_page_config(page_title="O기요 리뷰 기반 매장 추천 서비스", page_icon="🍴", layout="centered")

st.title("🍱 🍙별점 + 리뷰 기반 매장 추천 생성봇🍙 🍱")

st.markdown("안녕하세요! 저는 여러분들이 입력한 별점과 리뷰를 기반으로 한성대 인근 배달 음식점을 추천해주는 매장 추천 봇 입니다!", unsafe_allow_html=True)

with st.form(key="customer_form", clear_on_submit=False):

    # star_cols = st.columns(3)
    # taste_star = star_cols[0].radio("맛 별점", ("5", "4", "3", "2", "1"))
    # quantity_star = star_cols[1].radio("양 별점", ("5", "4", "3", "2", "1"))
    # delivery_star = star_cols[2].radio("배달 별점", ("5", "4", "3", "2", "1"))
    taste_star = st.radio("맛 별점", ("5", "4", "3", "2", "1"))
    quantity_star = st.radio("양 별점", ("5", "4", "3", "2", "1"))
    delivery_star = st.radio("배달 별점", ("5", "4", "3", "2", "1"))
    customer_review = st.text_area("리뷰를 작성해주세요!", placeholder="리뷰를 입력해주세요.", key="text")

    submit = st.form_submit_button(label="별점/리뷰 기반 음식점 추천 시작하기")

if submit:
    query = f'맛:{taste_star} 양:{quantity_star} 배달:{delivery_star} 리뷰:{customer_review}'

    st.markdown("🤔🤔 별점과 리뷰를 분석 중이에요!🤔🤔")
    with st.spinner("⌛분석 중..."):
        infer = inference_store_name(query)
        st.write(f"✅추천된 매장이에요! : {infer}")


# st.markdown("Developed by Hansung univ 23-2 NLP 팀 연어    [github](https://github.com/sb-111/NLP_Final_Project)", unsafe_allow_html=True)