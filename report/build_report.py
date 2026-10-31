from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from pathlib import Path

ROOT=Path(__file__).resolve().parent
d=Document(); s=d.sections[0]
s.page_width=Inches(8.27); s.page_height=Inches(11.69)
s.top_margin=s.bottom_margin=Inches(.72)
s.left_margin=s.right_margin=Inches(.8)
for name in ['Normal','Title','Subtitle','Heading 1','Heading 2','Caption']:
 st=d.styles[name]; st.font.name='Calibri'; st.font.color.rgb=RGBColor(0,0,0)
d.styles['Normal'].font.size=Pt(11)
d.styles['Normal'].paragraph_format.space_after=Pt(7)
d.styles['Normal'].paragraph_format.line_spacing=1.12
d.styles['Title'].font.size=Pt(30)
d.styles['Heading 1'].font.size=Pt(19)
d.styles['Heading 2'].font.size=Pt(13)
f=s.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.RIGHT
f.add_run('RecipeHub  |  ')
field=OxmlElement('w:fldSimple'); field.set(qn('w:instr'),'PAGE'); f._p.append(field)

def p(t='',style=None): return d.add_paragraph(t,style)
def h(t): d.add_heading(t,2)
def page(t): d.add_page_break(); d.add_heading(t,1)
def table(headers, rows, widths=None):
 t=d.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER
 t.autofit=False
 if widths:
  for c,w in zip(t.columns,widths): c.width=Inches(w)
 for c,x in zip(t.rows[0].cells,headers): c.text=x
 for row in rows:
  for c,x in zip(t.add_row().cells,row): c.text=x
 for i,row in enumerate(t.rows):
  for j,c in enumerate(row.cells):
   if widths: c.width=Inches(widths[j])
   c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   pr=c._tc.get_or_add_tcPr()
   sh=OxmlElement('w:shd'); sh.set(qn('w:fill'),'E5EBF0' if i==0 else ('F7F9FB' if i%2==0 else 'FFFFFF')); pr.append(sh)
   borders=OxmlElement('w:tcBorders')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge); el.set(qn('w:val'),'single'); el.set(qn('w:sz'),'4'); el.set(qn('w:color'),'D9D9D9'); borders.append(el)
   pr.append(borders)
   margins=OxmlElement('w:tcMar')
   for edge in ['top','left','bottom','right']:
    el=OxmlElement('w:'+edge); el.set(qn('w:w'),'85'); el.set(qn('w:type'),'dxa'); margins.append(el)
   pr.append(margins)
   for para in c.paragraphs:
    para.paragraph_format.space_after=Pt(2); para.paragraph_format.line_spacing=1.03
    for run in para.runs: run.font.size=Pt(9.5); run.bold=i==0
  no=OxmlElement('w:cantSplit'); row._tr.get_or_add_trPr().append(no)
 rep=OxmlElement('w:tblHeader'); t.rows[0]._tr.get_or_add_trPr().append(rep)
 p('')
 return t

p('RecipeHub', 'Title')
p('Full Stack Recipe Management and Sharing Application','Subtitle')
p('Web Application Development Mini Project Report')
p('')
for label,value in [('Student name','[Enter your full name]'),('Index number','[Enter your index number]'),('Module code','[Confirm EC4307 or EE4207]'),('Degree and institution','[Enter degree and institution]'),('Lecturer','[Enter lecturer name]'),('Submission date','31 October 2026'),('GitHub repository','[Insert repository URL]')]:
 para=p(); para.add_run(label+'\n').bold=True; para.add_run(value)
h('Abstract')
p('RecipeHub is a full stack web application for discovering, creating and managing cooking recipes. The application combines a React interface, an Express REST API and MongoDB storage. Visitors can browse recipes, search ingredients and filter categories. Registered users can manage their own recipes, save favourites, submit ratings and upload recipe photographs. Authentication uses cookie based sessions, and the API checks ownership before editing or deleting recipes. This report explains the application requirements, architecture, database structure, CRUD implementation, validation and verification approach.')

page('1 Introduction and Requirements')
h('Problem statement')
p('Recipes are often scattered across websites, messages and personal notes. This makes it difficult to retrieve a recipe, organise ingredients or maintain an updated personal collection. RecipeHub provides one interface for storing structured recipes and finding cooking ideas through search and category filters.')
h('Project objectives')
for x in ['Implement complete create, read, update and delete operations for recipes with persistent database storage.','Separate public browsing from authenticated account actions and restrict recipe changes to the owner.','Support discovery through keyword search, category filtering and sorting.','Provide account specific favourites, recipe ratings and photographs.','Build a consistent interface that adapts to smaller screens and provides useful validation feedback.']: p(x,'List Bullet')
h('Users and application scope')
p('A visitor can browse recipe cards, open recipe details and view aggregate ratings. A registered user can additionally create recipes, manage owned recipes, save favourites and rate recipes. The implementation does not include an administrator dashboard, payments, meal planning or a nutrition calculation service.')
table(['Requirement','Implemented behaviour'],[
('Recipe management','Title, category, time, servings, description, ingredients, instructions and image.'),
('Account management','Registration, login, session lookup and logout.'),
('Discovery','Search title, description and ingredients; filter by category; sort by time, name or newest.'),
('Personal collection','My recipes and authenticated favourites.'),
('Quality requirements','Persistent storage, ownership checks, input validation and responsive CSS.')],[1.45,5.1])
p('The recipe entity is the main CRUD entity. Favourites and ratings extend the core application without replacing the requirement for persistent recipe CRUD.')

page('2 Technologies and System Architecture')
p('RecipeHub follows a three tier structure. The browser renders the user interface, the Express service validates requests and applies access rules, and MongoDB stores application records. Mongoose defines schemas and performs database operations.')
table(['Layer or tool','Role'],[('React 19','Components, state management, forms and interactive navigation.'),('Vite 6','Frontend development server and production build.'),('Express 5 and Node.js','HTTP routing, JSON responses, authentication and upload handling.'),('MongoDB and Mongoose 8','Persistent documents, schema validation, references and indexes.'),('CSS and Lucide React','Responsive layouts, visual styling and interface icons.'),('Git and GitHub','Version control and submission repository.')],[1.65,4.9])
h('Request flow')
p('Browser with React  →  HTTP REST API with Express  →  Mongoose  →  MongoDB')
p('For example, creating a recipe sends JSON to POST /api/recipes with the session cookie. Authentication resolves the current account, the server selects allowed recipe fields and assigns the owner, and Mongoose validates and stores the document. The API returns the saved recipe so the interface can refresh its state.')
h('Project organisation')
table(['Location','Responsibility'],[('frontend/src.jsx','Application views, recipe forms, discovery controls and API requests.'),('frontend/AuthPage.jsx','Login and registration interface.'),('frontend/RecipePhoto.jsx','Recipe photograph presentation.'),('frontend/style.css','Shared styles and responsive breakpoints.'),('backend/server.js','Server startup, recipe schema and CRUD endpoints.'),('backend/auth.js','User records, password hashing, sessions and authentication.'),('backend/favourites.js and ratings.js','Account favourites and rating persistence.'),('backend/uploads.js','Authenticated image upload and static image serving.'),('scripts/','Database startup, seed data and integration tests.')],[2.35,4.2])
p('The local frontend uses 127.0.0.1:5173 and the API uses 127.0.0.1:4000. Cross origin requests include credentials and are restricted to the configured local frontend origins.')

page('3 Database Design')
p('MongoDB stores users, sessions, recipes, favourites and ratings as separate collections. ObjectId values identify records. References connect account activity to users and recipes; these relationships are enforced through application logic rather than relational foreign key constraints.')
table(['Collection','Main fields and constraints'],[
('users','_id; name required, maximum 60 characters; unique email; passwordHash; salt.'),
('sessions','_id; unique digest; user ObjectId; expires date with TTL index.'),
('recipes','_id; owner ObjectId; title required, maximum 120; category enum; time 1–1440; servings 1–100; description maximum 500; image maximum 2000; ingredients and instructions arrays; timestamps.'),
('favourites','_id; user and recipe ObjectIds; timestamps; unique compound index on user and recipe.'),
('ratings','_id; user and recipe ObjectIds; value 1–5; unique compound index on user and recipe.')],[1.25,5.3])
h('Entity relationships')
table(['Parent','Cardinality','Related entity','Meaning'],[('User','1 to many','Recipe','A user can own multiple recipes.'),('User','1 to many','Session','A user can have multiple active sessions.'),('User','1 to many','Favourite','A user can save multiple recipes.'),('Recipe','1 to many','Favourite','A recipe can be saved by many users.'),('User','1 to many','Rating','A user can rate multiple recipes.'),('Recipe','1 to many','Rating','A recipe can receive ratings from many users.')],[.85,1,1.05,3.65])
p('User → Favourite ← Recipe and User → Rating ← Recipe represent two many to many relationships through association collections. The compound indexes prevent duplicate favourites and multiple rating records for the same account and recipe. A repeat rating updates the existing value.')
h('Storage decisions')
p('Ingredients and instructions are embedded string arrays because they belong to one recipe and are normally loaded together. Categories use an enum containing Breakfast, Lunch, Dinner, Dessert and Drinks. Image bytes are stored in .local/uploads; the recipe document stores the image URL. Passwords are salted and hashed, and only a token digest is stored for each session.')
p('Deleting a recipe currently does not cascade deletion to every related favourite or rating. Favourite retrieval hides missing recipe references. Explicit cleanup of associated records is a future improvement.')

page('4 Recipe CRUD and REST API')
table(['Operation','Endpoint','Behaviour'],[('Create','POST /api/recipes','Requires login; stores allowed fields and assigns the current user as owner; returns 201.'),('Read','GET /api/recipes','Public list with author names; the frontend opens recipe details and performs discovery filtering.'),('Update','PUT /api/recipes/:id','Requires login and matching owner; validates changed fields and returns the updated recipe.'),('Delete','DELETE /api/recipes/:id','Requires login and matching owner; removes the record and returns 204.')],[.7,2,3.85])
h('Create')
p('A signed in user opens Add recipe and enters the recipe details. The frontend converts cooking time and servings to numbers and converts ingredients and instructions into arrays using nonempty lines. If a photograph is selected, the file is uploaded before the recipe request. The server assigns ownership from the authenticated account rather than accepting an owner supplied by the browser.')
h('Read')
p('The API retrieves recipes in descending creation order and includes the owner name for display. The frontend renders recipe cards and a detail view. Search checks title, description and ingredients without case sensitivity. Category filters and sorting are performed on the loaded recipes in the browser. My recipes compares each recipe owner with the signed in account.')
h('Update and delete')
p('Editing opens the existing recipe data in the form. The API matches both the requested recipe ID and the authenticated owner when applying updates. Deletion uses a confirmation interface before making the API request. A missing recipe or one not owned by the account returns 404, and requests without a valid session return 401.')
h('Additional API capabilities')
table(['Endpoint group','Purpose'],[('/api/auth/register, /login, /me, /logout','Create accounts, authenticate, restore session state and revoke sessions.'),('/api/favourites and /api/favourites/:id','Read personal favourites; add with PUT and remove with DELETE.'),('/api/ratings, /mine and /:id','Read public aggregates, retrieve own values and set ratings.'),('POST /api/uploads','Upload an authenticated JPEG, PNG or WebP image.')],[3,3.55])
p('When the API is unavailable, the frontend can show demonstration recipes using browser storage. This preview mode is separate from MongoDB persistence and must not be used as evidence of database CRUD in the demonstration.')

page('5 Validation Security and Error Handling')
h('Account authentication')
p('Registration accepts a trimmed name, normalised email address and a password of 8 to 128 characters. Email uniqueness prevents duplicate accounts. Passwords use scrypt with a random salt. Login verifies the supplied password using a timing safe comparison. A random session token is sent in an HttpOnly, SameSite Strict cookie, while the database holds its SHA 256 digest and expiry time.')
p('Sessions last one day. Authentication checks the expiry on each protected request, and logout deletes the matching session and clears its cookie. In production mode the cookie also uses Secure. Authentication POST requests have a simple in memory limit of 20 attempts per IP per minute.')
table(['Input or action','Validation and response'],[('Account registration','Valid email, name length and password length; duplicate email returns 409.'),('Recipe fields','Required title and category; category enum; numeric ranges; nonempty ingredient and instruction arrays.'),('Recipe identifiers','Invalid identifiers are handled as a client error; missing or inaccessible recipes return 404.'),('Ownership','Update and delete queries include owner equal to the authenticated user.'),('Rating','Only whole numbers from 1 to 5; requires login and an existing recipe.'),('Image upload','Login required; JPEG, PNG or WebP; file signature check; maximum 5 MB.'),('Unexpected failure','A generic server error response avoids exposing internal exception details.')],[1.4,5.15])
h('Frontend feedback')
p('Forms show validation messages and API errors. Recipe saving tracks a pending state, and success messages confirm saves and deletion. Favourites and ratings report failed requests so the interface does not silently claim that a change was stored. Photo URL input is checked in the frontend for supported URL prefixes.')
h('Current security limits')
p('The application is configured for local development. Public deployment requires HTTPS, deployment specific origins and public upload URLs. Additional hardening should include robust distributed rate limiting, more complete payload type validation and production monitoring. Uploaded files are validated by signature, but image decoding and re encoding would provide stronger content validation.')

page('6 User Interface and Responsiveness')
p('The interface uses cream backgrounds, green text, orange primary actions and pink accents. Recipe cards present photographs and concise cooking information. Home and discovery views provide search and category controls, while the sidebar gives access to personal recipes and favourites after login.')
h('Primary user journey')
p('A visitor browses recipes and opens a detail view. To contribute, the visitor registers or logs in, opens Add recipe and submits a completed form. The saved recipe appears in My recipes, where its owner can edit or delete it. Favourites and ratings connect the discovery experience to the user account.')
h('Responsive behaviour')
p('CSS media queries adjust the layout for narrower screens. Recipe grids reduce their column count, search controls wrap, the sidebar uses a mobile menu, and the authentication page changes to a single column. Inputs and navigation actions have dedicated mobile sizing. Keyboard focus styles and accessible labels are present for key controls.')
h('Figure 1 Desktop recipe discovery')
p('[Insert a screenshot of the running desktop Home or Discover view here.]')
p('Caption: Recipe cards, search, category filtering and sorting in the desktop interface.','Caption')
p('\n')
h('Figure 2 Recipe form or mobile interface')
p('[Insert a screenshot of Add or Edit recipe, or the application at a mobile screen width.]')
p('Caption: Replace this caption to describe the screenshot selected.','Caption')
h('Interface verification')
p('Before submission, check that the screenshots show the database connected application, that text and controls remain readable on a narrow screen, and that recipe forms and confirmation dialogs are fully visible. Use the live interface to demonstrate account actions and persistent CRUD.')

page('7 Testing and Verification')
p('The repository includes integration tests for the API, favourites, ratings and uploads. They create temporary test accounts and records, assert expected responses and remove their test data. The table below records expected outcomes; actual results must be entered after running the tests on the submission version.')
table(['Test','Expected outcome','Actual result'],[('Registration and login','Valid registration 201; correct login 200; wrong password 401.','[Enter result]'),('Recipe create and read','Logged in create 201; new record appears in GET list with correct owner.','[Enter result]'),('Recipe update','Changed time is returned; invalid negative time returns 400.','[Enter result]'),('Recipe delete','Deletion returns 204 and record is no longer in the list.','[Enter result]'),('Authentication and logout','Unauthenticated write 401; revoked session cannot access /auth/me.','[Enter result]'),('Favourite isolation','User A saves a favourite; user B cannot see or remove it.','[Enter result]'),('Rating update and average','Ratings 5 and 3 average 4; changing 5 to 1 produces 2 without an extra vote.','[Enter result]'),('Upload validation','No login 401; invalid image 400; oversized file 413; valid PNG 201.','[Enter result]'),('Image retrieval and saving','Uploaded image is retrievable and both URL and uploaded paths can be saved.','[Enter result]'),('Manual ownership check','User B cannot edit or delete a recipe created by user A.','[Enter result]'),('Manual persistence and mobile','Data remains after restart; forms and navigation work at mobile width.','[Enter result]')],[1.35,3.95,1.25])
h('Commands for repeatable verification')
for x in ['npm run test:api','node --env-file=backend/.env scripts/test-favourites.js','node --env-file=backend/.env scripts/test-ratings-uploads.js','npm run build']: p(x)
p('Run the integration tests with MongoDB and the API already running. Record the execution date and any failures, then repeat affected checks after fixes. Browser interaction, cross account ownership and restart persistence should also be demonstrated manually; the API scripts do not establish complete browser or usability coverage.')

page('8 Setup Conclusion and References')
h('Installation and local execution')
for x in ['Install Node.js and MongoDB Community Server, or configure a MongoDB Atlas connection. Clone the submitted GitHub repository and run npm install in its root.','Copy backend/.env.example to backend/.env and set MONGODB_URI. Keep credentials out of version control.','Start MongoDB. On this workstation npm run db starts the locally provisioned server; other computers need their own MongoDB installation or Atlas service.','In separate terminals run npm run server and npm run dev. Open http://127.0.0.1:5173.','Optionally run npm run db:seed against an empty recipe collection to insert starter recipes. Register an account to test protected actions.','Run the integration tests and npm run build. Back up both MongoDB data and .local/uploads to retain recipe photographs.']: p(x,'List Number')
h('Limitations and future work')
p('The current application targets local demonstration and has no public deployment configuration. Search and filtering load the full recipe collection, so pagination and database queries would improve scalability. Future work includes cleanup of references when recipes are deleted, upload lifecycle management, account recovery, automated browser tests and stronger server validation. Ratings and favourites are stored per account in MongoDB; browser demonstration storage is a separate fallback.')
h('Conclusion')
p('RecipeHub applies full stack web development to a practical recipe management task. React handles browsing and forms, Express applies authentication and CRUD rules, and MongoDB stores the main entity and account activity. Favourites, ratings and image uploads extend the core workflow. Final evaluation should demonstrate the connected database, owner restricted editing, validation feedback and the application at desktop and mobile sizes.')
h('References')
for x in ['Mini Project Evaluation Rubric COM, supplied module assessment document, dated 14 October 2026.','RecipeHub source code and README, submitted project repository. [Insert GitHub repository URL.]','React documentation: https://react.dev/','Express documentation: https://expressjs.com/','Mongoose documentation: https://mongoosejs.com/docs/','MongoDB documentation: https://www.mongodb.com/docs/','Node.js crypto documentation: https://nodejs.org/api/crypto.html']: p(x)
d.core_properties.title='RecipeHub Mini Project Report'
d.core_properties.subject='Full stack recipe management application'
d.core_properties.author=''
d.save(ROOT/'RecipeHub_Report_Editable.docx')
print(ROOT/'RecipeHub_Report_Editable.docx')
