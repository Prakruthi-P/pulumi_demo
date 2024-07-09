"""

1.Creating  Bucket In Standard Storage, In The EU Region. 
2.Bucket Configured As Static Website And CORS Configurations
3.Make the bucket publicly accessible
4.Upload index.html to bucket
5.Upload 404.html to bucket
6.Define lifecycle rules
7.Apply lifecycle rules to the bucket
8.Export the bucket URL

"""

import pulumi
import pulumi_gcp as gcp

static_site = gcp.storage.Bucket("static-site",
    name="image-store.com",
    location="EU",
    force_destroy=True,
    uniform_bucket_level_access=True,
    website={
        "mainPageSuffix": "index.html",
        "notFoundPage": "404.html",
    },
    cors=[{
        "origins": ["http://image-store.com"],
        "methods": [
            "GET",
            "HEAD",
            "PUT",
            "POST",
            "DELETE",
        ],
        "responseHeaders": ["*"],
        "maxAgeSeconds": 3600,
    }])

# Make the bucket publicly accessible
bucket_iam_binding = gcp.storage.BucketIAMBinding('bucket-iam-binding',
    bucket=static_site.name,
    role='roles/storage.objectViewer',
    members=['allUsers'],
)

# Upload index.html
index_html = gcp.storage.BucketObject('index.html',
    bucket=static_site.name,
    source=pulumi.FileAsset('index.html'),
    content_type='text/html',
)

# Upload 404.html
not_found_html = gcp.storage.BucketObject('404.html',
    bucket=static_site.name,
    source=pulumi.FileAsset('404.html'),
    content_type='text/html',
)

# Define lifecycle rules
lifecycle_rules = [
    {
        "action": {
            "type": "SetStorageClass",
            "storageClass": "NEARLINE",
        },
        "condition": {
            "age": 30,
        },
    },
    {
        "action": {
            "type": "SetStorageClass",
            "storageClass": "COLDLINE",
        },
        "condition": {
            "age": 90,
        },
    },
    {
        "action": {
            "type": "Delete",
        },
        "condition": {
            "age": 365,
        },
    },
    {
        "action": {
            "type": "Delete",
        },
        "condition": {
            "createdBefore": "2023-01-01T00:00:00Z",
        },
    },
]

# Apply lifecycle rules to the bucket
bucket_lifecycle = gcp.storage.BucketObjectLifecycle("bucket-lifecycle",
    bucket=static_site.name,
    rules=lifecycle_rules,
)
# Export the bucket URL
pulumi.export('bucket_url', pulumi.Output.concat('https://storage.googleapis.com/', static_site.name, '/index.html'))
