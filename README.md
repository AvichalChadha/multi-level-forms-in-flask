# multi-level-forms-in-flask
This is a multi-level form created using flask.(No javascript)


##About the multi-page form

=> I have coded it using sessions in flask

=> All the data is being stored in the sessions before sending it to the database.All the data is being stored in the sessions before sending it to the database.

=>User can't just skip to 2nd or 3rd page of the form untill he has filled the previous page.

=> If you try to reload the web page that you are redirected to after submitting the form,the use will be told to fill the form again. Hence the session is popped out. This is done so that the user doesn't spam the database by just reloading.










