"""Make a response from the requests library work like a proper stream.
David Megginson
October 2018

License: Public Domain
"""

import io


class RequestsResponseIOWrapper(io.RawIOBase):
    """Wrapper for a Response object from the requests library.  Streaming
    in requests is a bit broken: for example, if you're streaming, the
    stream from the raw property doesn't unzip the payload.

    This would be totally unnecessary if requests didn't force a
    choice between a totally-raw stream or an interator that doesn't
    act like IO.

    Copied over from libhxl-python

    """

    _seen_decode_exception = False
    """Remember if the decode_content param failed for read()."""

    BUFFER_SIZE = 0x1000
    """Size of input chunk buffer from requests.raw.iter_content"""

    def __init__(self, response):
        """Construct a wrapper around a requests response object
        @param response: the HTTP response from the requests library
        """
        self.response = response
        self.buffer = None
        self.buffer_pos = -1
        self.iter = response.iter_content(self.BUFFER_SIZE) # iterator through the input

    def read(self, size=-1):
        """Read raw byte input from the requests raw.iter_content iterator
        The function will unzip zipped content.
        @param size: the maximum number of bytes to read, or -1 for all available.
        """
        result = bytearray()

        if size == -1:
            # Read all of the content at once
            for chunk in self.iter:
                result += chunk
            self.buffer = None
        else:
            # Read from chunks until we have enough content
            while size > 0:
                if not self.buffer:
                    try:
                        self.buffer = next(self.iter)
                    except StopIteration:
                         # stop if we've run out of input
                        break
                    self.buffer_pos = 0
                avail = min(len(self.buffer)-self.buffer_pos, size) #actually read
                result += self.buffer[self.buffer_pos:self.buffer_pos+avail]
                size -= avail
                self.buffer_pos += avail
                if self.buffer_pos >= len(self.buffer):
                    self.buffer = None

        return bytes(result) # FIXME - how can we avoid a copy?

    def readinto(self, b):
        """Read content into a buffer of some kind.
        This is not very efficient right now -- too much copying.
        @param b: the buffer to read into (will read up to its length)
        """
        result = self.read(len(b))[:len(b)]
        size = len(result)
        b[:size] = result[:size]
        return size

    def readable(self):
        """Flag whether the content is readable."""
        try:
            return self.response.raw.readable()
        except:
            return True

    @property
    def content_type(self):
        return self.response.headers.get('Content-type')

    def close(self):
        """Close the streaming response."""
        return self.response.close()

# end of module
