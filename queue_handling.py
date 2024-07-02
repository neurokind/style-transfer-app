import time
import threading
import uuid
from queue import Queue

import model_inference


class RequestQueue:
    def __init__(self):
        # Создаем очередь для обработки запросов
        self.queue = Queue()
        
        # Список для хранения результатов
        self.requests_results = []
        
        # Запуск потока обработки запросов в очереди
        self.process_requests_thread = threading.Thread(target=self.__process_requests, daemon=True)
        self.process_requests_thread.start()
        
        print("created queue instance")
    
      
    # Функция для обработки запросов в очереди
    def __process_requests(self):
        while True:
            time.sleep(1)
            if not self.queue.empty():
                request = self.queue.get()
                result = self.edit_image(request["content_image"], request["style_image"], request["epochs"])
                request["result"] = result
                self.requests_results.append(request)
                
                
    # Функция для запуска обработки изображения
    def edit_image(self, content_image, style_image, epochs):
        print("started editing image")
        edited_image = model_inference.inference_edit_image(content_image, style_image, epochs)
        
        return edited_image
    
    
    # Пытаемся извлечь результат запроса из списка результатов
    def fetch_result(self, request_id):
        for request in self.requests_results:
            if request["request_id"] == request_id:
                return request
    
        return None
    
    
    # Добавление в очередь запросов
    def add_to_queue(self, content_image, style_image, epochs):
        # Создаем id запроса
        request_id = str(uuid.uuid4())
        # Добавляем запрос в очередь
        request = {"request_id": request_id, "time": time.time(), 
                   "content_image": content_image,
                   "style_image": style_image, "epochs": epochs}
        self.queue.put(request)

        # Отображаем информацию о состоянии очереди (1 epoch approx = 5 sec)
        # eta_sec = 5 * epochs
        # queue_size = self.queue.qsize()
        # if queue_size > 0:
        #     eta_sec = queue_size * 5 * epochs  # Предполагаемое время ожидания (в секундах)

        return request_id
