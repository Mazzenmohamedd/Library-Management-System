class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.book_isbns = set()

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def _normalize(self, word):
        """Normalize word: lowercase and keep only alphanumeric and hyphens."""
        return ''.join(c for c in word.lower() if c.isalnum() or c == '-')

    def insert(self, text, isbn):
        """Insert all keywords from the text into the Trie, mapping to the given ISBN."""
        words = text.split()
        for word in words:
            clean_word = self._normalize(word)
            if not clean_word:
                continue
            
            node = self.root
            for char in clean_word:
                if char not in node.children:
                    node.children[char] = TrieNode()
                node = node.children[char]
            node.is_end_of_word = True
            node.book_isbns.add(isbn)

    def search(self, keyword):
        """Search for a keyword and return a set of ISBNs."""
        clean_word = self._normalize(keyword)
        if not clean_word:
            return set()

        node = self.root
        for char in clean_word:
            if char not in node.children:
                return set()
            node = node.children[char]
        
        # Return exact matches. For prefix search, we would traverse deeper.
        # SRS implies "relevant book records", exact keyword matching is safer for now 
        # but prefix support is good for "Trie" expectations.
        # Let's collect all ISBNs from this node downwards to support prefix search (e.g., "Har" -> "Harry Potter")
        return self._collect_isbns(node)

    def _collect_isbns(self, node):
        isbns = set(node.book_isbns)
        for child in node.children.values():
            isbns.update(self._collect_isbns(child))
        return isbns

    def multi_keyword_search(self, keywords):
        """
        Search for multiple keywords and return the intersection of results.
        If a keyword returns no results, the intersection will be empty.
        """
        if not keywords:
            return set()
            
        result_sets = []
        for kw in keywords:
            res = self.search(kw)
            result_sets.append(res)
        
        if not result_sets:
            return set()
            
        # Intersection: only books matching ALL keywords
        final_isbns = set.intersection(*result_sets)
        return final_isbns
