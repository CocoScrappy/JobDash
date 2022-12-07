from sklearn.metrics.pairwise import cosine_similarity
import html2text
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import requests
# from . import models

# nltk.download('punkt')

# resume = """<p>ALI NEHME, Ph.D.</p>
#  <p>Tel: +1 (438) 334-1206 | Email: <a href="mailto:ali.hassan.nehme@gmail.com" target="_self">ali.nehme@biomedinfo.co</a> | Address: Brossard (Quebec), Canada</p>
#  <p>GitHub: github.com/nehmea LinkedIn: www.linkedin.com/in/ali-nehme1</p>
#  <h1>Profile</h1>
#  <p>A Full Stack Developer with a passion for developing scalable and complex applications. Backed up with data science experience and a diverse set of soft skills from 10 years of scientific research. Always strive to bring 100% to the work I do. I look forward to joining a creative and hard-working environment that helps me grow my technical skills while moving projects to success.</p>
#  <p>Available for an internship/work starting from January 3rd, 2023.</p>
#  <p>Technical Skills</p>
#  <p>Frontend: JavaScript, React, ThymeLeaf, HTML, CSS, XAML, Bootstrap</p>
#  <p>Backend: Java, Node.js, C#, .NET Core, PHP, Python, Socket IO, R, Ubuntu</p>
#  <p>Frameworks: Spring Boot, WPF</p>
#  <p>Database: MySQL, MSSQL, PhPMyAdmin</p>
#  <p>Hosting: AWS EC2, AWS RDS, XAMPP</p>"""


# job_description = """
# You will be responsible for writing clean, robust software code using best practice development in an agile environment as well as have the opportunity to be part of the transition of our applications to the cloud.If you feel you are the right fit for this role please email me your word resume to aaron.lail@randstad.ca AdvantagesWe advance the mining industry towards a safer, more efficient, and more sustainable future through the delivery of innovative software solutions and deep domain mining expertise. Guided by our underlying principles of mining expertise, innovation, and sustainability, we strive to create safer, more efficient and more sustainable operations for our mining customers.ResponsibilitiesKey Responsibilities• Design and produce high quality software code• Assist with the integration of new features• Support development by undertaking analysis, testing, and troubleshooting• Adhere to software quality standards and corporate objectives• Contribute towards the software development roadmap• Document and support our clients software solutionsQualificationsAbout You• Strong professional experience of 5 years or more in C++ is required• Experience in C#, .NET, and SQL development highly regardedSummaryIf you feel you are the right fit for this role please email me your word resume to aaron.lail@randstad.ca Randstad Canada is committed to fostering a workforce reflective of all peoples of Canada. As a result, we are committed to developing and implementing strategies to increase the equity, diversity and inclusion within the workplace by examining our internal policies, practices, and systems throughout the entire lifecycle of our workforce, including its recruitment, retention and advancement for all employees. In addition to our deep commitment to respecting human rights, we are dedicated to positive actions to affect change to ensure everyone has full participation in the workforce free from any barriers, systemic or otherwise, especially equity-seeking groups who are usually underrepresented in Canada's workforce, including those who identify as women or non-binary/gender non-conforming; Indigenous or Aboriginal Peoples; persons with disabilities (visible or invisible) and; members of visible minorities, racialized groups and the LGBTQ2+ community.Randstad Canada is committed to creating and maintaining an inclusive and accessible workplace for all its candidates and employees by supporting their accessibility and accommodation needs throughout the employment lifecycle. We ask that all job applications please identify any accommodation requirements by sending an email to accessibility@randstad.ca to ensure their ability to fully participate in the interview process."""


def extract_text_from_docx(html):
    h = html2text.HTML2Text()
    h.ignore_links = True
    txt = h.handle(html)
    if txt:
        return txt.replace('\t', ' ')
    return None


def get_matching_skills(input_text, skills):
    stop_words = set(nltk.corpus.stopwords.words('english'))
    word_tokens = nltk.tokenize.word_tokenize(input_text)

    # remove the stop words
    filtered_tokens = [w for w in word_tokens if w not in stop_words]

    # remove the punctuation
    filtered_tokens = [w for w in word_tokens if w.isalpha()]

    # generate bigrams and trigrams (such as artificial intelligence)
    bigrams_trigrams = list(
        map(' '.join, nltk.everygrams(filtered_tokens, 2, 2)))

    # we create a set to keep the results in.
    found_skills = set()

    # we search for each token in our skills
    for token in filtered_tokens:
        if token.lower() in skills:
            found_skills.add(token.lower())

    # we search for each bigram and trigram in our skills database
    for ngram in bigrams_trigrams:
        if ngram.lower() in skills:
            found_skills.add(ngram.lower())

    return found_skills


def get_text_matching_matrix(text):
    nltk.download('stopwords')
    stop_words = set(nltk.corpus.stopwords.words('english'))
    cv = CountVectorizer(stop_words=stop_words)
    count_matrix = cv.fit_transform(text)

    return count_matrix


def get_text_matching_score(text):
    nltk.download('stopwords')
    stop_words = set(nltk.corpus.stopwords.words('english'))
    cv = CountVectorizer(stop_words=stop_words)
    count_matrix = cv.fit_transform(text)

    # get the match percentage
    matchPercentage = cosine_similarity(count_matrix)[0][1] * 100
    matchPercentage = round(matchPercentage, 2)  # round to two decimal

    return {'count_matrix': count_matrix, 'matchPercentage': matchPercentage}


# resume_text = extract_text_from_docx(resume)
# job_description_text = extract_text_from_docx(job_description)

# text = [job_description_text, resume_text]

# matching_score = get_text_matching_score(text)

# print(matching_score['count_matrix'])
# print(matching_score['matchPercentage'])

# # Print the similarity scores
# print("\nSimilarity Scores:")
# print(cosine_similarity(matching_score['count_matrix']))

# print("Your resume matches about " +
#       str(matching_score['matchPercentage']) + "% of the job description.")

# db_skills = Skill.objects.all()
# required_skills = extract_skills(job_description_text, db_skills)
# matching_skills = get_matching_skills(resume_text, required_skills)
# matching_score = len(matching_skills)/len(required_skills)
# print(round(matching_score, 2))
