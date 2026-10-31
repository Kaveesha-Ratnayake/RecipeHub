# RecipeHub

RecipeHub is a full-stack recipe discovery and management web application developed using **React, Vite, Node.js, Express.js, and MongoDB**.

The application allows users to explore recipes, search for cooking ideas, manage their own recipes, save favourites, rate recipes, and upload recipe photos. It provides a user-friendly interface with persistent database storage.

## 1. Technologies Used

**Frontend**
- React.js
- Vite
- HTML, CSS, and JavaScript

**Backend**
- Node.js
- Express.js
- RESTful APIs

**Database**
- MongoDB

**Development Tools**
- Visual Studio Code
- Git and GitHub
- npm

## 2. Main Features

### Recipe Management
- Create new recipes with ingredients, descriptions, and cooking instructions.
- View recipes and their details.
- Edit existing recipes.
- Delete recipes with confirmation.
- Search recipes by title, description, or ingredients.
- Filter recipes by category and sort results.

### User Authentication
- Register using a name, email address, and password.
- Log in and log out securely.
- Passwords are protected using salted scrypt hashes.
- Sessions use HttpOnly and SameSite cookies.
- Users can edit and delete only recipes they own.

### Favourites
- Save favourite recipes.
- View and manage saved favourites.
- Store favourites separately for each user in MongoDB.

### Ratings
- Rate recipes from 1 to 5 stars.
- Update previously submitted ratings.
- View average ratings and rating counts.
- Store ratings persistently in MongoDB.

### Recipe Photos
- Add recipe photos using an image URL.
- Upload JPEG, PNG, or WebP images up to 5 MB.
- Store uploaded images locally.

### User Interface
- Responsive recipe browsing interface.
- Recipe cards and detailed recipe views.
- Search, category filtering, and sorting.
- Consistent styling and navigation.

## 3. Project Structure

```text
RecipeHub/
├── backend/
├── frontend/
├── report/
├── scripts/
├── .gitignore
├── README.md
├── package.json
└── package-lock.json
```

## 4. Installation and Setup

### Prerequisites

- Node.js and npm
- MongoDB Community Server or MongoDB Atlas
- A modern web browser

### Step 1: Install Dependencies

Open a terminal in the RecipeHub project directory and run:

```bash
npm install
```

### Step 2: Configure MongoDB

Copy `backend/.env.example` to `backend/.env` and configure the `MONGODB_URI` connection string.

Never upload `.env` files containing database credentials to GitHub.

### Step 3: Start MongoDB

For the documented local Windows setup, run:

```bash
npm run db
```

The local database runs on `127.0.0.1:27017`.

Alternatively, configure a MongoDB Atlas connection.

### Step 4: Start the Backend

Open another terminal in the project directory and run:

```bash
npm run server
```

The backend API runs on port `4000`.

### Step 5: Start the Frontend

Open another terminal and run:

```bash
npm run dev
```

Open the application at:

http://127.0.0.1:5173

### Step 6: Add Starter Recipes (Optional)

```bash
npm run db:seed
```

This inserts starter recipes into an empty recipe collection.

## 5. Database and RESTful API

MongoDB is used to store recipe information, user accounts, favourites, and ratings.

The backend provides RESTful API endpoints for recipe management.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/recipes` | Retrieve recipes |
| POST | `/api/recipes` | Create a recipe |
| PUT | `/api/recipes/:id` | Update a recipe |
| DELETE | `/api/recipes/:id` | Delete a recipe |
| GET | `/api/favourites` | Retrieve user favourites |
| PUT | `/api/favourites/:id` | Save a favourite |
| DELETE | `/api/favourites/:id` | Remove a favourite |

Recipe modifications require authentication, and editing or deleting a recipe requires ownership authorization.

## 6. Validation and Security

RecipeHub includes the following documented security and validation measures:

- Password hashing using salted scrypt hashes.
- Session management using HttpOnly and SameSite cookies.
- Authentication checks for protected operations.
- Recipe ownership checks for editing and deleting.
- Image upload restrictions for file type and size.
- Database-backed storage for user-specific information.

The application is configured for local development. Production deployment requires HTTPS and appropriate production security settings.

## 7. Testing

The project includes scripts for checking API functionality.

**API and CRUD testing**

```bash
npm run test:api
```

**Favourites testing**

```bash
node --env-file=backend/.env scripts/test-favourites.js
```

**Ratings and uploads testing**

```bash
node --env-file=backend/.env scripts/test-ratings-uploads.js
```

These scripts are intended to verify authentication, authorization, CRUD operations, validation, favourites, ratings, and image uploads.

## 8. Current Limitations

- The application is configured primarily for local development.
- The frontend provides a browser-based preview when the backend is unavailable; this preview does not provide MongoDB persistence.
- Uploaded images are stored locally and require separate storage configuration for production hosting.
- External images and Google Fonts may require an internet connection.
- MongoDB and locally uploaded files must be backed up separately from the GitHub source repository.

## 9. Project Documentation

The `report/` directory contains project documentation and an Entity Relationship Diagram (ERD).

The project is developed as part of the Web Application Development module and demonstrates frontend development, backend API integration, database management, authentication, and CRUD operations.

