Attendees: Danny, Andrew

Impediments:
* Review of rubric

Done:
* Added functionality to crud_get_recipes and views.py to allow for search by recipe title
* Added UI search elements to browse recipe page to allow for search by recipe title
* Added testing for crud_get_recipes when specifying tags or search queries
* Grandma no longer has an opaque background
* Improved behavior when user requests a recipe that does not exist
* Added login, register, and logout routes
* Added controls that users must be logged in to create recipes
* Added controls that users can only see recipes they submitted or recipes marked public (currently impossible)
* Added controls that users can only edit recipes they submitted
* Added controls that users can only delete recipes they submitted
* Significantly reworked tests to account for authentication

TODO:
* Introduce additional tests
* Use POST request to delete objects
* Rename references to "add" recipe to "add or edit" recipe
* More specific users in user stories
* Conditionally hide "Add Recipe", "Edit Recipe", and "Delete Recipe" buttons
* Allow for public recipes