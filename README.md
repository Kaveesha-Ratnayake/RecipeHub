# RecipeHub

A warm recipe discovery and management interface built with React, Vite, Express and MongoDB.

## Run the frontend

1. Install Node.js and run `npm install` in this folder.
2. Run `npm run dev` and open http://127.0.0.1:5173.
3. Run `npm run build` for a production frontend build.

Without a running API, the frontend uses six example recipes and stores changes in this browser's localStorage. This is a design preview, not database persistence.

## Connect MongoDB

1. Start a local MongoDB instance, or use your MongoDB Atlas connection string.
2. Copy `backend/.env.example` to `backend/.env` and set MONGODB_URI. Never commit credentials.
3. Run `npm run server` in a second terminal, then reload the frontend.
4. The API supports GET/POST /api/recipes and PUT/DELETE /api/recipes/:id. With the API connected, recipes persist in MongoDB. Demo recipes are not automatically inserted into the database.

## Current scope and limitations

Search title, description and ingredients; filter categories; sort; save favourites; open recipe details; and add, edit or delete recipes with confirmation. Orange primary actions, cream backgrounds, blush pink accents and green typography are defined in frontend/style.css.

Authentication and ownership authorization are not implemented yet. The API is intended for local development only; do not expose it publicly before adding authentication. The My recipes flag currently belongs to the frontend session; API-backed ownership still needs user accounts. Photos load from Unsplash and fonts from Google Fonts, requiring internet access.

## Rubric work remaining

Implement register/login and server-side ownership checks, verify CRUD against a real MongoDB instance, prepare the ERD/report and record the demonstration. Understand and explain all submitted code during the viva.

## User accounts

Use the sidebar's Log in / Register link to open the account page. Registration requires a name, email and password of at least 8 characters. The backend must be running with MongoDB connected; there are no fake demo logins. Passwords use salted scrypt hashes. Sessions last one day and use HttpOnly, SameSite cookies; logout revokes the session. Recipe writes require authentication and edit/delete operations check the recipe owner. Use the documented 127.0.0.1 frontend address for cookies and CORS. Set NODE_ENV=production and HTTPS before production use. Existing recipes without an owner remain read-only.

The authentication and ownership implementation supersedes the earlier authentication limitation above. End-to-end database validation remains pending until MongoDB is configured.

## Local MongoDB setup (Windows)

The official MongoDB Community server is installed in ignored `.local/mongodb`; database files live in ignored `.local/data`. Keep that data folder to preserve your users and recipes. backend/.env contains the local connection string and is ignored by Git.

Start these in separate terminals from the project folder:

1. `npm run db` — local database, bound only to 127.0.0.1:27017.
2. `npm run server` — API on port 4000.
3. `npm run dev` — frontend.

Run `npm run db:seed` once for starter recipes (only inserts into an empty collection). Run `npm run test:api` for registration, sessions, authorization, CRUD and validation checks. The test removes only the records it creates. API-backed recipes and user accounts persist on disk; favourites and ratings currently remain browser-local. Local database binaries are not included in Git, so another computer needs its own MongoDB installation or Atlas URI.

## Account favourites

Favourites now use authenticated GET /api/favourites and PUT/DELETE /api/favourites/:id. MongoDB stores each user/recipe pair with a unique compound index. Only the signed-in user's favourites are returned or changed. The previous shared browser favourites are deliberately not migrated because their owner is unknown. Ratings remain browser-local. Verify account separation with `node --env-file=backend/.env scripts/test-favourites.js`.

## Account ratings and recipe photos

Ratings now persist in MongoDB with one rating per user/recipe pair. Logged-in users can set or update a 1–5 rating. Everyone can see the aggregate average and count; the signed-in user's own value is shown separately. Shared legacy browser ratings are not migrated because their owner is unknown.

Recipe forms accept either an image URL or a computer upload. Uploads require authentication, accept JPEG/PNG/WebP up to 5 MB, and are stored under ignored `.local/uploads`. Keep this directory with the database when backing up. Existing upload URLs continue to work when editing. This local setup serves uploaded photos from http://127.0.0.1:4000/uploads; production hosting needs a configured public URL or object storage.

Run `node --env-file=backend/.env scripts/test-ratings-uploads.js` to verify rating isolation, averages, repeat rating updates, login persistence, image type/size validation, and URL/uploaded image saves. The test cleans up its temporary data and uploaded file.
