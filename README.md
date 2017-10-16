# mcPhee

#### Request should have headers:
    { "Authorization": "<auth_key>" }
    
    
Contratos dos endpoints
-------------
**/v1/person**

> **Post:**
{
		"name": "String",
		"age": int,
		"document": "String",
		"atribute" : int, [options: 1 - user, 2 - teacher, 3 - manager, 4 - admin]
		"addressName": "String",
		"addresNumber" "String",
		"addressComplement" : "String",
		"email": "String",
   		"password", "String",
		"Contact", "String"	
}
> **Response:**
> {
	> "sucess": True,
	"path" "/v1/person/<*int:id*>"
}

**/v1/person/<*int:id*>**

> **Get:**
{
		"name": "String",
		"age": int,
		"document": "String",
		"atribute" : int, [options: 1 - user, 2 - teacher, 3 - manager, 4 - admin]
		"addressName": "String",
		"addresNumber" "String",
		"addressComplement" : "String",
		"email": "String",
		"contact", "String"
		"schools" : [ { "school_name": "String", "school_attribute" : int} ]
		"students": [ { "name": "str", "age": int, "obs": "string", "class": "str", "schoolID": int, "schoolName": str} ]
}

**/v1/student**

> **Post:**
{
		"name": "String",
		"age": int,
		"obs": "String",
		"documents": [list of strings]	
}
> **Response:**
> {
	> "sucess": True,
	"path" "/v1/student/<*int:id*>"
}
