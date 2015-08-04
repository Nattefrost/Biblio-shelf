SELECT title,read, editor, author 
FROM Books B
JOIN Authors A
ON B.author_id = A.id
JOIN Editors E
ON B.editor_id = E.id;