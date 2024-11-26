Attendees: Danny, Andrew

Recapped work from last working session.

Done:
* The functionality to edit recipes now appropriately overwrites a previous object, rather than adding a new object
* The functionality to edit recipes now pre-populates the tag field with values from its previous submission
* The add/edit recipe page shows common tags (which are links that do nothing)
* Tags now visible on the view recipe page (which are links that do nothing)
* 4 additional unit tests added (total now is 16) - Breaking down methods to get lists of ingredients/instructions as suggested by Richard (+2) and similar methods for tags (+2)

TODO:
* Prepare for stakeholder meeting on 12/1 (Confirm date!)
* Have a total of 20 unit tests by end of sprint
* Use POST request to delete objects
* Rename references to "add" recipe to "add or edit" recipe
* Refactor some functionality for easier unit tests.  E.g. rather than embedding the functionality to edit a recipe
inside a view, build a utility method for overwriting an exiting recipe that we could also write a unit test for.  Call
that utility method from both the view and the unit test
* Add a "Clean recipe data" from a form, and use this as a constructor.  This can also be unit tested
* "Code smell" issues can be an impediment