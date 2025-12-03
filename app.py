import streamlit as st
import pandas as pd
import json 
import utils

# Cấu hình trang
st.set_page_config(
    page_title="Trợ lý Phân loại Cảm xúc",
    layout="centered"
)

# Tiêu đề
st.title("Phân loại Cảm xúc Tiếng Việt")
st.write("Nhập câu văn bản tiếng Việt bên dưới để AI phân tích.")

# Sidebar
with st.sidebar:
    st.header("Thông tin dự án")
    st.info("Mô hình: PhoBERT")
    st.info("Dữ liệu: SQLite")
    
    st.divider()
    st.write("Quản lý dữ liệu")
    
    # Nút xóa lịch sử
    if st.button("Xóa toàn bộ lịch sử"):
        try:
            utils.clear_history()
            st.success("Đã xóa sạch dữ liệu!")
            st.rerun() 
        except Exception as e:
            st.error(f"Lỗi khi xóa: {e}")

# Khu vực nhập liệu
user_input = st.text_area("Nhập văn bản tại đây:", height=100, placeholder="Ví dụ: Hôm nay tôi rất vui...")

# Xử lý khi nhấn nút Phân loại
if st.button("Phân loại cảm xúc", type="primary"):
    if not user_input.strip():
        st.warning("Vui lòng nhập nội dung!")
    else:
        try:
            with st.spinner("Đang phân tích..."):
                tokenizer, model = utils.load_model()
                result = utils.predict_sentiment(user_input, tokenizer, model)
                utils.save_history(result['text'], result['sentiment'])
            st.success("Phân tích thành công!")
            st.write("Đầu ra:")
            json_str = json.dumps(result, ensure_ascii=False, indent=4)
            st.code(json_str, language='json')
        except Exception as e:
            st.error(f"Đã xảy ra lỗi: {e}")

# Hiển thị Lịch sử
st.divider()
st.subheader("Lịch sử phân loại")
history_data = utils.load_history()

if history_data:
    df = pd.DataFrame(history_data)
    df.columns = ["Nội dung", "Cảm xúc", "Thời gian"]
    st.dataframe(df, use_container_width=True, hide_index=True)
