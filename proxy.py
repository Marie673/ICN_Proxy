import cefpyco

with cefpyco.create_handle() as handle:
    handle.send_data("ccnx:/test", 0, "hello")
