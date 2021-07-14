import sys


def application(env, start_response):
    version = "{}.{}".format(sys.version_info.major, sys.version_info.minor)
    start_response("200 OK", [("Content-Type", "text/plain")])
    message = "Hello World!  Nginx uWSGI Python {} Docker".format(
        version
    )
    return [message.encode("utf-8")]
