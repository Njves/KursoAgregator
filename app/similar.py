from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors


def str_to_vecs(text, target):
    """Функция трансформирует заданные строки в вектора"""
    # в качестве токенов для векторизации выступают буквы
    vectorizer = CountVectorizer(analyzer='char')
    vectorizer = vectorizer.fit_transform([text, target])
    text_vec, target_vec = vectorizer.toarray()[0], vectorizer.toarray()[1]
    return text_vec, target_vec

def cos_sim_vecs(vec1, vec2):
    """Функция вычисляет косинусное сходство для двух заданных векторов"""
    vec1 = vec1.reshape(1, -1)
    vec2 = vec2.reshape(1, -1)
    return cosine_similarity(vec1, vec2)[0][0]

def get_similar_course(course, courses):
    recommended_courses = []
    for i in courses:
        text_vec, target_vec = str_to_vecs(course.name, i.name)
        score = cos_sim_vecs(text_vec, target_vec)
        recommended_courses.append((score, i))
    recommended_courses.sort(key=lambda x: x[0], reverse=True)
    print(recommended_courses[0:5], 'Алло')
    recommended_courses = recommended_courses[0:5]
    recommended_courses = [i[1] for i in recommended_courses]
    return recommended_courses
