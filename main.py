import time
import streamlit as st

from PIL import Image
from queue_handling import RequestQueue
import app_tests


@st.cache_resource
def get_request_queue():
    """Function for generating global REQUEST_QUEUE
    used for all the users

    Returns:
        RequestQueue(): Queue of unique requests for image-editing.
    """
    global REQUEST_QUEUE
    
    if REQUEST_QUEUE is None:
        REQUEST_QUEUE = RequestQueue()

    return REQUEST_QUEUE


def periodic_result_fetch(request_queue, request_id):
    """Method that tries to get the result of
    image-editing from request_queue each 1 second.

    Args:
        request_queue (RequestQueue()): Queue of unique requests for image-editing.
        request_id (string): Uuid4 key for queue entry.

    Returns:
        dict: Entry of queue with uuid4 key, time of creation,
        request params and image as the result.
    """
    textholder = st.empty()
    textholder.write(f"Current queue size: {request_queue.queue.qsize()}")
    
    while True:
        time.sleep(1)
        done_request = request_queue.fetch_result(request_id)
        if done_request is not None:
            textholder.write("Done!")
            return done_request
          
        textholder.write(f"Текущий размер очереди: {request_queue.queue.qsize()}")
        if request_queue.queue.qsize() == 0:
            textholder.write("Your request is under processing...")


def main():
    """Main app function. Creates the streamlit UI and delegates the logic.
    """
    # Получение или создание экземпляра очереди запросов
    request_queue = get_request_queue()

    # Multi select
    selections = st.multiselect("Photo style:", ["Kuindzhi", "Kandinsky", "Malevich"])

    # Number input
    choice = st.number_input("Choose the number of epochs", 0, 50)

    # File upload
    data = st.file_uploader("Share png file", type=['png'])

    if data is not None:
        # User image show
        st.image(data, caption="Your image", use_column_width=True)


        if st.button("Process image"):
            # Request queue test (disabled)
            # app_tests.queue_test(request_queue.add_to_queue, selections, data)
            
            # Добавление в очередь запросов
            req_id, eta_sec = request_queue.add_to_queue(selections, data)

            st.write(f"Добавлен запрос с id: {req_id}")
            st.write(f"Ожидаемое время ожидания: {eta_sec} секунд")

            result = periodic_result_fetch(request_queue, req_id)
            st.image(result["result"], caption="Edited image", use_column_width=True)


if __name__ == "__main__":
    main()