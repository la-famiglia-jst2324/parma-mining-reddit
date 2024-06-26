"""This class represents our normalization map.

It will be used at initialization endpoint.
"""


class RedditNormalizationMap:
    """Normalization map for Reddit."""

    map_json = {
        "Source": "reddit",
        "Mappings": [
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "company name",
            },
            {
                "SourceField": "searches",
                "DataType": "nested",
                "MeasurementName": "post searches on a subreddit",
                "NestedMappings": [
                    {
                        "SourceField": "subreddit",
                        "DataType": "text",
                        "MeasurementName": "name of subreddit",
                    },
                    {
                        "SourceField": "submissions",
                        "DataType": "nested",
                        "MeasurementName": "submissions on reddit",
                        "NestedMappings": [
                            {
                                "SourceField": "author",
                                "DataType": "text",
                                "MeasurementName": "author of submission",
                            },
                            {
                                "SourceField": "comment_count",
                                "DataType": "int",
                                "MeasurementName": "comment count of submission",
                            },
                            {
                                "SourceField": "created_at",
                                "DataType": "date",
                                "MeasurementName": "submission creation date",
                            },
                            {
                                "SourceField": "id",
                                "DataType": "text",
                                "MeasurementName": "id of submission",
                            },
                            {
                                "SourceField": "is_original_content",
                                "DataType": "bool",
                                "MeasurementName": "is submission original content",
                            },
                            {
                                "SourceField": "is_self",
                                "DataType": "bool",
                                "MeasurementName": "does submission contain self text",
                            },
                            {
                                "SourceField": "is_video",
                                "DataType": "bool",
                                "MeasurementName": "is submission video",
                            },
                            {
                                "SourceField": "over18",
                                "DataType": "bool",
                                "MeasurementName": "is submission over 18",
                            },
                            {
                                "SourceField": "permalink",
                                "DataType": "link",
                                "MeasurementName": "permalink of submission",
                            },
                            {
                                "SourceField": "homepage",
                                "DataType": "link",
                                "MeasurementName": "repository homepage url",
                            },
                            {
                                "SourceField": "score",
                                "DataType": "int",
                                "MeasurementName": "like count of submission",
                            },
                            {
                                "SourceField": "subreddit_name",
                                "DataType": "text",
                                "MeasurementName": "name of subreddit",
                            },
                            {
                                "SourceField": "subreddit_description",
                                "DataType": "text",
                                "MeasurementName": "description of subreddit",
                            },
                            {
                                "SourceField": "subreddit_subscribers",
                                "DataType": "int",
                                "MeasurementName": "subscriber count of subreddit",
                            },
                            {
                                "SourceField": "title",
                                "DataType": "text",
                                "MeasurementName": "title of submission",
                            },
                            {
                                "SourceField": "text",
                                "DataType": "paragraph",
                                "MeasurementName": "text of submission",
                            },
                            {
                                "SourceField": "upvote_ratio",
                                "DataType": "float",
                                "MeasurementName": "rate of upvotes to downvotes",
                            },
                            {
                                "SourceField": "url",
                                "DataType": "link",
                                "MeasurementName": "url of submission",
                            },
                            {
                                "SourceField": "comments",
                                "DataType": "nested",
                                "MeasurementName": "comments of the submission",
                                "NestedMappings": [
                                    {
                                        "SourceField": "author",
                                        "DataType": "text",
                                        "MeasurementName": "author name of comment",
                                    },
                                    {
                                        "SourceField": "text",
                                        "DataType": "paragraph",
                                        "MeasurementName": "text of comment",
                                    },
                                    {
                                        "SourceField": "upvotes",
                                        "DataType": "int",
                                        "MeasurementName": "upvote count of of comment",
                                    },
                                    {
                                        "SourceField": "downvotes",
                                        "DataType": "int",
                                        "MeasurementName": "downvote count of comment",
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        ],
    }

    def get_normalization_map(self):
        """Return the normalization map."""
        return self.map_json
