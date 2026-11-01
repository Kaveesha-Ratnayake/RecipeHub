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

- Node.js 22 or newer and npm
- MongoDB Community Server or MongoDB Atlas
- A modern web browser

### Step 1: Clone and Install Dependencies

```bash
git clone https://github.com/Kaveesha-Ratnayake/RecipeHub.git
cd RecipeHub
```

Then install dependencies:

Open a terminal in the RecipeHub project directory and run:

```bash
npm install
```

### Step 2: Configure MongoDB

Copy `backend/.env.example` to `backend/.env` and configure the `MONGODB_URI` connection string.

For a local database, use:

```env
PORT=4000
MONGODB_URI=mongodb://127.0.0.1:27017/recipehub
```

On Windows PowerShell, copy the example with `Copy-Item backend/.env.example backend/.env`.
Never upload `.env` files containing database credentials to GitHub.

### Step 3: Start MongoDB

Choose one option:

- **Installed MongoDB Community Server:** start its MongoDB Windows service. If you installed only the binaries, create a data folder and run `mongod --dbpath <absolute-data-folder> --bind_ip 127.0.0.1 --port 27017` using your mongod executable. Keep that terminal open.
- **Project-local Windows ZIP installation:** extract MongoDB Community Server so that `.local/mongodb/<extracted-folder>/bin/mongod.exe` exists, then run `npm run db`. This creates `.local/data`. The binaries and data are ignored by Git, so a fresh clone does not include them. **Do not run this command if a MongoDB service already uses port 27017.**
- **MongoDB Atlas:** set your Atlas connection string in `backend/.env`, configure access for your computer, and skip the local database command.

Keep MongoDB running while using the application.

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

Keep the backend and frontend terminals open. The frontend uses port 5173 and stops with an error if the port is already occupied; use the existing running instance instead of launching duplicates.

Open the application at:

http://127.0.0.1:5173

### Step 6: Add Starter Recipes (Optional)

```bash
npm run db:seed
```

This inserts starter recipes into an empty recipe collection. Your existing local accounts, recipes and uploaded files are not included in a GitHub clone. Register a new account on a new installation.

If login shows "account service is unavailable", check that MongoDB and `npm run server` are running. Use `http://127.0.0.1:5173` consistently. This repository is source code, not a hosted application; frontend API addresses currently target the local computer.

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


### Additional setup notes

`npm run db` can use the project-local Windows ZIP binaries, `mongod` on PATH, or an executable specified by the `MONGOD_PATH` environment variable. If port 27017 is already in use, it prints a message rather than launching a duplicate server. This does not prove the process on that port is MongoDB; the backend connection verifies that.

Convenient checks: `npm run test:api`, `npm run test:favourites`, and `npm run test:ratings` (run sequentially while MongoDB and the backend are running).


