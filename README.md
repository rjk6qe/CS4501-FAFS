#Free and for Sale
####Home Page : http://localhost:8000/fafs/

<br>
#Free and for Sale Web layer
## Middleware
The web layer uses a middleware file for custom authentication rather than Django's built in middleware.
In each request, the cookie will be checked for the authentication token. If found,
a request to the experience layer API will be made with the token to attempt to find the user information
associated with the token. If the token is found and is valid, the user info will be placed in
request.user.

#Free and for Sale Model API

##Table: User
###URL: /api/v1/users/
###Methods: GET, POST, PATCH

####GET
	Accepts primary key on URL, with no key specified returns all Users in DB

####POST
	Accepts: email (unique), school primary key, password

####PATCH
	Accepts: user_id (of already existing user), email, password
	NOTE: requires either email or password, not both

##Table: School
###URL: /api/schools/
###Methods: GET, POST

####GET
	Accepts primary key on URL, with no key specified returns all Schools in DB

####POST
	Accepts: name, city, state


##Table: Address
###URL: /api/addresses/
###Methods: GET, POST

####GET
	Accepts primary key on URL, with no key specified returns all Addresses in DB

####POST
	Accepts: street_number, street_name, city, state, zipcode, description

##Table: Category
###URL: /api/categories/
###Methods: GET, POST

####GET
	Accepts primary key on URL, with no key specified returns all Categories in DB

####POST
	Accepts: name, description

##Table: Product
###URL: /api/products/
###Methods: GET, POST

####GET
	Accepts primary key on URL, with no key specified returns all Products in DB

####POST
	Accepts: name, description, category_id, price, owner_id, pick_up

##Table: Transaction
###URL: /api/transactions/
###Methods: GET, POST

####GET
	Accepts primary key on URL, with no key specified returns all Transactions in DB

####POST
	Accepts: seller, buyer, product_id
