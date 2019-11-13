CREATE OR REPLACE VIEW
books_vw(book_id
, guten_id
, title
, download_count
, author
, birth_year
, death_year
, book_lang
, book_subject
, shelf
, mime_type
)
AS
SELECT
b.id as book_id
,b.gutenberg_id as guten_id
,b.title
,b.download_count
,a.name as author
,a.birth_year as birth_year
,a.death_year as death_year
,l.code as book_lang
,s.name as book_subject
,sh.name as shelf
,bf.mime_type as mime_type
FROM books_book AS b
INNER JOIN books_book_authors as ba ON ba.book_id = b.id
INNER JOIN books_author as a ON a.id = ba.author_id 
INNER JOIN books_book_languages as bl ON bl.book_id = b.id
INNER JOIN books_language as l ON l.id = bl.language_id
LEFT OUTER JOIN books_book_subjects as bs ON bs.book_id = b.id
LEFT OUTER JOIN books_subject as s ON s.id = bs.subject_id
LEFT OUTER JOIN books_book_bookshelves as bsh ON bsh.book_id = b.id
LEFT OUTER JOIN books_bookshelf as sh ON sh.id = bsh.bookshelf_id
LEFT OUTER JOIN books_format as bf ON bf.book_id = b.id

