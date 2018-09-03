import pandas as pd


class DataMerge:
    def __init__(self):
        # self.course_tags = pd.read_csv('data/course_tags.csv')
        # self.user_assessment = pd.read_csv('data/user_assessment_scores.csv')
        # self.user_views = pd.read_csv('data/user_course_views.csv')
        self.user_interests = pd.read_csv('data/user_interests.csv')

    def merge_func(self):
        course_join = self.course_tags.merge(self.user_interests, left_on='course_tags', right_on='interest_tag',
                                             how='inner',
                                             left_index=True)
        user_join = self.user_assessment.merge(self.user_views, left_on='user_handle', right_on='user_handle',
                                               how='inner')
        data = course_join.merge(user_join,
                                 left_on=['user_handle', 'course_id'],
                                 right_on=['user_handle', 'course_id'],
                                 how='inner')

        course_join.to_csv('course_join.csv', index=None)
        user_join.to_csv('user_join.csv', index=None)
        data.to_csv('data.csv', index=None)

    def check_format(self):
        a = pd.read_csv('course_join.csv')
        print a.head(5)

    def create_individual_vectors(self):
        from sklearn.metrics import pairwise_distances
        from scipy.spatial.distance import cosine, correlation
        import sys
        ss = self.user_interests.drop('date_followed', axis=1)#.head(3)
        sss = pd.concat([ss, pd.get_dummies(ss['interest_tag'])], axis=1)
        # print sss
        # print sss.columns.values
        feature_list = list(sss.columns.values)
        feature_list.remove('user_handle')
        df = sss.groupby('user_handle')[feature_list].sum()
        df.reset_index(inplace=True)
        print df.head()
        user_list = list(df['user_handle'].apply(str))
        # print user_list
        # sys.exit(0)
        df = df.drop('user_handle', axis=1)
        # df.reset_index(inplace=True)
        # user_list.insert(0, 'features')
        # df.columns = user_list
        # print df
        # sys.exit(0)
        user_sim = pairwise_distances(df.as_matrix(), metric="jaccard")
        print type(user_sim)
        user_sim_df = pd.DataFrame(user_sim)
        print user_sim_df.shape
        user_sim_df.to_csv('xx.csv')


if __name__:
    s = DataMerge()
    # s.merge_func()
    # s.check_format()
    s.create_individual_vectors()
