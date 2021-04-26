# code-sample
A mini code sample based on Django Rest Framework, that contains a survey endpoint on who can vote in the US and who can't.

The survey enpoint consist of some simple input and boolean fields that could lest us know if someone is eligible too vote or not. 

The inputs are: first_name, last_name, and the boolean checkboxes are: is_us_citizen and is_registered_to_vote.

Once these informations are registered, the survey detail enpoint optionnaly allows to upload a photo of that someone these informations belong to.

To avoid file duplication confusion and for security matters, each file name that is uploaded will be replaced by a random uuid number, and will be available as that on the upload file.

Prior to run pip install -r requirements.txt to install the dependencies before testing it on a localhost.
