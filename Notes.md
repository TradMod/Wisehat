wisehat phases plan (on-the-go)

phase 1 
prompt template which tells the system about flaggings
- import the model -
- basic ai model chat -
- add a template with a system prompt -
- take user input -
- full prompt to the model and fetch the response -
- memory of the chat -

phase 2 
website page loader and input to the prompt
- Website Page loader -
- website pages number check (immunefi & hackenproof) -
- take user input and based on that page search/fetch -
- add those page details into the prompt - 
 
phase 3
prepare the bbp rules analyzer template
- write importent things needed in evaluating BBPs
- discuss with llms about the system prompt
- refine it using the online resources
- write the BBPs rules edge cases
- refine the final prompt
- Test it using 10-25 programs 

-> Gotta store the results in a file and once the same program is called again, just pass the previous results (esp if only 30days passed or the updatedAt is not changed), this will help reduce the compute and time and increase the speed of the application. That can also be the displayed on the frontend.
qq, how does this work online, will the other users will use my device storage or i will need any db? maybe good time to integrate postgresql