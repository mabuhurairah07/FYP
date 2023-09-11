# recommendation.py
from sklearn.metrics.pairwise import cosine_similarity

class ProductRecommender:
    def __init__(self, user_feedback_df):
        self.user_feedback_df = user_feedback_df
        self.product_similarity_matrix = self._calculate_similarity_matrix()

    def _calculate_similarity_matrix(self):
        # Create a user-item matrix (rows: users, columns: products, values: ratings)
        user_item_matrix = self.user_feedback_df.pivot(index='user_id', columns='product_id', values='stars')
        # Fill NaNs with 0 (user hasn't rated a product)
        user_item_matrix = user_item_matrix.fillna(0)
        # Calculate cosine similarity between products
        similarity_matrix = cosine_similarity(user_item_matrix.T)
        return similarity_matrix
