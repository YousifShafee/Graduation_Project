import pandas as pd
import scipy
from scipy.stats import pearsonr
from Api.models import Books


def euclidean_score(train_user, test_user):
    user_list = []
    second_user = []
    for i in test_user:
        for j in train_user:
            if int(i[1]) == int(j[1]):
                user_list.append(int(i[2]))
                second_user.append(int(j[2]))
    return round(pearsonr(scipy.array(user_list), scipy.array(second_user))[0], 2)


def item_item(current_item):

    data = pd.DataFrame(list(Books.data(1)))
    data = data.convert_objects(convert_numeric=True)
    item = pd.DataFrame(list(Books.item(1)))

    item['book_id'] = item['book_id'].fillna(0).astype(int)
    r = len(data)
    user_train = (data.sort_values('book_id'))[:r]
    user_test = (data.sort_values('book_id'))[:r]
    end = user_train['book_id'].max()

    user_test = user_test[(user_test['book_id'] == current_item)]

    user_train = user_train.as_matrix(columns=['book_id', 'user_id', 'rating'])
    user_test = user_test.as_matrix(columns=['book_id', 'user_id', 'rating'])
    users_list = []

    for i in range(1, end + 1):
        li = []
        for j in range(0, len(user_train)):
            if user_train[j][0] == i:
                li.append(user_train[j])
            else:
                break
        user_train = user_train[j:]
        users_list.append(li)

    score_list = []
    for i in range(0, len(users_list)):
        score_list.append([i + 1, euclidean_score(users_list[i], user_test)])

    score = pd.DataFrame(score_list, columns=['book_id', 'Similarity'])
    score = score[score.Similarity != 1.00]

    score = score.sort_values(by='Similarity', ascending=False)
    score_matrix = score.as_matrix()

    int(score_matrix[0][0])
    user = int(score_matrix[0][0])
    common_list = []
    full_list = []
    for i in user_test:
        for j in users_list[user - 1]:
            if int(i[1]) == int(j[1]):
                common_list.append(int(j[1]))
            full_list.append(j[1])

    common_list = set(common_list)
    full_list = set(full_list)
    recommendation = full_list.difference(common_list)
    item_list = (((pd.merge(item, data).sort_values(by='book_id').groupby('book_name'))))[
        'book_id', 'book_name', 'rating']
    item_list = item_list.mean()
    item_list['book_name'] = item_list.index
    item_list = item_list.as_matrix()

    recommendation_list = []
    for i in recommendation:
        recommendation_list.append(item_list[i - 1])

    recommendation = (pd.DataFrame(recommendation_list, columns=['book_id', 'mean_rating', 'book_name'])).sort_values(
        by='mean_rating', ascending=False)
    results = recommendation.to_dict(orient='records')
    for i in results:
        img = Books.objects.get(id=i['book_id']).img
        i['book_id'] = int(i['book_id'])
        i['img'] = str(img)

    return results
