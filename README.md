# Trợ lý Phân loại Cảm xúc Tiếng Việt (Vietnamese Sentiment Analysis)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![Model](https://img.shields.io/badge/Model-PhoBERT-green)](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment)

Đồ án môn học: Xây dựng ứng dụng khai phá dữ liệu văn bản sử dụng mô hình Transformer.
Ứng dụng cho phép phân loại cảm xúc từ các câu bình luận, đánh giá tiếng Việt (bao gồm cả viết tắt, teencode) thành 3 nhãn: **Tích cực (Positive)**, **Tiêu cực (Negative)**, và **Trung tính (Neutral)**.

---

## Tính năng nổi bật

* **Phân loại chính xác:** Sử dụng mô hình `PhoBERT` (được fine-tune cho tác vụ Sentiment Analysis) với độ chính xác cao.
* **Giao diện thân thiện:** Xây dựng trên nền tảng **Streamlit**, dễ dàng tương tác.
* **Xử lý đa dạng:** Hiểu được tiếng Việt có dấu, không dấu và các từ lóng phổ biến.
* **Lưu trữ lịch sử:** Tự động lưu kết quả phân loại vào cơ sở dữ liệu **SQLite** cục bộ.
* **Đầu ra chuẩn JSON:** Hiển thị kết quả dưới dạng Dictionary/JSON phục vụ tích hợp.
---

## Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.x
* **Giao diện (Frontend):** Streamlit
* **Mô hình AI (Backend):** Hugging Face Transformers, PyTorch
* **Model Checkpoint:** `wonrax/phobert-base-vietnamese-sentiment`
* **Cơ sở dữ liệu:** SQLite3
* **Xử lý dữ liệu:** Pandas

---

## Cấu trúc thư mục

```text
SentimentApp/
├── app.py              # File chính chạy giao diện Streamlit
├── utils.py            # Chứa các hàm xử lý Logic, AI và Database
├── requirements.txt    # Danh sách các thư viện cần cài đặt
├── sentiment.db        # Database SQLite (Tự sinh ra khi chạy app)
└── README.md           # Hướng dẫn sử dụng