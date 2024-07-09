import pulumi
from pulumi_gcp import storage

# Create a GCS bucket
bucket = storage.Bucket('my-static-website-bucket',
    location='US',
    website=storage.BucketWebsiteArgs(
        main_page_suffix='index.html',
        not_found_page='404.html',
    ),
    uniform_bucket_level_access=True
)

# Make the bucket publicly accessible
bucket_iam_binding = storage.BucketIAMBinding('bucket-iam-binding',
    bucket=bucket.name,
    role='roles/storage.objectViewer',
    members=['allUsers'],
)

# Upload index.html
index_html = storage.BucketObject('index.html',
    bucket=bucket.name,
    source=pulumi.FileAsset('index.html'),
    content_type='text/html',
)

# Upload 404.html
not_found_html = storage.BucketObject('404.html',
    bucket=bucket.name,
    source=pulumi.FileAsset('404.html'),
    content_type='text/html',
)

# Export the bucket URL
pulumi.export('bucket_url', pulumi.Output.concat('https://storage.googleapis.com/', bucket.name, '/index.html'))
