# library
Basic library app


# Comments:
- About updating status of the book when it is borrowed/returned, there are different approaches.
 First I think more common is to use 'patch' method and in json payload set status '"is_borrowed": True/False'.
 But from my experience, I would say for such actions, it is better to have separate endpoint, and leave 'patch' for
 actual update of book data, like: 'title', 'author', (potentially 'borrowed_by' if someone made mistake and want to
 fix it, but with that it would be better to allow this for authenticated users, to do not have mess in system).
- I ignored adding users db table and setting relation, as here in the task description, it was about books API.
- It would be better to use async methods of SqlAlchemy for better performance
- Date validation on creation of book could be added, for date not from the future.
- Haven't added pagination yet. Will be added in next version.