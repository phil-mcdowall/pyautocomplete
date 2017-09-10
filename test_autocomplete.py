import unittest
from autocomplete import Autocomplete

class TestAutocomplete(unittest.TestCase):

    def test_empty_dictionary(self):
        ac = Autocomplete()
        self.assertEqual(ac.find("a"), [])

    def test_insert_find(self):
        ac = Autocomplete()
        ac.insert('foo')
        ac.insert('foobar')
        self.assertEquals(sorted(ac.find('foo')),['foo','foobar'])
        self.assertEquals(ac.find('foob'), ['foobar'])
        self.assertEquals(ac.find(''), ['foo','foobar'])
        self.assertEquals(ac.find('bar'),[])

    def test_insertlist_find(self):
        ac = Autocomplete(['foo','foobar'])
        self.assertEquals(sorted(ac.find('foo')),['foo','foobar'])
        self.assertEquals(ac.find('foob'), ['foobar'])
        self.assertEquals(ac.find(''), ['foo','foobar'])
        self.assertEquals(ac.find('bar'),[])

    def test_remove(self):
        ac = Autocomplete(['foo', 'foobar'])
        ac.remove('foo')
        self.assertEquals(sorted(ac.find('foo')), ['foobar'])
        self.assertEquals(ac.find('foob'), ['foobar'])
        self.assertEquals(ac.find(''), ['foobar'])
        self.assertEquals(ac.find('bar'), [])

if __name__ == '__main__':
    unittest.main()
