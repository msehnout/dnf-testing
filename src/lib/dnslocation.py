import hashlib
import base64
import unittest


def email2location(email_address: str, tag: str = "_openpgpkey") -> str:
    """
    Implements RFC 7929, section 3
    https://tools.ietf.org/html/rfc7929#section-3
    :param email_address:
    :param tag:
    :return:
    """
    split = email_address.split("@")
    if len(split) == 2:
        local = split[0]
        domain = split[1]
        hash = hashlib.sha256()
        hash.update(local.encode('utf-8'))
        digest = base64.b16encode(hash.digest()[0:28])\
            .decode("utf-8")\
            .lower()
        return digest+"."+tag+"."+domain
    else:
        # Error
        return "Error"


class TestTransformation(unittest.TestCase):

    def test_hugh(self):
        self.assertEqual(email2location("hugh@example.com"),
                         "c93f1e400f26708f98cb19d936620da35eec8f72e57f9eec01c1afd6._openpgpkey.example.com")

    def test_packager(self):
        self.assertEqual(email2location("packager@example.com"),
                         "d6fb116e0485a16e447de0c6317eb48e6ce1370e7986400f95ebad00._openpgpkey.example.com")

    def test_revoked(self):
        self.assertEqual(email2location("revoked@example.com"),
                         "4bb47f186df233e48b09d241ee4defb821add0c35ac8311469fe1522._openpgpkey.example.com")


if __name__ == '__main__':
    unittest.main()