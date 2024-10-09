# __Political Sentiment Dashboard__
#### __ML Experts Internship Evaluation Task: Sarin Sthapit__
##
### __Approach__
##### 1. __Fetching News Articles and Top 5 Hot Topics__
###### Two APIs, News API and GNews API were used to extract news articles based on the names of cities that were entered by the user. A URL is constructed to query News API for articles related to the specified city. Then, similar topics are filtered out, and unique topics are retained using _SequenceMatcher_. Count occurences of keywords are used to find the most common phrases for specified number of topics.
##### N-Grams mechanism is used to extract the hot topics while preserbing the context of words by considering them in combination rather than treating them as isolated units. This also helps to provide a richer representation of the text data. 
##
##### 2. __Extracting Discussion from Reddit__ 
##
##### 3. __Summarization of Discussions__
##
##### 4. __Sentiment Analysis__
##
##### 5. __Frontend Development using Flask__
#
#
### __Installation Instructions__
###### 1. First of all, clone the repository: _git clone https://github.com/SarinSthapit/MLE-Intern-Task.git_ 
###### 2. Enter into the local repository: _cd MLE-Intern-Task_
###### 3. Create a Conda environment: _conda create --name new_env python=3.9.18_
###### 4. Activate the Conda environment: _conda activate new_env_
###### 5. Install dependencies: _conda env create -f environment.yml_ OR _pip istall -r requirements.txt_
###### 6. Run the command in terminal: _python -m src.app_
