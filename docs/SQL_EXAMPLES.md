# SQL-примеры

Примеры соответствуют таблицам `users` и `notes` проекта.

## SELECT

```sql
SELECT id, email, phone
FROM users;

SELECT id, title, status
FROM notes
WHERE status = false
ORDER BY title;
```

## INSERT

```sql
INSERT INTO users (id, email, phone)
VALUES ('user-id', 'user@example.com', '+79990000000');
```

## UPDATE

```sql
UPDATE notes
SET status = true
WHERE id = 'note-id';
```

## DELETE

```sql
DELETE FROM notes
WHERE id = 'note-id';
```

## JOIN

```sql
SELECT notes.id, notes.title, users.email
FROM notes
JOIN users ON users.id = notes.user_id
ORDER BY users.email, notes.title;
```

## Фильтрация и пагинация

```sql
SELECT id, title, status
FROM notes
WHERE status = false
ORDER BY id
LIMIT 20 OFFSET 0;
```
