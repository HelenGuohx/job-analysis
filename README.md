# Job Analysis
Job Analysis is an analytical tool to discover the information from job data 

### Our functions

- Providing keywords about a specific position
- Sorting job posts by the relavance to users' profession skills from high to low


## Function 1: providing keywords about a specific position

Introduction:


### Approaches to obtain clean keywords
- Extract the text of \<li> tag within job description element
- Filter keywords by 'NOUN' or 'VERB' which is a token's POS (part-of-speech) only for unigram
- Define stop words such as 'experience, job, work' 