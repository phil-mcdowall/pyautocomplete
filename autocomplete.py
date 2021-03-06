from functools import _lru_cache_wrapper
from collections import namedtuple

class _TrieNode:
    def __init__(self):
        self.children = {}
        self.terminal = False


class Autocomplete:

    def __init__(self, words=None,max_cache=0):
        """
        Instantiate autocomplete with optional
        list of words. Search results can be cached for
        better performance if search patterns are temporally correlated.
        Cache may become very large if search patterns are short.
        max_cache:0 - no cache
        max_cache:n - cache last n results
        max_cache:None - cache unlimited number of results
        :param words: list
        :param max_cache: int
        """
        self.tree = _TrieNode()
        if words:
            for word in words:
                self.insert(word)

        # wrap find in cache wrapper
        self.find = _lru_cache_wrapper(self._find,max_cache,False, namedtuple('CacheStats',
                                                                              'hits,misses,currsize,maxsize'))

    def insert(self, word):
        """
        Insert a word into the autocomplete dictionary
        :param word: string
        """
        node = self.tree
        for char in word:
            if char not in node.children:
                node.children[char] = _TrieNode()
            node = node.children[char]
        node.terminal = True

    def remove(self, word):
        """
        remove a word from the trie. This method
        will prevent the word being returned, but
        the nodes will remain in the trie as they
         may form the prefix of more words.
        :param word: string
        """
        self._find_prefix_node(word).terminal = False

    def from_dictionary_file(self, path):
        """
        Insert words into dictionary from a file.
        File should contain a single list per line.
        On linux systems this can be a system dict
        from '/usr/share/dict/words'
        :param path: string
        """
        with open(path, 'r') as f:
            for word in f.readlines():
                self.insert(word[:-1])

    def _find_children(self, root_node, accumulator, results):
            for char, child in root_node.children.items():
                if child.terminal:
                    results.append(accumulator+char)
                results = self._find_children(child, accumulator + char, results)
            return results

    def _find_prefix_node(self, pattern):
        node = self.tree
        for char in pattern:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node

    def _find(self, pattern):
        """
        Find a word in that matches the given prefix pattern.
        If no match is found returns an empty list
        :param pattern: string
        :return: list
        """
        pattern_node = self._find_prefix_node(pattern)
        if pattern_node:
            result = self._find_children(pattern_node, pattern, [])
            if pattern_node.terminal:
                result.append(pattern)
            return result
        else:
            return []

