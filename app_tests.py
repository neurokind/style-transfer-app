def queue_test(add_to_queue, selections, data):
    # Добавление в очередь запросов
    req_id1, eta_sec1 = add_to_queue(selections, data)
    req_id2, eta_sec2 = add_to_queue(selections, data)
    req_id3, eta_sec3 = add_to_queue(selections, data)
    
    if req_id1 != req_id2 != req_id3 and eta_sec1 != eta_sec2 != eta_sec3:
        print("Queue test passed")
        return 0
    else:
        print("Queue test failed")
        return 1