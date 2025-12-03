import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import streamlit as st
import sqlite3
import os
from datetime import datetime

# CẤU HÌNH
MODEL_NAME = "wonrax/phobert-base-vietnamese-sentiment"
DB_FILE = 'sentiment.db'  # Tên file database SQLite

# AI MODEL

@st.cache_resource
def load_model():
    print("Đang tải model... Vui lòng đợi.")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    return tokenizer, model

def predict_sentiment(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    with torch.no_grad():
        outputs = model(**inputs)
    
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    prediction = torch.argmax(probabilities, dim=1).item()
    
    labels = {0: "NEGATIVE", 1: "POSITIVE", 2: "NEUTRAL"}
    
    # Chỉ trả về text và sentiment
    return {
        "text": text,
        "sentiment": labels[prediction]
    }

# DATABASE (SQLITE)

def init_db():
    """Tạo bảng history nếu chưa tồn tại"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Tạo bảng với 4 cột: id, nội dung, nhãn, thời gian
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            sentiment TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_history(text, sentiment):
    """Lưu kết quả vào database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    c.execute('INSERT INTO history (text, sentiment, timestamp) VALUES (?, ?, ?)', 
              (text, sentiment, timestamp))
    
    conn.commit()
    conn.close()

def load_history():
    """Lấy danh sách lịch sử từ database"""
    # Nếu file db chưa có, tạo mới
    if not os.path.exists(DB_FILE):
        init_db()
        return []

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # Lấy tất cả dữ liệu, sắp xếp mới nhất lên đầu
    c.execute('SELECT text, sentiment, timestamp FROM history ORDER BY id DESC')
    rows = c.fetchall()
    conn.close()
    
    # Chuyển đổi format để giống với format cũ cho dễ hiển thị
    history_list = []
    for row in rows:
        history_list.append({
            "text": row[0],
            "sentiment": row[1],
            "timestamp": row[2]
        })
    return history_list

# Hàm xóa toàn bộ dữ liệu trong bảng history
def clear_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM history")
    conn.commit()
    conn.close()
