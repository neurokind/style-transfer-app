import streamlit as st
import datetime
import time
import threading

from sympy import per
import model_inference
from PIL import Image
from queue_handling import RequestQueue


# Глобальный экземпляр RequetsQueue
REQUEST_QUEUE = None


def get_request_queue():
    global REQUEST_QUEUE
    
    if REQUEST_QUEUE is None:
        REQUEST_QUEUE = RequestQueue()

    return REQUEST_QUEUE


def periodic_result_fetch(request_queue, request_id):
     textholder = st.empty()
     textholder.write(f"Текущий размер очереди: {request_queue.queue.qsize()}")
     while True:
          time.sleep(1)
          done_request = request_queue.fetch_result(request_id)
          if done_request != None:
               st.write("Done!")
               return done_request
          
          textholder.write(f"Текущий размер очереди: {request_queue.queue.qsize()}")


def main():
     # Получение или создание экземпляра очереди запросов
     request_queue = get_request_queue()
     
     # Multi select
     selections = st.multiselect("Photo style:", ["Kuindzhi", "Kandinsky", "Malevich"])

     # Number input
     choice = st.number_input("Choose the number of epochs", 0, 50)

     # File upload
     data = st.file_uploader("Share png file", type=['png'])

     if data != None:
          #edited_image = model_inference.inference_edit_image(data)

          # User image show
          st.image(data, caption="Your image", use_column_width=True)


          if st.button("Process image"):
               # Добавление в очередь запросов
               req_id, eta_sec = request_queue.add_to_queue(selections, data)
               
               st.write(f"Добавлен запрос с id: {req_id}")
               st.write(f"Ожидаемое время ожидания: {eta_sec} секунд")
               
               result = periodic_result_fetch(request_queue, req_id)
               st.image(result["result"], caption="Edited image", use_column_width=True)


if __name__ == "__main__":
     main()