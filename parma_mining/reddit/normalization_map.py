# This class represents our normalization map, will be used at initialization endpoint
class RedditNormalizationMap:
    map_json = {
        "Source": "Reddit",
        "Mappings": [
            {
                "SourceField": "id",
                "DataType": "text",
                "MeasurementName": "company id",
            },
            {"SourceField": "url", "DataType": "link", "MeasurementName": "reddit url"},
            {
                "SourceField": "search_key",
                "DataType": "text",
                "MeasurementName": "search key used to find company",
            },
            {
                "SourceField": "search_type",
                "DataType": "text",
                "MeasurementName": "type of search used to find company",
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
                        "DataType": "boolean",
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
                        "SourceField": "scraped_at",
                        "DataType": "date",
                        "MeasurementName": "timestamp of scraping",
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
                        "DataType": "text",
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
                                "DataType": "text",
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
                                "MeasurementName": "downvote coun of comment",
                            },
                        ],
                    },
                ],
            },
        ],
    }

    def get_normalization_map(self):
        return self.map_json
