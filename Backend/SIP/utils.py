import re


# uri in format sip:SOMEID@DOMANINNAME
# gets the someID part
def getIdFromUri(uri):
    m = re.match("(sip:)(.+)@(.+)", uri)
    # in case the uri doesn't match at all
    if m is None:
        return False

    return m.group(2)
