#Free and for Sale API

##Table: User
###URL: /api/users/
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

