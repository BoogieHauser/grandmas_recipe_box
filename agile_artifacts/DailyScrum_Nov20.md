Attendees: Andrew, Danny, Mark, Veronica

Done:
* We have provided functionality to edit a pre-existing recipe
  * We re-use the add recipe form, but pre-populate fields with the existing recipes' information

TODO (includes notes from meeting Richard 10/22):
* Use POST request to delete objects
* Rename references to "add" recipe to "add or edit" recipe
* Refactor some functionality for easier unit tests.  E.g. rather than embedding the functionality to edit a recipe
inside a view, build a utility method for overwriting an exiting recipe that we could also write a unit test for.  Call
that utility method from both the view and the unit test
* Add a "Clean recipe data" from a form, and use this as a constructor.  This can also be unit tested
* "Code smell" issues can be an impediment