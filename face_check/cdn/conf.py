import os

AWS_ACCESS_KEY_ID="DO00CTRXKLG8AZQ994KF"
AWS_SECRET_ACCESS_KEY="89mDaX5tOPl7J3gjbjONmwVent41ODGS/JwUb+kvM0Q"

#AWS_ACCESS_KEY_ID=public_key_id_from_digital_ocean
#AWS_SECRET_ACCESS_KEY=private_key_id_from_digital_ocean

#AWS_ACCESS_KEY_ID=os.environ.get("AWS_ACCESS_KEY_ID") 
#AWS_SECRET_ACCESS_KEY=os.environ.get("AWS_SECRET_ACCESS_KEY") 
AWS_STORAGE_BUCKET_NAME="facecheck"
AWS_S3_ENDPOINT_URL="https://sgp1.digitaloceanspaces.com"

AWS_S3_OBJECT_PARAMETERS = {
  "CacheControl": "max-age=86400",
  "ACL": "public-read"
}
AWS_LOCATION="https://facecheck.sgp1.digitaloceanspaces.com"
AWS_S3_FILE_OVERWRITE = True


DEFAULT_FILE_STORAGE = "face_check.cdn.backends.MediaRootS3Boto3Storage"
STATICFILES_STORAGE = "face_check.cdn.backends.StaticRootS3Boto3Storage"


STATIC_URL = 'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'static')
MEDIA_URL =  'https://%s/%s/' % (AWS_S3_ENDPOINT_URL, 'media')



#STATIC_URL = 'https://facecheck.sgp1.digitaloceanspaces.com/static/' 
#MEDIA_URL = 'https://facecheck.sgp1.digitaloceanspaces.com/media/'

#https://facecheck.sgp1.digitaloceanspaces.com/media/student_images/Helarie_Mea_Genovania.jpg
