import signal
import string
import unittest

import shortener
from shortener import normalize_url, url_to_hash_to_code, link_to_short

URL_SAFE_CHARS = set(string.ascii_letters + string.digits + "-_")


class ShortenerTestCase(unittest.TestCase):
    # urldb and N are module globals, so reset them around every test
    def setUp(self):
        shortener.urldb.clear()
        self.saved_n = shortener.N

    def tearDown(self):
        shortener.N = self.saved_n
        shortener.urldb.clear()


class TestNormalizeUrl(ShortenerTestCase):
    def test_lowercases_scheme_and_host_but_not_path(self):
        self.assertEqual(normalize_url("HTTPS://Example.COM/Docs"), "https://example.com/Docs")

    def test_no_port_does_not_add_none(self):
        self.assertEqual(normalize_url("https://example.com/a"), "https://example.com/a")

    def test_keeps_query_and_fragment(self):
        self.assertEqual(normalize_url("https://a.com/p?x=1#top"), "https://a.com/p?x=1#top")

    def test_no_stray_separators_without_query_or_fragment(self):
        self.assertEqual(normalize_url("https://a.com/p"), "https://a.com/p")

    def test_empty_path_becomes_slash(self):
        self.assertEqual(normalize_url("https://a.com"), "https://a.com/")

    def test_strips_default_ports(self):
        self.assertEqual(normalize_url("http://a.com:80/"), "http://a.com/")
        self.assertEqual(normalize_url("https://a.com:443/"), "https://a.com/")

    def test_keeps_port_that_is_not_default_for_scheme(self):
        self.assertEqual(normalize_url("https://a.com:80/"), "https://a.com:80/")
        self.assertEqual(normalize_url("https://a.com:22/"), "https://a.com:22/")
        self.assertEqual(normalize_url("http://a.com:8080/"), "http://a.com:8080/")

    def test_strips_surrounding_whitespace(self):
        self.assertEqual(normalize_url("  https://a.com/x\n"), "https://a.com/x")

    # Assumes you pick "default to https" for a missing scheme; flip it if you reject instead.
    def test_missing_scheme_defaults_to_https(self):
        self.assertEqual(normalize_url("example.com/x"), "https://example.com/x")

    def test_rejects_bad_input(self):
        bad_urls = [
            "",
            "   ",
            "javascript:alert(1)",
            "ftp://a.com/file",
            "https://",
            "https://a.com/my file",
            "https://a.com/\r\nSet-Cookie: x=1",
        ]
        for bad in bad_urls:
            with self.subTest(url=bad):
                with self.assertRaises(ValueError):
                    normalize_url(bad)


class TestUrlToHashToCode(ShortenerTestCase):
    def test_same_input_same_code(self):
        self.assertEqual(url_to_hash_to_code("https://a.com/", 0), url_to_hash_to_code("https://a.com/", 0))

    def test_code_is_n_url_safe_chars(self):
        for i in range(500):
            code = url_to_hash_to_code(f"https://a.com/{i}", 0)
            with self.subTest(code=code):
                self.assertEqual(len(code), shortener.N)
                self.assertTrue(set(code) <= URL_SAFE_CHARS)

    def test_each_counter_gives_a_different_code(self):
        codes = [url_to_hash_to_code("https://a.com/", c) for c in range(20)]
        self.assertEqual(len(set(codes)), 20)


class TestLinkToShort(ShortenerTestCase):
    def test_returns_code_and_stores_normalized_url(self):
        code = link_to_short("HTTPS://A.com/x")
        self.assertEqual(len(code), shortener.N)
        self.assertEqual(shortener.urldb[code], "https://a.com/x")

    def test_same_url_twice_is_deduped(self):
        first = link_to_short("https://a.com/x")
        second = link_to_short("https://a.com/x")
        self.assertEqual(first, second)
        self.assertEqual(len(shortener.urldb), 1)

    def test_equivalent_urls_share_a_code(self):
        self.assertEqual(link_to_short("https://A.com:443/x"), link_to_short("https://a.com/x"))

    def test_forced_collisions_get_unique_codes_and_dedup_still_works(self):
        shortener.N = 1  # only 64 possible codes, so collisions are guaranteed
        urls = [f"https://a.com/{i}" for i in range(20)]
        codes = [link_to_short(u) for u in urls]
        self.assertEqual(len(set(codes)), len(urls))
        for url, code in zip(urls, codes):
            with self.subTest(url=url):
                self.assertEqual(shortener.urldb[code], url)
                self.assertEqual(link_to_short(url), code)  # retrace finds its own code

    # Assumes you add a max-attempts guard that raises RuntimeError.
    def test_full_table_raises_instead_of_looping_forever(self):
        shortener.N = 1
        signal.signal(signal.SIGALRM, lambda *_: self.fail("retry loop never ended"))
        signal.alarm(5)
        try:
            with self.assertRaises(RuntimeError):
                for i in range(200):
                    link_to_short(f"https://a.com/{i}")
        finally:
            signal.alarm(0)


if __name__ == "__main__":
    unittest.main()
