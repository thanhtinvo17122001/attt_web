python3 manage.py migrate sessions
python3 manage.py crawler

docker exec mysql_container /usr/bin/mysqldump --no-tablespaces  -u mysql --password=changeme attt_web > backup.sql
docker exec mysql_container /usr/bin/mysqldump --no-tablespaces  -u mysql --password=changeme attt_web > crawler_data.sql

docker exec -i mysql_container mysql -u mysql -p changeme attt_web < db.sql

alter table comments
    add parent_id varchar(36) null after post_id;

alter table comments
    add constraint comments_parent_id_comments_id_
        foreign key (parent_id) references comments (id)
        on delete cascade;

https://cloudinary.com/console/c-8b10f8c5b24da1fcf6648ebd15057f/media_library/folders/home

https://docs.djangoproject.com/en/4.1/howto/custom-management-commands/


STATIC_URL = 'static/'
=> Folder chưa CSS, Javascript của dự án

'DIRS': ['templates/'],
=> folder chứa file template .html

config: Khi tạo django project, tự tạo bởi django
=> ATTT_WEB => đổi tên thành folder config

tạo 1 app trong django
app
- common: File dùng chung
- Controller: Admin, public, auth => gọi service
- management: custom command in django
- models: django models
- modules
  + model: django model
  + service: gọi db => gọi đến model

Mô hình MVC => model - view - controller
controller -> models (trả về view)
controller -> service (gọi model) (trả về view)
service: xử lý logic

Docker-compose
tạo container
Image: mysql => tạo 1 container (máy ảo) => cài sẵn mysql => connect tới db trong container

DataGrip: tool connect db (có thể dùng bất cứ tool nào để connect tới db)