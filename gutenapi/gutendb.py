from sqlalchemy import create_engine, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, desc
from contextlib import contextmanager
import os

DATABASE_URL = os.environ.get('DATABASE_URL')

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class Author(Base):
    """Base author class"""

    __tablename__ = "books_author"
    id = Column(Integer, primary_key=True)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    name = Column(String)


class AuthorLink(Base):
    """Base author class"""

    __tablename__ = "books_book_authors"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    author_id = Column(Integer)


class Language(Base):
    """Base author class"""

    __tablename__ = "books_language"
    id = Column(Integer, primary_key=True)
    code = Column(String)


class LanguageLink(Base):
    """Base author class"""

    __tablename__ = "books_book_languages"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    language_id = Column(Integer)


class Subject(Base):
    """Base author class"""

    __tablename__ = "books_subject"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class SubjectLink(Base):
    """Base author class"""

    __tablename__ = "books_book_subjects"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    subject_id = Column(Integer)


class BookShelf(Base):
    """Base author class"""

    __tablename__ = "books_bookshelf"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class BookShelfLink(Base):
    """Base author class"""

    __tablename__ = "books_book_bookshelves"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer)
    bookshelf_id = Column(Integer)


class BookFormat(Base):
    """Base author class"""

    __tablename__ = "books_format"
    id = Column(Integer, primary_key=True)
    mime_type = Column(String)
    url = Column(String)
    book_id = Column(Integer)


class Books(Base):
    """Base books class. This is a view in database"""

    __tablename__ = "books_vw"
    book_id = Column(Integer, primary_key=True)
    guten_id = Column(Integer)
    download_count = Column(Integer)
    title = Column(String)
    author = Column(String)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    book_lang = Column(String)
    subject = Column(String)
    shelf = Column(String)
    mime_type = Column(String)


def get_books(**kwargs):

    guten_ids = kwargs.get("guten_ids", None)
    languages = kwargs.get("languages", None)
    authors = kwargs.get("authors", None)
    titles = kwargs.get("titles", None)
    topics = kwargs.get("topics", None)
    mime_types = kwargs.get("mime_types", None)

    page = kwargs.get("page", 0)
    page_size = kwargs.get("page_size", 25)

    books_list = []

    with session_scope() as session:

        query = session.query(
            Books.book_id, Books.guten_id, Books.title, Books.download_count
        )
        if guten_ids is not None:
            query = query.filter(Books.guten_id.in_(guten_ids))

        if languages is not None:
            _filter = []
            for lang in languages:
                _filter.append(Books.book_lang.like("%" + lang + "%"))
            query = query.filter(or_(*_filter))

        print(authors)
        if authors is not None:
            _filter = []
            for author in authors:
                _filter.append(Books.author.ilike("%" + author + "%"))
            query = query.filter(or_(*_filter))

        if titles is not None:
            _filter = []
            for title in titles:
                _filter.append(Books.title.ilike("%" + title + "%"))
            query = query.filter(or_(*_filter))

        if topics is not None:
            _filter = []
            for topic in topics:
                _filter.append(Books.subject.ilike("%" + topic + "%"))
                _filter.append(Books.shelf.ilike("%" + topic + "%"))
            query = query.filter(or_(*_filter))

        book_count = query.distinct().count()

        if mime_types is not None:
            _filter = []
            for mime_type in mime_types:
                _filter.append(Books.title.like("%" + mime_type + "%"))
            query = query.filter(or_(*_filter))

        query = query.distinct().order_by(desc(Books.download_count))

        if page_size:
            query = query.limit(page_size)
        if page:
            query = query.offset(page * page_size)

        if page > 0:
            prev_page = page - 1
        else:
            prev_page = 0

        next_page = page + 1
        if page_size * next_page > book_count:
            next_page = page

        books = query.all()

        if books is not None:
            for book in books:

                book_authors = (
                    session.query(Author.name, Author.birth_year, Author.death_year)
                    .filter(Author.id == AuthorLink.author_id)
                    .filter(AuthorLink.book_id == book.book_id)
                ).all()

                book_langs = (
                    session.query(Language.code)
                    .filter(Language.id == LanguageLink.language_id)
                    .filter(LanguageLink.book_id == book.book_id)
                ).all()

                book_subjects = (
                    session.query(Subject.name)
                    .filter(Subject.id == SubjectLink.subject_id)
                    .filter(SubjectLink.book_id == book.book_id)
                ).all()

                book_shelves = (
                    session.query(BookShelf.name)
                    .filter(BookShelf.id == BookShelfLink.bookshelf_id)
                    .filter(BookShelfLink.book_id == book.book_id)
                ).all()

                book_formats = (
                    session.query(BookFormat.mime_type, BookFormat.url)
                    .filter(BookFormat.book_id == book.book_id)
                    .all()
                )

                books_list.append(
                    {
                        "gutenberg_id": book.guten_id,
                        "title": book.title,
                        "download_count": book.download_count,
                        "authors": [book_auth._asdict() for book_auth in book_authors],
                        "languages": [book_lang.code for book_lang in book_langs],
                        "subjects": [book_sub.name for book_sub in book_subjects],
                        "bookshelves": [book_shelf.name for book_shelf in book_shelves],
                        "links": [
                            book_format._asdict() for book_format in book_formats
                        ],
                    }
                )
    response = {
        "count": book_count,
        "previous": prev_page,
        "next": next_page,
        "books": books_list,
    }
    return response
