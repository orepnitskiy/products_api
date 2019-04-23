# products_api
This is a project that realize API of grocery store. For correct start of application it's mandatory to start and apply all migrations. Technical description of project you can see below:

(POST) /api/v1/goods/ - create product in grocery store
Format of request: application/json
Example of request: 
{
  "Authorization":"Base dXNlcjp1c2Vy"
  "title": "Cheese\"Russian\"",
  "description": "Very delicious cheese, almost like Italian.",
  "price": 100
}
Limitations:
- You can access only if you user with is_staff flag
- All fields are mandatory 
- title - not empty string, not longer than 64 symbols
- description - not empty string, not longer than 1024 symbols
- price - not empty string ( that can be transferred to int) or int, values from 1 to 1000000
Possible answers:
- 201 - product successfully saved
  Example of answer:
    {"id": 112}
- 400 - request didn't go through validation

(POST) /api/v1/goods/:id/reviews/ - create review to product, where :id - id of product.
Format of request: application/json
Example of request:
{
  "text": "Best. Cheese. Ever.",
  "grade": 9
}
Limitations:
- All fields are mandatory
- text - not empty string, not longer than 1024 symbols
- grade - not empty string (that can be transferred to int type) or, values from 1 to 10
Possible answers:
- 201 - review successfully saved
  Example of answer:
    {"id": 95}
- 400 - request didn't validate
- 404 - no product with that id.

(GET) /api/v1/goods/:id/ - получить информацию о товаре, включая 5 последних отзывов.
Format of request: application/json
Limitations:
- If there's more than 5 reviews - return 5 latest. Sort by id of review.
- If there's 5 reviews - return all.
Possible answers:
- 200 - OK
  Example of request:
  {      
    "id": 112,
    "title": "Cheese \"Russian\"",
    "description": "Very delicious cheese.",
    "price": 100,
    "reviews": [{ 
      "id": 95,
      "text": "Best. Cheese. Ever.",
      "grade": 9
    }]    
  }
- 404 - There is no product with that id.
