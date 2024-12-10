# Tech Hive - E-commerce Website

Tech Hive is an e-commerce platform specializing in computer-related products, offering users a smooth and efficient online shopping experience. The website incorporates a variety of advanced features such as semantic search, an ordering system, shopping cart functionalities, and an admin portal for business analysis.

---

## Features

- **Semantic Search**: Provides intelligent product search with context-aware suggestions.
- **Advanced Search Options**: Filter and search products based on categories, specifications, and price.
- **Ordering System**: Allows customers to place orders seamlessly, with real-time order tracking.
- **Shopping Cart**: Users can add, view, and manage items in their cart.
- **Admin Portal**: Includes tools for business analysis, providing insights into product performance and sales trends.

---

## Tech Stack

### Frontend
- **HTML**
- **CSS**
- **JavaScript**

### Backend
- **[Litestar](https://docs.litestar.dev/2/)**: Used to build robust and scalable backend services.
- **[PostgreSQL](https://www.postgresql.org/)**: Database management system to handle data storage and retrieval.
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)**: For managing database migrations.
- **[Docker](https://docs.docker.com/)**: Containers are used to ensure consistency across development, testing, and production environments.

---

## Getting Started

### Installation & setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/HM3IT/tech-hive-backend.git
   cd e-commerce-backend
   ```
2. **Start the docker-container**
   For window user
    ```bash
    ./start.dev.sh
    ```

    For linux user
    ```bash
    bash start.dev.sh
    ```

![image](https://github.com/user-attachments/assets/c39bd119-bb33-453b-bdf2-ffc9d65c5d9d)

3. **API endpoint**:
To test the API separately from the front-end, use the [Swagger UI](http://127.0.0.1:8000/schema/swagger)
