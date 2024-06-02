class Article:
    all = []
    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)
        author._articles.append(self)  # Add this article to the author's list of articles
        magazine.add_article(self)  # Add this article to the magazine's list of articles


    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value
        else:
            raise ValueError("Author must be of type Author")

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        else:
            raise ValueError("Magazine must be of type Magazine")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            if not hasattr(self, '_title'):
                self._title = value
            else:
                raise AttributeError("Title cannot be changed after instantiation") #TODO replace raise ValueError with raise AttributeError
        else:
            raise ValueError("Title must be a string between 5 and 50 characters") #TODO replace raise ValueError with raise ValueError


class Author:
    def __init__(self, name):
        self.name = name
        self._articles = []

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value) > 0:
            if not hasattr(self, '_name'):
                self._name = value
            else:
                raise ValueError("Name cannot be changed after instantiation") #TODO replace raise ValueError with raise AttributeError
        else:
            raise ValueError("Name must be a non-empty string") #TODO replace raise ValueError with raise ValueError

    def articles(self):
        return self._articles

    def magazines(self):
        return list(set(article.magazine for article in self._articles))

    def add_article(self, magazine, title):
        article = Article(self, magazine, title)
        return article

    def topic_areas(self):
        if not self._articles:
            return None
        return list(set(magazine.category for magazine in self.magazines()))


class Magazine:
    _instances = []

    def __init__(self, name, category):
        self.name = name
        self.category = category

        self._articles = []
        Magazine._instances.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        else:
            raise ValueError("Name must be a string between 2 and 16 characters") #TODO replace raise ValueError with raise ValueError

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        else:
            raise ValueError("Category must be a non-empty string")

    def articles(self):
        return self._articles

    def contributors(self):
        return list(set(article.author for article in self._articles))

    def article_titles(self):
        if not self._articles:
            return None
        return [article.title for article in self._articles]

    def add_article(self, article):
        self._articles.append(article)

    def contributing_authors(self):
        author_counts = {}
        for article in self._articles:
            author = article.author
            if author not in author_counts:
                author_counts[author] = 0
            author_counts[author] += 1

        prolific_authors = [author for author, count in author_counts.items() if count > 2]
        if prolific_authors:
            return prolific_authors
        else:
            return None

    @classmethod
    def top_publisher(cls):
        if not cls._instances or all(len(magazine.articles()) == 0 for magazine in cls._instances):
            return None
        return max(cls._instances, key=lambda magazine: len(magazine.articles()))