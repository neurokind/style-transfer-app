def queue_test(add_to_queue, style, content, epochs):
    # Добавление в очередь запросов
    req_id1 = add_to_queue(style, content, epochs)
    req_id2 = add_to_queue(style, content, epochs)
    req_id3 = add_to_queue(style, content, epochs)
    
    if req_id1 != req_id2 != req_id3:
        print("Queue test passed")
        return 0
    else:
        print("Queue test failed")
        return 1