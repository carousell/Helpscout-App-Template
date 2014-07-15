import hmac
import hashlib
import base64


try:
    # compare_digest is only available in Python 2.7.7
    from hmac import compare_digest
except ImportError:
    # Use unsafe String comparison function for Python < 2.7.7
    compare_digest = lambda x, y: x == y


def is_helpscout_request(secret, request_data, helpscout_sig):
    """Determines if a incoming request if from Help Scout using X-HelpScout-Signature.
    Help Scout uses SHA1 as its hash function. Before comparing signatures, we need to
    base64 encode the manually computed HMAC hash.

    Keyword arguments:
        secret -- Help Scout Secret Key for a Help Scout custom app
        request_data -- Raw (String) request data from Help Scout
        helpscout_sig -- Help Scout computed hash from X-HelpScout-Signature
    """
    dig = hmac.new(secret, msg=request_data, digestmod=hashlib.sha1).digest()
    computed_sig = base64.b64encode(dig).decode()

    return compare_digest(computed_sig, helpscout_sig)
