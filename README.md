# Books and Authors Management System

This project is a mini full-stack application for managing books and authors. The server side is built with Django and GraphQL, and the database used is SQLite. The client side, which is currently pending, will be developed using React.

## Features

- Create, update, and retrieve books and authors.
- Enforce unique constraints on author names.
- Use GraphQL for API queries and mutations.


## GraphQL API

### Queries

- Retrieve all books:
```graphql
query {
  allBooks {
    id
    name
    genre
    author {
      name
    }
    dateReleased
  }
}
```

- Retrieve a specific book by ID:
```graphql
query {
  book(id: 1) {
    id
    name
    genre
    author {
      name
    }
    dateReleased
  }
}
```

- Retrieve all authors:
```graphql
query {
  allAuthors {
    id
    name
    books {
      name
    }
  }
}
```

- Retrieve a specific author by ID:
```graphql
query {
  author(id: 1) {
    id
    name
    books {
      name
      genre
      dateReleased
    }
  }
}
```

### Mutations

- Add an author:
```graphql
utation {
  createAuthor(name: "Friedrich Nietzsche") {
    id
    name
    success
    message
  }
}
```

- Add a book:
```graphql
mutation {
  createBook(name: "Thus Spoke Zarathustra", genre: "Philosophy", authorId: 1, dateReleased: "1883-01-01") {
    id
    name
    success
    message
  }
}
```

- Update an author:
```graphql
mutation {
  updateAuthor(id: 1, name: "F. Nietzsche") {
    id
    name
    success
    message
  }
}
```

- Update a book:
```graphql
mutation {
  updateBook(id: 1, name: "Thus Spoke Zarathustra", genre: "Philosophy", authorId: 1, dateReleased: "1883-01-01") {
    id
    name
    success
    message
  }
}
```

## Pending Features
Development of the client side using React.