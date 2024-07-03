import time
import threading
import uuid
from queue import Queue

import model_inference


# Class of queue of requests. Instance must be single for all users
class RequestQueue:
    def __init__(self):
        # Create queue
        self.queue = Queue()
        
        # Create results list
        self.requests_results = []
        
        # Start the thread of request processing
        self.process_requests_thread = threading.Thread(target=self.__process_requests, daemon=True)
        self.process_requests_thread.start()
        
        print("created queue instance")
    
      
    def __process_requests(self):
        """Request processing method. Has infinite loop.
        Must work in own thread to don't stop other processes.
        """
        while True:
            time.sleep(1)
            if not self.queue.empty():
                request = self.queue.get()
                result = self.edit_image(request["content_image"], request["style_image"], request["epochs"])
                request["result"] = result
                self.requests_results.append(request)
                
                
    def edit_image(self, content_image, style_image, epochs):
        """Method delegates image editting process to the model.

        Args:
            content_image (image): content image to feed the model.
            style_image (image): style image to feed the model.
            epochs (int): count of epochs for model training.

        Returns:
            image: image edited by the model.
        """
        edited_image = model_inference.inference_edit_image(content_image, style_image, epochs)
        
        return edited_image
    
    
    def fetch_result(self, request_id):
        """Method to get and delete the result from 
        results list by request_id if the result is in presence.

        Args:
            request_id (uuid4): unique id identifying a request.

        Returns:
            dict or None: dictionary represents a request itself.
        """
        for i in range(0, len(self.requests_results)):
            request = self.requests_results[i]
            if request["request_id"] == request_id:
                request_to_return = request
                self.requests_results.pop(i)

                return request_to_return

        return None
    
    
    def add_to_queue(self, content_image, style_image, epochs):
        """Method creates a request and adds it to queue of requests.

        Args:
            content_image (image): content image to feed the deep learning model.
            style_image (image): style image to feed the deep learning model.
            epochs (int): count of epochs for training the deep learning model.

        Returns:
            uuid4: unique id identifying a request.
        """
        # Create request uuid
        request_id = str(uuid.uuid4())
        # Add to queue
        request = {"request_id": request_id, "time": time.time(), 
                   "content_image": content_image,
                   "style_image": style_image, "epochs": epochs}
        self.queue.put(request)

        return request_id
