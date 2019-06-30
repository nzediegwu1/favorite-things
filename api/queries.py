conditionally_increment_ranking = """UPDATE api_favourite SET ranking = ranking + 1
                    WHERE ranking > %s AND category_id = %s AND deleted = %s"""
