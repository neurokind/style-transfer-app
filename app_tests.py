def queue_test(add_to_queue, style, content, epochs):
    """Testing method to check if requests in queue has unique indexes.

    Args:
        add_to_queue (method): any method to add request in queue that returns index of request.
        style (image): style image to feed deep learning model.
        content (image): content image to feed the deep learning model.
        epochs (int): count of epochs to train deep learning model.

    Returns:
        int: 0 if test passed, 1 if test not passed.
    """
    # Add 3 requests to queue
    req_id1 = add_to_queue(style, content, epochs)
    req_id2 = add_to_queue(style, content, epochs)
    req_id3 = add_to_queue(style, content, epochs)
    
    if req_id1 != req_id2 != req_id3:
        print("Queue test passed")
        return 0
    else:
        print("Queue test failed")
        return 1